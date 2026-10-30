"""Sample data + synthetic generators for SkillBridge AI (demo only)."""
from __future__ import annotations

import random
import pandas as pd

CITIES = ["Karachi", "Lahore", "Islamabad", "Remote"]

# career -> {skill: required level (0-100)}
CAREERS = {
    "Python Developer": {"Python": 80, "OOP": 70, "Git": 65, "SQL": 60, "REST APIs": 70,
                         "Testing": 55, "Django/FastAPI": 65, "Problem Solving": 75},
    "Data Analyst": {"Python": 70, "Pandas": 80, "SQL": 80, "Data Visualization": 70,
                     "Statistics": 65, "Excel": 55, "Analytical Reasoning": 75, "Communication": 60},
    "Machine Learning Engineer": {"Python": 80, "Statistics": 70, "scikit-learn": 75, "Deep Learning": 60,
                                  "Data Preprocessing": 70, "Model Deployment": 55, "SQL": 50, "Git": 55},
}
ALL_SKILLS = sorted({s for c in CAREERS.values() for s in c})

SKILL_ALIASES = {
    "Python": ["python"], "OOP": ["oop", "object oriented", "object-oriented"], "Git": ["git", "github", "gitlab"],
    "SQL": ["sql", "mysql", "postgresql", "postgres", "sqlite"], "REST APIs": ["rest", "api", "apis", "restful"],
    "Testing": ["pytest", "unittest", "testing", "tdd"], "Django/FastAPI": ["django", "fastapi", "flask"],
    "Problem Solving": ["problem solving", "algorithms", "data structures", "leetcode"],
    "Pandas": ["pandas", "numpy"], "Data Visualization": ["matplotlib", "seaborn", "plotly", "power bi", "tableau", "visualization", "visualisation"],
    "Statistics": ["statistics", "statistical", "hypothesis testing"], "Excel": ["excel", "spreadsheet", "vlookup"],
    "Analytical Reasoning": ["analytical", "analysis", "analytics"], "Communication": ["communication", "presentation", "presenting"],
    "scikit-learn": ["scikit-learn", "sklearn", "machine learning"], "Deep Learning": ["tensorflow", "pytorch", "keras", "deep learning", "neural"],
    "Data Preprocessing": ["preprocessing", "data cleaning", "feature engineering"], "Model Deployment": ["deployment", "mlops", "docker", "streamlit"],
}

# skill -> list of (question, options, correct index)
QUIZ = {
    "Python": [("What does len({1, 2, 2, 3}) return?", ["4", "3", "2", "Error"], 1),
               ("Which pattern guarantees a file is closed after use?", ["f = open('a.txt')", "with open('a.txt') as f:", "open('a.txt').close", "file('a.txt')"], 1)],
    "OOP": [("What does inheritance let a class do?", ["Reuse and extend a parent class's behaviour", "Hide every attribute", "Run faster", "Avoid defining methods"], 0)],
    "Git": [("Which command records staged changes in history?", ["git push", "git commit", "git fetch", "git stash"], 1)],
    "SQL": [("Which clause filters rows AFTER grouping?", ["WHERE", "HAVING", "ORDER BY", "LIMIT"], 1),
            ("Which JOIN keeps every row of the left table even with no match?", ["INNER JOIN", "LEFT JOIN", "CROSS JOIN", "NATURAL JOIN"], 1)],
    "REST APIs": [("Which HTTP status code means a resource was created?", ["200", "201", "204", "301"], 1)],
    "Testing": [("What is the main purpose of a unit test?", ["Verify a small piece of code in isolation", "Test the system with real users", "Measure server load", "Check UI colours"], 0)],
    "Django/FastAPI": [("In FastAPI, what is commonly used to validate request bodies?", ["Pydantic models", "Jinja templates", "CSS selectors", "Cron jobs"], 0)],
    "Problem Solving": [("A sorted list holds 1,000,000 numbers. Fastest way to check if x exists?", ["Linear scan", "Binary search", "Sort again, then scan", "Nested loops"], 1)],
    "Pandas": [("Which call returns the mean salary per department?", ["df.groupby('dept')['salary'].mean()", "df.mean('dept')", "df.salary.dept.mean()", "df['salary'].groupby.mean"], 0),
               ("Which method drops rows containing missing values?", ["df.dropna()", "df.remove_nan()", "df.clean()", "df.fillna(None)"], 0)],
    "Data Visualization": [("Best chart for showing a trend over time?", ["Pie chart", "Line chart", "Word cloud", "Treemap"], 1)],
    "Statistics": [("Which measure is least affected by outliers?", ["Mean", "Median", "Range", "Standard deviation"], 1)],
    "Excel": [("Which function returns a value from another column of a table by lookup?", ["VLOOKUP", "SUMIF", "CONCAT", "ROUND"], 0)],
    "Analytical Reasoning": [("Signups rose 20% but revenue stayed flat. Best first step?", ["Ignore it", "Segment revenue by plan and user cohort", "Double ad spend", "Drop the revenue metric"], 1)],
    "Communication": [("You must present findings to a non-technical manager. Start with:", ["The code", "The conclusion and the action it implies", "The list of libraries", "Raw data"], 1)],
    "scikit-learn": [("Why split data into train and test sets?", ["Estimate performance on unseen data", "Make training faster", "Remove outliers", "Balance classes"], 0)],
    "Deep Learning": [("What does an activation function such as ReLU add to a network?", ["Non-linearity", "More data", "Disk speed", "Labels"], 0)],
    "Data Preprocessing": [("Why scale features before k-nearest neighbours?", ["Distances depend on feature ranges", "It removes rows", "It removes labels", "It encrypts data"], 0)],
    "Model Deployment": [("A sensible way to serve a trained model to a web app?", ["Wrap it in an API endpoint", "Email the pickle file", "Retrain on every request", "Embed it in CSS"], 0)],
}

