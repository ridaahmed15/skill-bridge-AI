"""Scoring and analysis logic. Transparent, rule-based, and easy to swap for an LLM later."""
from __future__ import annotations

import io
import re
import zipfile

from data import ALL_SKILLS, CAREERS, PRACTICAL, QUIZ, SKILL_ALIASES, coverage  # noqa: F401


def read_cv_text(uploaded) -> str:
    name, raw = uploaded.name.lower(), uploaded.getvalue()
    try:
        if name.endswith(".pdf"):
            try:
                from pypdf import PdfReader
            except ImportError:
                return ""
            return "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(raw)).pages)
        if name.endswith(".docx"):
            with zipfile.ZipFile(io.BytesIO(raw)) as z:
                xml = z.read("word/document.xml").decode("utf8", "ignore")
            return re.sub(r"<[^>]+>", " ", xml)
        return raw.decode("utf8", "ignore")
    except Exception:
        return ""


def detect_skills(text: str) -> list[str]:
    t = text.lower()
    found = []
    for skill, aliases in SKILL_ALIASES.items():
        if any(re.search(r"(?<![a-z])" + re.escape(a) + r"(?![a-z])", t) for a in aliases):
            found.append(skill)
    return found


def detect_years(text: str) -> int:
    m = re.findall(r"(\d{1,2})\+?\s*(?:years?|yrs?)", text.lower())
    return max(map(int, m)) if m else 0


def score_quiz(skill: str, chosen: list) -> float:
    qs = QUIZ[skill]
    right = sum(1 for (_, _, ans), c in zip(qs, chosen) if c == ans)
    return round(100 * right / len(qs))


def score_practical(career: str, text: str):
    """Keyword rubric: a transparent heuristic. Replace with LLM or human review in production."""
    words = len(text.split())
    rubric = PRACTICAL[career]["rubric"]
    t = text.lower()
    hits = [(label, any(k in t for k in kws)) for label, kws in rubric]
    if words < 40:
        return 0, [(label, False) for label, _ in rubric], words
    return round(100 * sum(h for _, h in hits) / len(hits)), hits, words


def skill_scores(profile: dict, quiz: dict, practical: dict) -> dict:
    """Per skill: value 0-100 and status. Self-ratings count at half weight until verified."""
    out = {}
    for s in ALL_SKILLS:
        q = quiz.get(s)
        ps = [pr["score"] for c, pr in practical.items() if s in PRACTICAL[c]["skills"]]
        p = max(ps) if ps else None
        if q is not None and p is not None:
            out[s] = {"value": 0.6 * q + 0.4 * p, "status": "Verified"}
        elif q is not None:
            out[s] = {"value": q, "status": "Verified"}
        elif p is not None:
            out[s] = {"value": p, "status": "Verified"}
        elif s in profile.get("self", {}):
            out[s] = {"value": profile["self"][s] * 0.5, "status": "Self-rated"}
        else:
            out[s] = {"value": 0, "status": "Not assessed"}
    return out


def readiness(values: dict, req: dict) -> float:
    return coverage(values, req) * 100


def band(score: float) -> str:
    if score < 40:
        return "Getting started"
    if score < 65:
        return "Building skills"
    if score < 85:
        return "Approaching the role rubric"
    return "Meets the role rubric"


def gap_list(values: dict, req: dict) -> list[tuple[str, float]]:
    gaps = [(s, req[s] - values.get(s, 0)) for s in req if values.get(s, 0) < req[s]]
    return sorted(gaps, key=lambda x: -x[1])


def job_match(job: dict, scores: dict) -> float:
    return coverage({s: v["value"] for s, v in scores.items()}, job["req"]) * 100
