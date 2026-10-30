from __future__ import annotations

import calendar
import datetime as dt

import pandas as pd
import streamlit as st

from data import CAREERS, JOBS, PRACTICAL, PROJECTS, QUIZ, RESOURCES, ALL_SKILLS, CITIES
from logic import (band, detect_skills, detect_years, job_match, read_cv_text, readiness,
                   score_practical, score_quiz, skill_scores)
from ui import (BAR_COLORS, bar, esc, go_page, learning_plan, md, page_head, radar, section, seeker_ctx,
                spark, style_fig, toggle_done)

ROLE = "Job Seeker"


def _record_history():
    p, sc, req, demo, r = seeker_ctx()
    st.session_state.hist.append(round(r))


def _handle_cv(uploaded, key_prefix=""):
    ss = st.session_state
    if uploaded is not None and ss.cv_id != uploaded.file_id:
        text = read_cv_text(uploaded)
        ss.cv_id = uploaded.file_id
        ss.cv_skills = detect_skills(text)
        ss.cv_years = detect_years(text)
        if not text.strip():
            st.warning("Couldn't read text from this file. Try a text-based PDF, DOCX or TXT.")


def ranked_jobs():
    ss = st.session_state
    sc = skill_scores(ss.profile, ss.quiz, ss.practical)
    rows = [(job_match(j, sc), j) for j in JOBS]
    return sorted(rows, key=lambda x: -x[0])


