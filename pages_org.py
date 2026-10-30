from __future__ import annotations

import random

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from data import ALL_SKILLS, CAREERS, CITIES, PROJECTS, QUIZ, STATUSES, coverage, employer_demand
from logic import band
from ui import bar, esc, md, page_head, radar, section, style_fig

K_MIN = 5  # smallest group size shown in aggregated views


def _fit(row, req):
    return round(coverage({s: row[s] for s in req}, req) * 100)


# ================================================================ EMPLOYER
def emp_overview():
    ss = st.session_state
    page_head("Employer Overview", "AI assists the shortlist. You make every hiring decision.")
    stat = pd.Series(ss.cand_status).value_counts()
    k = st.columns(4)
    k[0].metric("Open vacancies", sum(v["open"] for v in ss.vacancies))
    k[1].metric("Applicants", len(ss.cand_status))
    k[2].metric("Assessed", sum(1 for v in ss.cand_status.values() if v not in ("Applied", "Rejected")))
    k[3].metric("Shortlisted", int(stat.get("Shortlisted", 0)))
    order = ["Applied", "Assessed", "Shortlisted", "Interview", "Offer"]
    reached = [sum(1 for v in ss.cand_status.values() if v in order[i:] or (i == 0 and v == "Rejected")) for i in range(5)]
    c1, c2 = st.columns([1.2, 1], gap="large")
    with c1:
        fig = go.Figure(go.Funnel(y=order, x=reached, marker=dict(color=["#A3B4FF", "#8B4DFF", "#06D6A0", "#F7BE0B", "#FF7A1A"])))
        st.plotly_chart(style_fig(fig, 340), width="stretch")
    with c2:
        v = ss.vacancies[0]
        df = ss.cands.copy()
        df["Fit %"] = df.apply(lambda r: _fit(r, v["req"]), axis=1)
        top = df.sort_values("Fit %", ascending=False).head(5)[["Name", "Fit %", "City"]]
        st.markdown(f"**Top fits for {v['title']}**")
        st.dataframe(top, hide_index=True, width="stretch",
                     column_config={"Fit %": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d")})


def emp_vacancies():
    ss = st.session_state
    page_head("Vacancies", "Define required and preferred skills instead of relying on CV keywords.")
    with st.expander("Publish a vacancy", expanded=False):
        with st.form("vac_form", clear_on_submit=True):
            a, b, c = st.columns(3)
            title = a.text_input("Job title")
            city = b.selectbox("City", CITIES)
            typ = c.selectbox("Type", ["Full-time", "Internship", "Contract"])
            pay = st.text_input("Monthly pay range (PKR)", "PKR 90k-130k")
            req_s = st.multiselect("Required skills", ALL_SKILLS)
            level = st.slider("Required level for these skills", 30, 95, 60)
            pref = st.multiselect("Preferred skills", ALL_SKILLS)
            if st.form_submit_button("Publish vacancy", type="primary"):
                if not title.strip() or not req_s:
                    st.error("Add a title and at least one required skill.")
                else:
                    ss.vacancies.append({"id": len(ss.vacancies) + 1, "title": title.strip(), "city": city, "type": typ, "pay": pay,
                                         "req": {s: level for s in req_s}, "pref": [s for s in pref if s not in req_s], "open": True})
                    st.rerun()
    for i, v in enumerate(ss.vacancies):
        with st.container(key=f"card_{['lav', 'butter', 'pink'][i % 3]}_vac{i}"):
            a, b = st.columns([4, 1])
            with a:
                md(f'<div class="rec"><h3>{esc(v["title"])} <span class="chip {"g" if v["open"] else "r"}">{"Open" if v["open"] else "Closed"}</span></h3>'
                   f'<div class="cap" style="color:#555">{esc(v["city"])} · {esc(v["type"])} · {esc(v["pay"])}</div>'
                   f'<div style="margin-top:.6rem"><b>Required:</b> ' + "".join(f'<span class="chip p">{esc(s)} ≥{l}</span>' for s, l in v["req"].items()) + '</div>'
                   f'<div><b>Preferred:</b> ' + ("".join(f'<span class="chip">{esc(s)}</span>' for s in v["pref"]) or "None") + '</div></div>')
            with b:
                if st.button("Close" if v["open"] else "Reopen", key=f"vac_t{i}", width="stretch"):
                    v["open"] = not v["open"]
                    st.rerun()
                if st.button("Delete", key=f"vac_d{i}", width="stretch") and len(ss.vacancies) > 1:
                    ss.vacancies.pop(i)
                    st.rerun()


def emp_assessments():
    ss = st.session_state
    page_head("Assessments", "Create practical assessments tied to the skills you hire for.")
    with st.form("asm_form", clear_on_submit=True):
        a, b = st.columns(2)
        title = a.text_input("Assessment name")
        fmt = b.selectbox("Format", ["Quiz", "Practical task", "Quiz + practical"])
        skills = st.multiselect("Skills assessed", ALL_SKILLS)
        c, d = st.columns(2)
        minutes = c.number_input("Time limit (minutes)", 10, 180, 45)
        pass_mark = d.slider("Pass mark %", 30, 90, 60)
        brief = st.text_area("Candidate instructions / task brief", height=100)
        if st.form_submit_button("Create assessment", type="primary"):
            if not title.strip() or not skills:
                st.error("Add a name and at least one skill.")
            else:
                ss.emp_assess.append({"title": title.strip(), "skills": skills, "format": fmt, "minutes": minutes, "pass": pass_mark, "brief": brief})
                st.rerun()
    df = pd.DataFrame([{"Assessment": a["title"], "Format": a["format"], "Skills": ", ".join(a["skills"]), "Minutes": a["minutes"], "Pass %": a["pass"]} for a in ss.emp_assess])
    st.dataframe(df, hide_index=True, width="stretch")
    st.caption("Question banks available from SkillBridge: " + ", ".join(f"{s} ({len(q)})" for s, q in QUIZ.items()))


def _set_status(cid, status):
    st.session_state.cand_status[cid] = status


def emp_candidates():
    ss = st.session_state
    page_head("Candidates", "Compare evidence: assessments, projects and fit to your requirements.")
    vtitle = st.selectbox("Vacancy", [v["title"] for v in ss.vacancies])
    v = next(x for x in ss.vacancies if x["title"] == vtitle)
    req = v["req"]
    df = ss.cands.copy()
    df["Fit %"] = df.apply(lambda r: _fit(r, req), axis=1)
    df["Assessment %"] = df.apply(lambda r: round(sum(r[s] for s in req) / len(req)), axis=1)
    df["Status"] = df["id"].map(ss.cand_status)
    f1, f2, f3 = st.columns(3)
    min_fit = f1.slider("Minimum fit %", 0, 100, 0)
    cities = f2.multiselect("City", CITIES)
    stat = f3.multiselect("Status", STATUSES)
    q = ss.get("q", "").lower()
    view = df[df["Fit %"] >= min_fit]
    if cities:
        view = view[view["City"].isin(cities)]
    if stat:
        view = view[view["Status"].isin(stat)]
    if q:
        view = view[view["Name"].str.lower().str.contains(q)]
    view = view.sort_values("Fit %", ascending=False)
    st.dataframe(view[["Name", "University", "City", "Experience (yrs)", "Projects", "Fit %", "Assessment %", "Status"]],
                 hide_index=True, width="stretch",
                 column_config={"Fit %": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d"),
                                "Assessment %": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d")})
    if view.empty:
        st.info("No candidates match these filters.")
        return
    tab1, tab2 = st.tabs(["Compare candidates", "Candidate detail"])
    skills = list(req)
    with tab1:
        names = st.multiselect("Pick up to 4", view["Name"].tolist(), default=view["Name"].tolist()[:3], max_selections=4)
        if names:
            series = {n: [int(view[view["Name"] == n].iloc[0][s]) for s in skills] for n in names}
            if len(skills) >= 3:
                st.plotly_chart(radar(series, skills), width="stretch")
            comp = pd.DataFrame(series, index=skills)
            comp.loc["Fit %"] = [int(view[view["Name"] == n].iloc[0]["Fit %"]) for n in names]
            st.dataframe(comp, width="stretch")
    with tab2:
        who = st.selectbox("Candidate", view["Name"].tolist())
        row = view[view["Name"] == who].iloc[0]
        cid = int(row["id"])
        a, b = st.columns([1.2, 1], gap="large")
        with a:
            md(f'<h3 style="margin:0">{esc(who)}</h3><div class="cap">{esc(row["University"])} · {esc(row["City"])} · {row["Experience (yrs)"]} yrs experience</div>')
            md("".join(bar(f"{s} (needs {l})", row[s], "#06D6A0" if row[s] >= l else "#F7BE0B") for s, l in req.items()))
        with b:
            strengths = [s for s, l in req.items() if row[s] >= l]
            gaps = [s for s, l in req.items() if row[s] < l]
            st.markdown("**Why this fit (explainable)**")
            md(f'<div class="note">Meets {len(strengths)} of {len(req)} required levels. '
               f'Strong: {esc(", ".join(strengths) or "none yet")}. Below target: {esc(", ".join(gaps) or "none")}.</div>')
            rng = random.Random(cid)
            projs = rng.sample(list(PROJECTS.values()), min(int(row["Projects"]), 3))
            st.markdown("**Portfolio evidence**")
            st.write("\n".join(f"- {p}" for p in projs) or "No projects submitted.")
            st.caption(f"Current status: **{ss.cand_status[cid]}**")
            b1, b2, b3 = st.columns(3)
            for col, label, new in ((b1, "Shortlist", "Shortlisted"), (b2, "Interview", "Interview"), (b3, "Reject", "Rejected")):
                col.button(label, key=f"cs_{new}_{cid}", on_click=_set_status, args=(cid, new), width="stretch")
        st.caption("Scores are decision support. Review portfolios and interview before deciding.")


def emp_performance():
    ss = st.session_state
    page_head("Recruitment Performance", "Track how your hiring funnel is moving.")
    n = len(ss.cand_status)
    assessed = sum(1 for v in ss.cand_status.values() if v not in ("Applied", "Rejected"))
    k = st.columns(4)
    k[0].metric("Assessment completion", f"{100 * assessed / max(n, 1):.0f}%")
    k[1].metric("Offers", sum(1 for v in ss.cand_status.values() if v == "Offer"))
    k[2].metric("Avg. days to shortlist", "6.4", help="Sample figure for the demo")
    k[3].metric("Applicants / vacancy", f"{n / max(len(ss.vacancies), 1):.0f}")
    rng = random.Random(9)
    weeks = [f"W{i}" for i in range(1, 9)]
    df = pd.DataFrame({"Week": weeks, "Applications": [rng.randint(6, 22) for _ in weeks], "Assessed": [rng.randint(3, 15) for _ in weeks]})
    st.plotly_chart(style_fig(px.bar(df, x="Week", y=["Applications", "Assessed"], barmode="group"), 340), width="stretch")
    st.caption("Weekly trend is sample data. Funnel counts above come from your shortlisting actions.")


def emp_intel():
    ss = st.session_state
    page_head("Skills Intelligence", f"Aggregated and privacy-protected. Groups under {K_MIN} people are hidden.")
    pool = ss.pool
    goal = st.selectbox("Career goal", ["All"] + list(CAREERS))
    d = pool if goal == "All" else pool[pool["Career goal"] == goal]
    g = d.groupby("City")
    sizes = g.size()
    avg = g[ALL_SKILLS].mean().round(0)
    avg.loc[sizes[sizes < K_MIN].index] = float("nan")
    fig = px.imshow(avg, aspect="auto", color_continuous_scale=["#F8D7FB", "#DDE3FF", "#8B4DFF"], text_auto=True, zmin=0, zmax=100)
    st.plotly_chart(style_fig(fig, 320), width="stretch")
    hidden = sizes[sizes < K_MIN].index.tolist()
    st.caption(f"Candidates in view: {len(d)}." + (f" Suppressed small groups: {', '.join(hidden)}." if hidden else ""))
    overall = d[ALL_SKILLS].mean().sort_values()
    st.markdown("**Scarcest skills in this pool**")
    md("".join(f'<span class="chip o">{esc(s)} · {v:.0f}</span>' for s, v in overall.head(5).items()))


# ================================================================ UNIVERSITY
def uni_overview():
    ss = st.session_state
    c = ss.cohort
    page_head("University Overview", "Aggregated skills evidence for your students. No personal data shown.")
    k = st.columns(4)
    k[0].metric("Students assessed", len(c))
    k[1].metric("Avg. readiness", f"{c['Readiness'].mean():.0f}")
    k[2].metric("Approaching rubric (65+)", f"{100 * (c['Readiness'] >= 65).mean():.0f}%")
    weakest = c[ALL_SKILLS].mean().sort_values().index[0]
    k[3].metric("Weakest skill", weakest)
    fig = px.histogram(c, x="Readiness", nbins=10, color="Program", color_discrete_sequence=["#8B4DFF", "#06D6A0", "#F7BE0B"])
    st.plotly_chart(style_fig(fig, 340), width="stretch")


def uni_skills():
    ss = st.session_state
    page_head("Skill Assessment", "Assess practical skills across programs and launch cohort assessments.")
    avg = ss.cohort.groupby("Program")[ALL_SKILLS].mean().round(0).T.reset_index().rename(columns={"index": "Skill"})
    fig = px.bar(avg.melt(id_vars="Skill", var_name="Program", value_name="Avg score"), x="Skill", y="Avg score", color="Program", barmode="group",
                 color_discrete_sequence=["#8B4DFF", "#06D6A0", "#F7BE0B"])
    st.plotly_chart(style_fig(fig, 380), width="stretch")
    with st.form("cohort_asm"):
        skills = st.multiselect("Skills for the next cohort assessment", ALL_SKILLS, default=["Testing", "Communication"])
        prog = st.selectbox("Program", ss.cohort["Program"].unique())
        due = st.date_input("Due date")
        if st.form_submit_button("Launch assessment", type="primary"):
            ss.setdefault("launched", []).append({"Program": prog, "Skills": ", ".join(skills), "Due": str(due)})
            st.rerun()
    if ss.get("launched"):
        st.dataframe(pd.DataFrame(ss.launched), hide_index=True, width="stretch")


def _gaps_vs_employers():
    ss = st.session_state
    dem = employer_demand()
    avg = ss.cohort[list(dem)].mean().round(0)
    df = pd.DataFrame({"Skill": list(dem), "Employer demand": list(dem.values()), "Cohort average": [int(avg[s]) for s in dem]})
    df["Gap"] = (df["Employer demand"] - df["Cohort average"]).clip(lower=0)
    return df.sort_values("Gap", ascending=False)


def uni_gaps():
    page_head("Skill Gaps vs Employers", "Compare curriculum outcomes with what employers ask for.")
    df = _gaps_vs_employers()
    fig = px.bar(df, x="Skill", y=["Employer demand", "Cohort average"], barmode="group", color_discrete_sequence=["#0E0E12", "#8B4DFF"])
    st.plotly_chart(style_fig(fig, 380), width="stretch")
    st.dataframe(df, hide_index=True, width="stretch",
                 column_config={"Gap": st.column_config.ProgressColumn(min_value=0, max_value=60, format="%d")})
    st.caption("Employer demand is the average required level across sample vacancies on the platform.")


def uni_progress():
    ss = st.session_state
    page_head("Student Progress", "Anonymised IDs. Filter by program and semester.")
    c = ss.cohort
    a, b = st.columns(2)
    prog = a.multiselect("Program", c["Program"].unique().tolist())
    sem = b.slider("Semester range", 1, 8, (1, 8))
    v = c[(c["Semester"] >= sem[0]) & (c["Semester"] <= sem[1])]
    if prog:
        v = v[v["Program"].isin(prog)]
    if len(v) < K_MIN:
        st.warning(f"Fewer than {K_MIN} students match. Broaden the filters to protect privacy.")
        return
    line = v.groupby("Semester")["Readiness"].mean().reset_index()
    st.plotly_chart(style_fig(px.line(line, x="Semester", y="Readiness", markers=True, color_discrete_sequence=["#8B4DFF"]), 300), width="stretch")
    st.dataframe(v[["Student", "Program", "Semester", "Track", "Readiness", "Projects", "Assessments done"]], hide_index=True, width="stretch",
                 column_config={"Readiness": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d")})


def uni_projects():
    page_head("Recommended Projects", "Industry-relevant projects for the biggest cohort gaps.")
    df = _gaps_vs_employers().head(5)
    for i, r in enumerate(df.itertuples()):
        with st.container(key=f"card_{['pink', 'lav', 'butter'][i % 3]}_up{i}"):
            md(f'<div class="rec"><h3>{esc(r.Skill)} <span class="chip o">gap {r.Gap}</span></h3><div>{esc(PROJECTS.get(r.Skill, ""))}</div></div>')


def uni_reports():
    ss = st.session_state
    page_head("Reports", "Generate aggregated skills reports for departments and accreditation.")
    c = ss.cohort
    gaps = _gaps_vs_employers()
    table = c.groupby("Program").agg(Students=("Student", "count"), Avg_readiness=("Readiness", "mean")).round(0).reset_index()
    table = table[table["Students"] >= K_MIN]
    st.dataframe(table, hide_index=True, width="stretch")
    summary = ("SkillBridge AI aggregated skills report\n" + f"Students: {len(c)}\nAverage readiness: {c['Readiness'].mean():.0f}\n"
               + "Top gaps vs employers: " + ", ".join(gaps.head(3)["Skill"]) + "\n\n" + gaps.to_csv(index=False))
    st.download_button("Download report", summary, file_name="university_skills_report.txt")


# ================================================================ ADMIN
def admin_overview():
    ss = st.session_state
    page_head("Admin Overview", "Platform health at a glance.")
    k = st.columns(4)
    k[0].metric("Users", len(ss.users))
    k[1].metric("Employers", len(ss.employers))
    k[2].metric("Question banks", len(QUIZ))
    k[3].metric("Open flags", sum(1 for m in ss.mod if m["status"] == "Open"))
    st.info("Use the sidebar to manage accounts, assessments and moderation.")


def admin_users():
    ss = st.session_state
    page_head("Users & Employers", "Edit status inline, then save.")
    t1, t2 = st.tabs(["Users", "Employers"])
    with t1:
        ed = st.data_editor(ss.users, hide_index=True, width="stretch", key="ed_users", disabled=["ID", "Name", "Type", "City"],
                            column_config={"Status": st.column_config.SelectboxColumn(options=["Active", "Suspended"])})
        if st.button("Save user changes", key="save_users"):
            ss.users = ed
            st.toast("Users updated")
    with t2:
        ed2 = st.data_editor(ss.employers, hide_index=True, width="stretch", key="ed_emp", disabled=["Company", "City", "Open vacancies"],
                             column_config={"Status": st.column_config.SelectboxColumn(options=["Verified", "Pending review", "Suspended"]),
                                            "Plan": st.column_config.SelectboxColumn(options=["Free", "Subscription", "Per-vacancy"])})
        if st.button("Save employer changes", key="save_emp"):
            ss.employers = ed2
            st.toast("Employers updated")


def admin_assessments():
    page_head("Assessment Management", "Review the question banks that power skill verification.")
    df = pd.DataFrame([{"Skill": s, "Questions": len(q), "Used in careers": ", ".join(c for c, r in CAREERS.items() if s in r)} for s, q in QUIZ.items()])
    st.dataframe(df, hide_index=True, width="stretch")
    st.caption("Add questions by editing QUIZ in data.py, or connect a question database.")


def admin_moderation():
    ss = st.session_state
    page_head("Moderation", "Review flagged vacancies, portfolios and reports.")
    for i, m in enumerate(ss.mod):
        with st.container(key=f"card_grey_mod{i}"):
            a, b, c = st.columns([4, 1, 1])
            a.markdown(f"**{m['item']}** · {m['reason']}  \nStatus: `{m['status']}`")
            if b.button("Approve", key=f"mod_a{i}", disabled=m["status"] != "Open"):
                m["status"] = "Approved"
                st.rerun()
            if c.button("Remove", key=f"mod_r{i}", disabled=m["status"] != "Open"):
                m["status"] = "Removed"
                st.rerun()


def admin_analytics():
    page_head("Analytics", "Basic usage trends (sample data).")
    rng = random.Random(4)
    w = [f"W{i}" for i in range(1, 11)]
    df = pd.DataFrame({"Week": w, "Job seekers": [rng.randint(20, 90) for _ in w], "Employers": [rng.randint(2, 14) for _ in w]})
    st.plotly_chart(style_fig(px.line(df, x="Week", y=["Job seekers", "Employers"], markers=True), 320), width="stretch")
    asm = pd.DataFrame({"Skill": list(QUIZ), "Attempts": [rng.randint(20, 160) for _ in QUIZ]}).sort_values("Attempts")
    st.plotly_chart(style_fig(px.bar(asm, x="Attempts", y="Skill", orientation="h", color_discrete_sequence=["#8B4DFF"]), 460), width="stretch")