PRACTICAL = {
    "Python Developer": {
        "title": "Design a task-management API",
        "prompt": "Describe (or paste code/pseudo-code for) a small REST API for a to-do list: endpoints, input validation, storage, error handling and tests. Aim for 60+ words.",
        "skills": ["REST APIs", "Testing", "Problem Solving"],
        "rubric": [("Defines CRUD endpoints", ["get", "post", "put", "delete", "endpoint"]),
                   ("Validates input", ["validate", "pydantic", "serializer", "schema"]),
                   ("Persists data in a database", ["database", "postgres", "sqlite", "orm", "model"]),
                   ("Handles errors with status codes", ["404", "400", "status code", "exception", "error"]),
                   ("Includes automated tests", ["pytest", "unittest", "test"])],
    },
    "Data Analyst": {
        "title": "Investigate a revenue drop",
        "prompt": "Explain how you would analyse a CSV of monthly sales to find why revenue dropped: cleaning, analysis, chart and recommendation. Aim for 60+ words.",
        "skills": ["Pandas", "Data Visualization", "Analytical Reasoning", "Communication"],
        "rubric": [("Cleans the data", ["missing", "duplicate", "clean", "null", "dropna"]),
                   ("Aggregates correctly", ["groupby", "pivot", "aggregate", "sum", "mean"]),
                   ("Visualises the result", ["chart", "plot", "visual", "matplotlib", "line"]),
                   ("Segments to find the cause", ["segment", "region", "product", "compare", "trend"]),
                   ("Ends with a recommendation", ["recommend", "action", "suggest", "next step"])],
    },
    "Machine Learning Engineer": {
        "title": "Plan a customer-churn model",
        "prompt": "Describe how you would build and ship a model that predicts customer churn: data prep, split, model, metrics and deployment. Aim for 60+ words.",
        "skills": ["Data Preprocessing", "scikit-learn", "Model Deployment"],
        "rubric": [("Prepares the data", ["missing", "encode", "scale", "clean", "feature"]),
                   ("Splits train/test", ["train", "test", "split", "cross-validation"]),
                   ("Chooses and justifies a model", ["logistic", "random forest", "gradient", "model"]),
                   ("Uses suitable metrics", ["precision", "recall", "f1", "auc", "accuracy"]),
                   ("Plans deployment/monitoring", ["api", "deploy", "fastapi", "streamlit", "monitor"])],
    },
}

RESOURCES = {
    "Python": [("Official Python Tutorial", "Docs", 10, "https://docs.python.org/3/tutorial/")],
    "OOP": [("Classes in the Python Tutorial", "Docs", 3, "https://docs.python.org/3/tutorial/classes.html")],
    "Git": [("Pro Git (free book)", "Book", 8, "https://git-scm.com/book/en/v2")],
    "SQL": [("SQL practice with SQLite", "Practice", 8, "")],
    "REST APIs": [("FastAPI Tutorial", "Docs", 6, "https://fastapi.tiangolo.com/tutorial/")],
    "Testing": [("pytest Getting Started", "Docs", 3, "https://docs.pytest.org/en/stable/getting-started.html")],
    "Django/FastAPI": [("Django Tutorial, parts 1-4", "Docs", 8, "https://docs.djangoproject.com/en/stable/intro/tutorial01/")],
    "Problem Solving": [("30 algorithm drills (arrays, hashing, search)", "Practice", 12, "")],
    "Pandas": [("10 Minutes to pandas", "Docs", 3, "https://pandas.pydata.org/docs/user_guide/10min.html")],
    "Data Visualization": [("Matplotlib user guide", "Docs", 5, "https://matplotlib.org/stable/users/index.html")],
    "Statistics": [("Descriptive stats + hypothesis testing refresher", "Course", 10, "")],
    "Excel": [("Lookup, pivot tables and charts workout", "Practice", 5, "")],
    "Analytical Reasoning": [("Case drills: metric moves and root causes", "Practice", 6, "")],
    "Communication": [("Present one insight in 3 minutes (record yourself)", "Practice", 2, "")],
    "scikit-learn": [("scikit-learn User Guide", "Docs", 10, "https://scikit-learn.org/stable/user_guide.html")],
    "Deep Learning": [("Neural-network basics with a small image dataset", "Course", 12, "")],
    "Data Preprocessing": [("Cleaning, encoding and scaling pipelines", "Practice", 6, "")],
    "Model Deployment": [("Serve a model with FastAPI or Streamlit", "Practice", 5, "")],
}