# ---------------------------------------------------------------- dashboard
def dashboard():
    ss = st.session_state
    p, sc, req, demo, r = seeker_ctx()
    verified = sum(1 for s in req if sc[s]["status"] == "Verified")
    plan = learning_plan()
    main, side = st.columns([3.1, 1.15], gap="large")

    with main:
        c1, c2 = st.columns([1, 1.4], gap="medium")
        with c1:
            with st.container(key="card_ready"):
                delta = ss.hist[-1] - ss.hist[-2] if len(ss.hist) > 1 else 0
                cls, arrow = ("up", "▲") if delta >= 0 else ("down", "▼")
                md(f'<div class="ch"><span>Career readiness</span></div>'
                   f'<div class="flex"><div><div class="big">{r:.0f}<small class="{cls}">{arrow} {abs(delta)} pts</small></div>'
                   f'<div class="cap">{esc(band(r))}</div></div>{spark(ss.hist)}</div>')
        with c2:
            with st.container(key="card_tracker"):
                top = sorted(req.items(), key=lambda x: -x[1])[:3]
                bars = "".join(bar(s, min(demo[s] / lvl * 100, 100), BAR_COLORS[i]) for i, (s, lvl) in enumerate(top))
                md(f'<div class="flex" style="align-items:stretch"><div style="min-width:40%"><div class="ch">Skill tracker</div>'
                   f'<div class="big" style="margin-top:1.6rem">{verified}<small class="cap">/ {len(req)}</small></div>'
                   f'<div class="cap">Skills verified for {esc(p["career"])}</div></div><div style="flex:1">{bars}</div></div>')
                st.button("+ View all skills", key="lnk_skills", on_click=go_page, args=(ROLE, "Skill-Gap Report"))

        j1, j2, j3 = st.columns([1.3, 1.1, 1.1], gap="medium")
        with j1:
            with st.container(key="card_dark_jobs"):
                ranks = ranked_jobs()
                m, job = ranks[ss.job_idx % len(ranks)]
                md(f'<div style="font-weight:600">Job feed</div><div class="jobcard"><div style="display:flex;align-items:center">'
                   f'<span class="logo">{esc(job["company"][0])}</span><div><div class="t">{esc(job["title"])}</div>'
                   f'<div class="cap">{esc(job["company"])} · {esc(job["city"])}</div></div></div>'
                   f'<div class="m">{esc(job["pay"])}/month · {esc(job["type"])}</div>{bar("Skill match", m, "#06D6A0")}</div>')
                b1, b2 = st.columns(2)
                applied = job["id"] in ss.applied
                if b1.button("Applied ✓" if applied else "Apply", key="dash_apply", disabled=applied, width="stretch"):
                    ss.applied.add(job["id"])
                    st.rerun()
                if b2.button("Next job", key="dash_next", width="stretch"):
                    ss.job_idx += 1
                    st.rerun()
        with j2:
            with st.container(key="card_mock"):
                md('<div class="ch"><span class="chip p">OFFER</span></div><h3 style="margin:.8rem 0 .3rem;font-size:1.3rem">Try our mock interview</h3>'
                   '<div class="cap">Practise answers to common questions for your target role, with no stress.</div>')
                with st.popover("Schedule"):
                    d = st.date_input("Date", dt.date.today() + dt.timedelta(days=2), key="mock_date")
                    if st.button("Add to calendar", key="mock_add", type="primary"):
                        ss.sessions[d.isoformat()] = "Mock interview"
                        st.rerun()
        with j3:
            with st.container(key="card_cv"):
                md('<div style="text-align:center;font-weight:800;font-size:1.15rem">Upload your CV</div>'
                   '<div class="cap" style="text-align:center">We will detect your skills and pre-fill your profile.</div>')
                up = st.file_uploader("CV", type=["pdf", "docx", "txt", "md"], key="cv_dash", label_visibility="collapsed")
                _handle_cv(up)
                if ss.cv_skills:
                    st.caption(f"Detected {len(ss.cv_skills)} skills: " + ", ".join(ss.cv_skills[:6]) + ("…" if len(ss.cv_skills) > 6 else ""))

        section("Course recommendations")
        if not plan:
            st.success("You meet the rubric for every skill in this career path. Try another career in Profile & CV.")
        else:
            cols = st.columns(3, gap="medium")
            for i, (s, g, res, proj) in enumerate(plan[:3]):
                tone = ["pink", "lav", "butter"][i % 3]
                key = f"{s}|{res[0]}"
                with cols[i]:
                    with st.container(key=f"card_{tone}_rec{i}"):
                        done = key in ss.done
                        md(f'<div class="rec"><h3>{esc(s)}</h3><div class="cap" style="color:#555">{esc(res[0])}</div>'
                           f'<div style="margin:.8rem 0"><span class="tag">#{esc(res[1].lower())}</span><span class="tag">#{res[2]}h</span>'
                           f'<span class="tag">gap {g:.0f}</span></div><div style="font-size:.85rem;font-weight:600">Project: {esc(proj)}</div></div>')
                        st.button("Done ✓" if done else "Mark done", key=f"rec_{i}", on_click=toggle_done, args=(key,))

    with side:
        today = dt.date.today()
        with st.container(key="card_calendar"):
            weeks = calendar.Calendar(firstweekday=6).monthdatescalendar(today.year, today.month)
            rows = ""
            for w in weeks:
                cells = ""
                for d in w:
                    cls = "in" if d.month == today.month else "out"
                    if d.isoformat() in ss.sessions:
                        cls = "ses"
                    if d == today:
                        cls += " today"
                    cells += f'<td class="{cls}" title="{esc(ss.sessions.get(d.isoformat(), ""))}">{d.day}</td>'
                rows += f"<tr>{cells}</tr>"
            md(f'<div class="ch" style="margin-bottom:.6rem">{today.strftime("%B %Y")}</div><table class="cal"><tr>'
               + "".join(f"<th>{x}</th>" for x in "SMTWTFS") + f"</tr>{rows}</table>")
        section("Upcoming lessons")
        with st.container(key="card_grey_lesson"):
            if plan:
                s, g, res, proj = plan[0]
                total = len(plan)
                donecount = sum(1 for k in ss.done if k.split("|")[0] in CAREERS[p["career"]])
                pct = 100 * donecount / max(total + donecount, 1)
                md(f'<h3 style="margin:.2rem 0">{esc(s)}</h3><div class="cap">{esc(res[0])}</div>'
                   f'<div style="margin:1rem 0 .3rem">{bar("Plan progress", pct, "#06D6A0")}</div>'
                   f'<div class="cap">{donecount} of {total + donecount} plan items done</div>')
                st.button("Open roadmap", key="open_road", type="primary", on_click=go_page, args=(ROLE, "Learning Roadmap"))
            else:
                st.write("No lessons pending.")
        with st.container(key="card_soft_comm"):
            md('<div class="big2">1350+</div><div class="cap">Members in our community</div>')
            if st.button("Joined ✓" if ss.joined else "Join", key="join_comm"):
                ss.joined = not ss.joined
                st.rerun()


