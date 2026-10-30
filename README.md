# SkillBridge AI: Streamlit dashboard (demo build)

Interactive dashboard for the SkillBridge AI concept. All data is **sample data**; nothing leaves your machine.

## Run it (needs Python 3.10+)

**Windows:** double-click `run.bat`
**macOS / Linux:** `./run.sh` (if blocked: `chmod +x run.sh`)
**Manual:** `pip install -r requirements.txt` then `streamlit run app.py`

The browser opens at http://localhost:8501.

### Roman Urdu
1. Zip ko extract karein.
2. Windows par `run.bat` double-click karein; Mac/Linux par terminal mein `./run.sh` chalayein.
3. Pehli baar libraries install hongi (1-2 minute), phir browser mein app khul jayegi.
4. Agar chalane mein masla ho: terminal mein `pip install -r requirements.txt` phir `streamlit run app.py`.

## What's inside (4 workspaces, switch from the sidebar)

| Workspace | Pages |
|---|---|
| Student / Job seeker | Dashboard, Profile & CV, Assessments (quizzes + practical task), Skill-Gap Report, Learning Roadmap, Portfolio, Job Board |
| Employer | Overview, Vacancies (required/preferred skills), Assessments builder, Candidates (compare, shortlist), Recruitment Performance, Skills Intelligence |
| University / Institute | Overview, Skill Assessment, Skill Gaps vs Employers, Student Progress, Recommended Projects, Reports |
| Admin | Overview, Users & Employers, Assessment Management, Moderation, Analytics |

Try this flow first: **Job Seeker > Assessments** (answer a few quizzes, submit the practical task) > **Skill-Gap Report** > **Learning Roadmap** > **Job Board**.

## How scoring works (kept transparent on purpose)
- Verified skill score = quiz result, blended 60/40 with the practical task when both exist.
- Self-ratings and CV-detected skills count at **half weight** until verified.
- Career Readiness Score = requirement-weighted coverage of the role rubric. It is shown as performance against a framework, not a measure of worth or employability.
- Employers see decision support only; shortlisting is always a manual action.
- Aggregated views hide groups smaller than 5 people.

## Files
- `app.py` shell, navigation, AI assistant | `pages_seeker.py`, `pages_org.py` pages
- `data.py` careers, question banks, jobs, sample data | `logic.py` scoring and CV parsing
- `styles.py` all CSS | `.streamlit/config.toml` theme

## Next steps for production
- Replace `assistant_reply()` in `app.py` with a language-model API call.
- Replace the keyword rubric in `logic.score_practical()` with model or human review.
- Move session state to PostgreSQL and add real authentication with role-based access.
- Add questions by extending `QUIZ` in `data.py`.
"# skill-bridge-AI" 