PROJECTS = {
    "Python": "CLI expense tracker with file storage and unit tests",
    "OOP": "Library management system using classes and inheritance",
    "Git": "Open a pull request to a small open-source repo",
    "SQL": "Design a normalised shop schema and write 10 reporting queries",
    "REST APIs": "Task-manager REST API with auth and pagination",
    "Testing": "Add 80% test coverage to one of your existing projects",
    "Django/FastAPI": "Student results portal in Django with PostgreSQL",
    "Problem Solving": "Solve and write up 20 problems with complexity notes",
    "Pandas": "Clean and analyse a public dataset into a short notebook",
    "Data Visualization": "Interactive sales dashboard with filters",
    "Statistics": "A/B test analysis with confidence intervals",
    "Excel": "Monthly budget model with pivot tables and charts",
    "Analytical Reasoning": "Written case study: why did metric X change?",
    "Communication": "5-slide insight deck for a non-technical audience",
    "scikit-learn": "House-price or churn prediction with model comparison",
    "Deep Learning": "Image classifier with a documented training run",
    "Data Preprocessing": "Reusable preprocessing pipeline for messy CSVs",
    "Model Deployment": "Deploy a trained model behind an API with a demo UI",
}

JOBS = [
    dict(id=1, title="Junior Python Developer", company="Indus Software House", city="Karachi", type="Full-time", pay="PKR 90k-130k",
         req={"Python": 65, "SQL": 50, "REST APIs": 55, "Git": 50, "Problem Solving": 60}),
    dict(id=2, title="Backend Intern (Django)", company="Harbor Tech Labs", city="Karachi", type="Internship", pay="PKR 30k-45k",
         req={"Python": 55, "Django/FastAPI": 50, "Git": 45, "SQL": 40}),
    dict(id=3, title="Data Analyst", company="Clifton Analytics", city="Karachi", type="Full-time", pay="PKR 110k-160k",
         req={"SQL": 70, "Pandas": 65, "Data Visualization": 60, "Excel": 50, "Analytical Reasoning": 60}),
    dict(id=4, title="Junior Data Analyst", company="Meridian Insights", city="Remote", type="Full-time", pay="PKR 80k-120k",
         req={"Python": 55, "Pandas": 60, "Statistics": 50, "Communication": 50}),
    dict(id=5, title="ML Engineer Intern", company="Neural Nest", city="Lahore", type="Internship", pay="PKR 40k-60k",
         req={"Python": 65, "scikit-learn": 55, "Data Preprocessing": 55, "Statistics": 50}),
    dict(id=6, title="FastAPI Developer", company="Port City Fintech", city="Karachi", type="Full-time", pay="PKR 140k-200k",
         req={"Python": 75, "Django/FastAPI": 70, "REST APIs": 70, "SQL": 60, "Testing": 55}),
    dict(id=7, title="BI Reporting Analyst", company="Saffron Retail Group", city="Islamabad", type="Full-time", pay="PKR 100k-140k",
         req={"Excel": 70, "SQL": 65, "Data Visualization": 65, "Communication": 60}),
    dict(id=8, title="Junior ML Engineer", company="Vector Works", city="Remote", type="Full-time", pay="PKR 150k-220k",
         req={"Python": 75, "scikit-learn": 70, "Deep Learning": 50, "Model Deployment": 50, "Git": 50}),
]

_FIRST = ["Ayesha", "Hamza", "Fatima", "Ali", "Sana", "Usman", "Zainab", "Bilal", "Hira", "Danish", "Maryam", "Faisal",
          "Noor", "Saad", "Iqra", "Talha", "Areeba", "Omar", "Mahnoor", "Rayyan", "Kiran", "Adeel"]
