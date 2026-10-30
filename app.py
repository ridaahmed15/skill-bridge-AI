"""SkillBridge AI: interactive Streamlit dashboard (demo build with sample data)."""
from __future__ import annotations

import streamlit as st

import pages_org as org
import pages_seeker as seeker
from data import (CAREERS, make_admin_employers, make_admin_users, make_candidates, make_cohort, make_pool)
from logic import band, gap_list
from styles import CSS
from ui import esc, md, seeker_ctx

st.set_page_config(page_title="SkillBridge AI", page_icon="🌉", layout="wide", initial_sidebar_state="expanded")
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

NAV = {
    "Job Seeker": [("Dashboard", "dashboard", seeker.dashboard), ("Profile & CV", "badge", seeker.profile_page),
                   ("Assessments", "quiz", seeker.assessments_page), ("Skill-Gap Report", "analytics", seeker.gap_report_page),
                   ("Learning Roadmap", "school", seeker.roadmap_page), ("Portfolio", "folder_special", seeker.portfolio_page),
                   ("Job Board", "work", seeker.job_board_page)],
    "Employer": [("Overview", "dashboard", org.emp_overview), ("Vacancies", "post_add", org.emp_vacancies),
                 ("Assessments", "fact_check", org.emp_assessments), ("Candidates", "groups", org.emp_candidates),
                 ("Recruitment Performance", "monitoring", org.emp_performance), ("Skills Intelligence", "insights", org.emp_intel)],
    "University": [("Overview", "dashboard", org.uni_overview), ("Skill Assessment", "quiz", org.uni_skills),
                   ("Skill Gaps vs Employers", "compare_arrows", org.uni_gaps), ("Student Progress", "trending_up", org.uni_progress),
                   ("Recommended Projects", "lightbulb", org.uni_projects), ("Reports", "summarize", org.uni_reports)],
    "Admin": [("Overview", "dashboard", org.admin_overview), ("Users & Employers", "manage_accounts", org.admin_users),
              ("Assessment Management", "assignment", org.admin_assessments), ("Moderation", "flag", org.admin_moderation),
              ("Analytics", "bar_chart", org.admin_analytics)],
}
ROLE_LABEL = {"Job Seeker": "Student / Job seeker", "Employer": "Employer", "University": "University / Institute", "Admin": "Administrator"}


def init():
    ss = st.session_state
    if ss.get("_init"):
        return
    ss.profile = {"name": "Guest", "career": "Python Developer", "years": 0, "self": {}}
    ss.update(quiz={}, practical={}, done=set(), portfolio=[], applied=set(), saved=set(), sessions={}, job_idx=0,
              hist=[0], cv_id=None, cv_skills=[], cv_years=0, joined=False, q="")
    ss.vacancies = [{"id": 1, "title": "Junior Python Developer", "city": "Karachi", "type": "Full-time", "pay": "PKR 90k-130k",
                     "req": {"Python": 65, "SQL": 50, "REST APIs": 55, "Git": 50, "Problem Solving": 60}, "pref": ["Django/FastAPI", "Testing"], "open": True}]
    ss.cands = make_candidates(18, "Python Developer", 7)
    ss.cand_status = {int(r["id"]): r["Status"] for _, r in ss.cands.iterrows()}
    ss.emp_assess = [{"title": "Python Fundamentals Check", "skills": ["Python", "Problem Solving"], "format": "Quiz + practical", "minutes": 45, "pass": 60}]
    ss.mod = [{"item": "Vacancy: 'Data Entry, earn fast'", "reason": "Possible misleading pay claim", "status": "Open"},
              {"item": "Portfolio: 'Chat app clone'", "reason": "Reported as copied code", "status": "Open"},
              {"item": "Employer profile: Vector Works", "reason": "Verification documents missing", "status": "Open"}]
    ss.cohort = make_cohort(72, 11)
    ss.pool = make_pool(150, 21)
    ss.users = make_admin_users()
    ss.employers = make_admin_employers()
    ss._init = True


