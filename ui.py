from __future__ import annotations

import html

import plotly.graph_objects as go
import streamlit as st

from data import CAREERS
from logic import gap_list, readiness, skill_scores

PALETTE = ["#8B4DFF", "#06D6A0", "#F7BE0B", "#FF7A1A", "#1B5CFF", "#F59AF4"]
BAR_COLORS = ["#06D6A0", "#8B4DFF", "#F7BE0B", "#FF7A1A", "#1B5CFF"]


def esc(x) -> str:
    return html.escape(str(x))


def H(s: str) -> str:
    """Collapse indented HTML so Markdown never treats it as a code block."""
    return "".join(line.strip() for line in s.strip().splitlines())


def md(s: str):
    st.markdown(H(s), unsafe_allow_html=True)


def bar(label: str, pct: float, color: str = "#06D6A0") -> str:
    pct = max(0, min(100, pct))
    return (f'<div class="barrow"><div class="barhead"><span>{esc(label)}</span><span>{pct:.0f}%</span></div>'
            f'<div class="track"><div class="fill" style="width:{pct:.0f}%;background:{color}"></div></div></div>')


def spark(vals, w=150, h=60) -> str:
    vals = list(vals)
    if len(vals) < 2:
        vals = [vals[0] if vals else 0] * 2
    mx = max(max(vals), 1)
    step = w / (len(vals) - 1)
    pts = [(i * step, h - 6 - (v / mx) * (h - 14)) for i, v in enumerate(vals)]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    area = f"0,{h} {line} {w},{h}"
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><linearGradient id="sg" x1="0" x2="0" y1="0" y2="1">'
            '<stop offset="0" stop-color="#FF7A1A" stop-opacity=".35"/><stop offset="1" stop-color="#FF7A1A" stop-opacity="0"/>'
            f'</linearGradient></defs><polygon points="{area}" fill="url(#sg)"/>'
            f'<polyline points="{line}" fill="none" stroke="#FF7A1A" stroke-width="2.5" stroke-linejoin="round"/></svg>')


def style_fig(fig, h: int = 340):
    fig.update_layout(height=h, margin=dict(l=10, r=10, t=30, b=10), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", colorway=PALETTE,
                      font=dict(family="Plus Jakarta Sans, Segoe UI, sans-serif", color="#0E0E12"),
                      legend=dict(orientation="h", y=-0.18))
    return fig


def radar(series: dict, skills: list[str], h: int = 380):
    fig = go.Figure()
    for i, (name, vals) in enumerate(series.items()):
        fig.add_trace(go.Scatterpolar(r=list(vals) + [vals[0]], theta=skills + [skills[0]], fill="toself", name=name,
                                      line=dict(color=PALETTE[i % len(PALETTE)], width=3), opacity=.75))
    fig.update_layout(polar=dict(radialaxis=dict(range=[0, 100], gridcolor="#E7E9F3"), angularaxis=dict(gridcolor="#E7E9F3")))
    return style_fig(fig, h)


def section(title: str, link_html: str = ""):
    md(f'<div class="sec"><span>{esc(title)}</span>{link_html}</div>')


def page_head(title: str, sub: str = ""):
    st.markdown(f"# {title}")
    if sub:
        md(f'<div class="sub">{esc(sub)}</div>')


def go_page(role: str, page: str):
    st.session_state[f"nav_{role}"] = page


def toggle_done(key: str):
    d = st.session_state.done
    d.symmetric_difference_update({key})


def seeker_ctx():
    ss = st.session_state
    p = ss.profile
    req = CAREERS[p["career"]]
    sc = skill_scores(p, ss.quiz, ss.practical)
    demo = {s: sc[s]["value"] for s in req}
    r = readiness(demo, req)
    return p, sc, req, demo, r


def learning_plan():
    """Ordered list of (skill, gap, resource tuple, project) for the current career."""
    from data import PROJECTS, RESOURCES
    p, sc, req, demo, r = seeker_ctx()
    plan = []
    for s, g in gap_list(demo, req):
        res = RESOURCES[s][0]
        plan.append((s, g, res, PROJECTS[s]))
    return plan