# ---------------------------------------------------------------- profile & CV
def profile_page():
    ss = st.session_state
    p = ss.profile
    page_head("Profile & CV", "Tell us your goal. Self-ratings are useful, but only verified results count in full.")
    left, right = st.columns([1.2, 1], gap="large")
    with left:
        with st.container(key="card_profile"):
            name = st.text_input("Name", p["name"])
            career = st.selectbox("Career goal", list(CAREERS), index=list(CAREERS).index(p["career"]))
            years = st.number_input("Years of experience", 0, 30, int(p["years"] or ss.cv_years))
            st.markdown("**Rate your skills (0-100)**")
            st.caption("Self-ratings count at half weight until you verify them with an assessment.")
            new_self = {}
            for s in CAREERS[career]:
                default = p["self"].get(s, 40 if s in ss.cv_skills else 0)
                new_self[s] = st.slider(s, 0, 100, int(default), key=f"self_{career}_{s}")
            if st.button("Save profile", type="primary"):
                ss.profile = {"name": name, "career": career, "years": years,
                              "self": {k: v for k, v in new_self.items() if v > 0} | {k: v for k, v in p["self"].items() if k not in CAREERS[career]}}
                st.toast("Profile saved")
                st.rerun()
    with right:
        with st.container(key="card_cvpage"):
            st.markdown("**Upload your CV**")
            up = st.file_uploader("CV file", type=["pdf", "docx", "txt", "md"], key="cv_page", label_visibility="collapsed")
            _handle_cv(up)
            if ss.cv_skills:
                md("".join(f'<span class="chip g">{esc(s)}</span>' for s in ss.cv_skills))
                st.caption(f"Experience mentioned: {ss.cv_years} years" if ss.cv_years else "No experience duration found.")
                st.caption("Detected skills pre-fill your sliders at 40 until you verify them.")
            else:
                st.info("Upload a CV to detect skills automatically.")


# ---------------------------------------------------------------- assessments
def assessments_page():
    ss = st.session_state
    p, sc, req, demo, r = seeker_ctx()
    page_head("Assessments", "Short quizzes and a practical task that turn claims into evidence.")
    tab1, tab2 = st.tabs(["Skill quizzes", "Practical task"])
    with tab1:
        pick = st.multiselect("Skills to assess", list(req), default=[s for s in req if s not in ss.quiz][:3])
        if not pick:
            st.info("Choose at least one skill to start.")
        else:
            with st.form("quiz_form"):
                answers = {}
                for s in pick:
                    st.markdown(f"#### {s}")
                    answers[s] = []
                    for qi, (q, opts, _) in enumerate(QUIZ[s]):
                        answers[s].append(st.radio(q, opts, index=None, key=f"q_{s}_{qi}"))
                submitted = st.form_submit_button("Submit answers", type="primary")
            if submitted:
                missing = [s for s in pick if any(a is None for a in answers[s])]
                if missing:
                    st.error("Answer every question for: " + ", ".join(missing))
                else:
                    for s in pick:
                        chosen = [QUIZ[s][i][1].index(a) for i, a in enumerate(answers[s])]
                        ss.quiz[s] = score_quiz(s, chosen)
                    _record_history()
                    st.success("Saved: " + ", ".join(f"{s} {ss.quiz[s]}%" for s in pick))
                    st.rerun()
        if ss.quiz:
            st.markdown("**Your verified quiz results**")
            st.dataframe(pd.DataFrame({"Skill": list(ss.quiz), "Score %": list(ss.quiz.values())}), hide_index=True, width="stretch")
    with tab2:
        task = PRACTICAL[p["career"]]
        with st.container(key="card_task"):
            md(f'<h3 style="margin:0 0 .3rem">{esc(task["title"])}</h3><div class="cap">{esc(task["prompt"])}</div>'
               + "".join(f'<span class="chip">{esc(s)}</span>' for s in task["skills"]))
            text = st.text_area("Your answer", height=220, key=f"prac_{p['career']}")
            if st.button("Submit task", type="primary", key="prac_submit"):
                score, hits, words = score_practical(p["career"], text)
                if words < 40:
                    st.error(f"Write at least 40 words ({words} so far) so the rubric has something to assess.")
                else:
                    ss.practical[p["career"]] = {"score": score, "hits": hits}
                    _record_history()
                    st.rerun()
        res = ss.practical.get(p["career"])
        if res:
            st.markdown(f"**Task score: {res['score']}%**")
            for label, ok in res["hits"]:
                st.markdown(f"{'✅' if ok else '⬜'} {label}")
            st.caption("This is a transparent keyword rubric for the prototype. Production use should add model or human review.")