def assistant_reply(role: str, q: str) -> str:
    """Rule-based helper. Swap this function for an LLM API call to get free-form answers."""
    ss = st.session_state
    q = q.lower()
    if role == "Job Seeker":
        p, sc, req, demo, r = seeker_ctx()
        gaps = gap_list(demo, req)
        if not ss.quiz and not ss.practical:
            return "Take a few quizzes in Assessments first. Until skills are verified, self-ratings count at half weight, so any advice would be guesswork."
        if "ready" in q or "score" in q:
            return f"Your readiness for {p['career']} is {r:.0f}/100 ({band(r)}) on this rubric. It reflects this framework only, not your overall employability."
        if "job" in q or "match" in q:
            m, j = seeker.ranked_jobs()[0]
            return f"Best current match: {j['title']} at {j['company']} ({m:.0f}% skill match). Open the Job Board for the breakdown."
        if not gaps:
            return "You meet every requirement for this path. Re-test periodically and add portfolio projects."
        return "Focus next on: " + ", ".join(f"{s} (gap {g:.0f})" for s, g in gaps[:3]) + ". The Learning Roadmap has a resource and project for each."
    if role == "Employer":
        top = ss.cands.assign(t=ss.cands[list(ss.vacancies[0]["req"])].mean(axis=1)).sort_values("t", ascending=False).iloc[0]
        return f"Highest assessment average for your first vacancy: {top['Name']}. Treat this as decision support and review portfolios before shortlisting."
    if role == "University":
        g = org._gaps_vs_employers().head(3)["Skill"].tolist()
        return "Largest gaps against employer demand: " + ", ".join(g) + ". See Recommended Projects for curriculum ideas."
    return "Check Moderation for open flags and Users & Employers for pending verifications."


def sidebar() -> str:
    with st.sidebar:
        md('<div class="brand"><i>🌉</i>SkillBridge AI</div>')
        role = st.selectbox("Workspace", list(NAV), format_func=lambda r: ROLE_LABEL[r], key="role")
        pages = {n: (icon, fn) for n, icon, fn in NAV[role]}
        key = f"nav_{role}"
        if key not in st.session_state or st.session_state[key] not in pages:
            st.session_state[key] = list(pages)[0]
        page = st.radio("Navigate", list(pages), key=key, label_visibility="collapsed",
                        format_func=lambda n: f":material/{pages[n][0]}: {n}")
        if role == "Job Seeker":
            md('<div class="pro"><span class="gem"></span><span class="pill"></span><span class="cyl"></span>'
               '<h4>Upgrade to Pro</h4><p>Unlimited assessments and deeper roadmaps</p><span class="rate">PKR 750 / month</span></div>')
            if st.button("Upgrade now", key="upgrade", width="stretch", type="primary"):
                st.toast("Demo build: payments are not connected.")
        st.caption("Demo build · sample data only")
    return role, page, pages[page][1]


def topbar(role: str):
    ss = st.session_state
    c1, c2, c3 = st.columns([4, 1.3, 0.6], vertical_alignment="center")
    with c1:
        st.text_input("Search", key="q", placeholder="Search jobs, candidates, skills", label_visibility="collapsed")
    with c2:
        with st.popover("AI Assistant ✦", width="stretch"):
            st.markdown("**Ask about your results**")
            for i, qq in enumerate(["What should I learn next?", "How ready am I?", "Which jobs fit me?"] if role == "Job Seeker" else ["Summarise my data"]):
                if st.button(qq, key=f"ai_q{i}", width="stretch"):
                    ss.ai_answer = assistant_reply(role, qq)
            free = st.text_input("Or type a question", key="ai_free")
            if free:
                ss.ai_answer = assistant_reply(role, free)
            if ss.get("ai_answer"):
                md(f'<div class="note">{esc(ss.ai_answer)}</div>')
    with c3:
        name = ss.profile["name"] if role == "Job Seeker" else ROLE_LABEL[role]
        initials = "".join(w[0] for w in name.split()[:2]).upper() or "SB"
        md(f'<div class="avatar">{esc(initials)}<b>{len(ss.applied) if role == "Job Seeker" else 3}</b></div>')


init()
role, page, render = sidebar()
topbar(role)
if role == "Job Seeker" and page == "Dashboard":
    st.markdown(f"# Hello, {esc(st.session_state.profile['name'])}")
    md(f'<div class="sub">Your path: {esc(st.session_state.profile["career"])}. Verify skills, close gaps, get matched.</div>')
render()