_LAST = ["Khan", "Ahmed", "Siddiqui", "Malik", "Qureshi", "Ansari", "Shaikh", "Raza", "Baig", "Memon"]
_UNIS = ["University A", "University B", "University C", "University D", "Institute E"]
STATUSES = ["Applied", "Assessed", "Shortlisted", "Interview", "Offer", "Rejected"]


def _clip(x: float) -> int:
    return int(max(5, min(98, x)))


def make_candidates(n: int, career: str, seed: int) -> pd.DataFrame:
    rng = random.Random(seed)
    rows, used = [], set()
    for i in range(1, n + 1):
        while True:
            name = f"{rng.choice(_FIRST)} {rng.choice(_LAST)}"
            if name not in used:
                used.add(name)
                break
        ability = rng.gauss(60, 14)
        row = {"id": i, "Name": name, "University": rng.choice(_UNIS), "City": rng.choice(CITIES),
               "Experience (yrs)": rng.choice([0, 0, 1, 1, 2, 3]), "Projects": rng.randint(0, 6),
               "Status": rng.choices(STATUSES, weights=[4, 5, 3, 2, 1, 3])[0]}
        for s in ALL_SKILLS:
            boost = 8 if s in CAREERS[career] else -8
            row[s] = _clip(ability + boost + rng.gauss(0, 12))
        rows.append(row)
    return pd.DataFrame(rows)


def make_pool(n: int, seed: int) -> pd.DataFrame:
    rng = random.Random(seed)
    rows = []
    for i in range(n):
        goal = rng.choice(list(CAREERS))
        ability = rng.gauss(58, 15)
        row = {"City": rng.choices(CITIES, weights=[5, 3, 2, 2])[0], "Career goal": goal}
        for s in ALL_SKILLS:
            row[s] = _clip(ability + (6 if s in CAREERS[goal] else -10) + rng.gauss(0, 12))
        rows.append(row)
    return pd.DataFrame(rows)


def coverage(values: dict, req: dict) -> float:
    tot = sum(req.values())
    return sum(w * min(values.get(s, 0) / w, 1) for s, w in req.items()) / tot if tot else 0.0


def make_cohort(n: int, seed: int) -> pd.DataFrame:
    rng = random.Random(seed)
    rows = []
    for i in range(1, n + 1):
        program = rng.choice(["BS Computer Science", "BS Software Engineering", "BS Data Science"])
        track = rng.choice(list(CAREERS))
        sem = rng.randint(1, 8)
        ability = 30 + sem * 4.5 + rng.gauss(0, 10)
        row = {"Student": f"S-{i:03d}", "Program": program, "Semester": sem, "Track": track}
        for s in ALL_SKILLS:
            # typical curriculum gaps: weak on testing, deployment, communication
            penalty = 14 if s in ("Testing", "Model Deployment", "Communication", "Git", "REST APIs") else 0
            row[s] = _clip(ability - penalty + rng.gauss(0, 10))
        row["Readiness"] = round(coverage({s: row[s] for s in CAREERS[track]}, CAREERS[track]) * 100)
        row["Projects"] = max(0, int(sem / 2 + rng.gauss(0, 1.2)))
        row["Assessments done"] = rng.randint(1, 8)
        rows.append(row)
    return pd.DataFrame(rows)


def employer_demand() -> dict:
    acc: dict[str, list[int]] = {}
    for j in JOBS:
        for s, lvl in j["req"].items():
            acc.setdefault(s, []).append(lvl)
    return {s: round(sum(v) / len(v)) for s, v in acc.items()}


def make_admin_users() -> pd.DataFrame:
    rng = random.Random(3)
    rows = []
    for i in range(1, 13):
        rows.append({"ID": f"U-{i:03d}", "Name": f"{rng.choice(_FIRST)} {rng.choice(_LAST)}",
                     "Type": rng.choice(["Job seeker", "Job seeker", "Student"]), "City": rng.choice(CITIES),
                     "Status": rng.choice(["Active", "Active", "Active", "Suspended"])})
    return pd.DataFrame(rows)


def make_admin_employers() -> pd.DataFrame:
    names = ["Indus Software House", "Harbor Tech Labs", "Clifton Analytics", "Meridian Insights",
             "Neural Nest", "Port City Fintech", "Saffron Retail Group", "Vector Works"]
    rng = random.Random(5)
    return pd.DataFrame([{"Company": n, "City": JOBS[i]["city"], "Plan": rng.choice(["Free", "Subscription", "Per-vacancy"]),
                          "Open vacancies": rng.randint(0, 4), "Status": rng.choice(["Verified", "Verified", "Pending review"])}
                         for i, n in enumerate(names)])