# ---------------------------------------------------------------- gap report
def gap_report_page():
    ss = st.session_state
    p, sc, req, demo, r = seeker_ctx()
    page_head("Skill-Gap Report", f"{p['name']} · target role: {p['career']}")
    c1, c2 = st.columns([1, 1.4], gap="large")
    with c1:
        with st.container(key="card_score"):
            md(f'<div class="ch">Career readiness score</div><div class="big">{r:.0f}<small class="cap">/ 100</small></div>'
               f'<div style="font-weight:700">{esc(band(r))}</div>')
        md('<div class="note">This score shows performance against a defined role rubric. It is not a measure of your worth or employability.</div>')
        unv = [s for s in req if sc[s]["status"] != "Verified"]
        if unv:
            st.warning(f"{len(unv)} skills are not yet verified: " + ", ".join(unv))
    with c2:
        skills = list(req)
        st.plotly_chart(radar({"Demonstrated": [round(demo[s]) for s in skills], "Required": [req[s] for s in skills]}, skills),
                        width="stretch")
    df = pd.DataFrame([{"Skill": s, "Required": req[s], "Demonstrated": round(demo[s]), "Gap": max(req[s] - round(demo[s]), 0),
                        "Evidence": sc[s]["status"]} for s in req]).sort_values("Gap", ascending=False)
    strengths = df[df["Gap"] == 0]["Skill"].tolist()
    weak = df[df["Gap"] > 0].head(3)["Skill"].tolist()
    s1, s2 = st.columns(2, gap="large")
    with s1:
        st.markdown("**Demonstrated strengths**")
        md("".join(f'<span class="chip g">{esc(s)}</span>' for s in strengths) or '<span class="cap">None yet. Take an assessment.</span>')
    with s2:
        st.markdown("**Areas requiring improvement**")
        md("".join(f'<span class="chip o">{esc(s)}</span>' for s in weak) or '<span class="cap">No gaps against this rubric.</span>')
    st.dataframe(df, hide_index=True, width="stretch",
                 column_config={"Demonstrated": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d"),
                                "Required": st.column_config.NumberColumn(format="%d")})
    report = (f"SkillBridge AI skill-gap report\nName: {p['name']}\nTarget: {p['career']}\nReadiness: {r:.0f}/100 ({band(r)})\n\n"
              + df.to_csv(index=False))
    st.download_button("Download report", report, file_name="skill_gap_report.txt")


# ---------------------------------------------------------------- roadmap
def roadmap_page():
    ss = st.session_state
    p, sc, req, demo, r = seeker_ctx()
    plan = learning_plan()
    page_head("Learning Roadmap", "Your biggest gaps first, each with one resource and one project.")
    donecount = sum(1 for k in ss.done if k.split("|")[0] in req)
    total = len(plan) + donecount
    md(bar("Roadmap progress", 100 * donecount / max(total, 1), "#8B4DFF"))
    covered = {k.split("|")[0] for k in ss.done}
    items = plan + [(s, 0, RESOURCES[s][0], PROJECTS[s]) for s in req if s in covered and s not in {x[0] for x in plan}]
    if not items:
        st.success("Nothing left on your roadmap. Re-run assessments to confirm your progress.")
    for i, (s, g, res, proj) in enumerate(items):
        key = f"{s}|{res[0]}"
        done = key in ss.done
        with st.container(key=f"card_{['pink', 'lav', 'butter'][i % 3]}_road{i}"):
            a, b = st.columns([4, 1])
            with a:
                link = f' · <a href="{res[3]}" target="_blank">open</a>' if res[3] else ""
                md(f'<div class="rec"><h3>{esc(s)} <span class="chip o">gap {g:.0f}</span></h3>'
                   f'<div><b>Learn:</b> {esc(res[0])} · {esc(res[1])} · ~{res[2]}h{link}</div>'
                   f'<div style="margin-top:.3rem"><b>Build:</b> {esc(proj)}</div></div>')
            with b:
                st.button("Done ✓" if done else "Mark done", key=f"road_{i}", on_click=toggle_done, args=(key,), width="stretch")
    st.caption("Marking an item done tracks effort only. Re-take the assessment to improve your verified score.")


# ---------------------------------------------------------------- portfolio
def portfolio_page():
    ss = st.session_state
    p, sc, req, demo, r = seeker_ctx()
    page_head("Portfolio", "Evidence employers can review: real projects tied to real skills.")
    with st.expander("Add a project", expanded=not ss.portfolio):
        with st.form("proj_form", clear_on_submit=True):
            title = st.text_input("Project title")
            link = st.text_input("Link (GitHub, demo, write-up)")
            skills = st.multiselect("Skills demonstrated", ALL_SKILLS)
            desc = st.text_area("What did you build and what was your role?", height=100)
            if st.form_submit_button("Add project", type="primary"):
                if not title.strip() or not skills:
                    st.error("Add a title and at least one skill.")
                else:
                    ss.portfolio.append({"title": title.strip(), "link": link.strip(), "skills": skills, "desc": desc.strip()})
                    st.rerun()
    if not ss.portfolio:
        st.info("No projects yet. Pick one from your Learning Roadmap and add it here.")
    cols = st.columns(2, gap="medium")
    for i, pr in enumerate(ss.portfolio):
        with cols[i % 2]:
            with st.container(key=f"card_{['lav', 'butter', 'pink'][i % 3]}_pf{i}"):
                link = f'<a href="{esc(pr["link"])}" target="_blank">{esc(pr["link"])}</a>' if pr["link"].startswith("http") else esc(pr["link"])
                md(f'<div class="rec"><h3>{esc(pr["title"])}</h3><div style="font-size:.9rem">{esc(pr["desc"])}</div>'
                   f'<div style="margin:.6rem 0">{"".join(f"<span class=chip>{esc(s)}</span>" for s in pr["skills"])}</div><div class="cap">{link}</div></div>')
                if st.button("Remove", key=f"pf_rm_{i}"):
                    ss.portfolio.pop(i)
                    st.rerun()


# ---------------------------------------------------------------- job board
def job_board_page():
    ss = st.session_state
    page_head("Job Board", "Roles ranked by how well your verified skills match the requirements.")
    f1, f2, f3 = st.columns([1, 1, 1])
    city = f1.multiselect("City", CITIES)
    typ = f2.multiselect("Type", ["Full-time", "Internship"])
    min_m = f3.slider("Minimum match %", 0, 100, 0)
    q = ss.get("q", "").lower()
    sc = skill_scores(ss.profile, ss.quiz, ss.practical)
    shown = 0
    for m, j in ranked_jobs():
        if (city and j["city"] not in city) or (typ and j["type"] not in typ) or m < min_m:
            continue
        if q and q not in (j["title"] + j["company"]).lower():
            continue
        shown += 1
        with st.expander(f"{j['title']} · {j['company']} · {m:.0f}% match"):
            md(f'<span class="chip p">{esc(j["city"])}</span><span class="chip">{esc(j["type"])}</span><span class="chip g">{esc(j["pay"])}/month</span>')
            for s, lvl in j["req"].items():
                have = sc[s]["value"]
                md(bar(f"{s} (needs {lvl})", min(have / lvl * 100, 100), "#06D6A0" if have >= lvl else "#F7BE0B"))
            a, b = st.columns(2)
            applied = j["id"] in ss.applied
            if a.button("Applied ✓" if applied else "Apply", key=f"apply_{j['id']}", disabled=applied, type="primary"):
                ss.applied.add(j["id"])
                st.rerun()
            saved = j["id"] in ss.saved
            if b.button("Saved ✓" if saved else "Save", key=f"save_{j['id']}"):
                ss.saved.symmetric_difference_update({j["id"]})
                st.rerun()
    if not shown:
        st.info("No roles match those filters.")
    st.caption("Sample listings for demonstration. Basic job access should stay free for job seekers.")
