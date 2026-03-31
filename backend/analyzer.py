from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skills import SKILLS_DB


def extract_skills(text):
    text = text.lower()
    found = []
    for skill in SKILLS_DB:
        if skill.lower() in text:
            found.append(skill)
    return sorted(list(set(found)))


def extract_projects(resume_text):
    lines = resume_text.lower().splitlines()
    project_lines = []

    for line in lines:
        if "-" in line or "project" in line:
            project_lines.append(line.strip())

    return project_lines


def calculate_text_similarity(resume_text, jd_text):
    vectorizer = TfidfVectorizer(stop_words="english")
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
    return round(score * 100, 2)


def calculate_skill_score(resume_skills, jd_skills):
    if not jd_skills:
        return 0
    matched = set(resume_skills).intersection(set(jd_skills))
    return round((len(matched) / len(jd_skills)) * 100, 2)


def detect_project_relevance(projects, jd_text):
    jd_text = jd_text.lower()
    if not projects:
        return 30, ["No visible project details found in resume"]

    relevant = 0
    weak_projects = []

    for project in projects:
        if any(word in jd_text for word in project.split()):
            relevant += 1
        else:
            weak_projects.append(project)

    relevance_score = round((relevant / len(projects)) * 100, 2)
    return relevance_score, weak_projects


def estimate_competition_rate(company_name, jd_text):
    text = f"{company_name} {jd_text}".lower()

    if any(word in text for word in ["google", "microsoft", "amazon", "meta", "product-based"]):
        return "Very High"
    if any(word in text for word in ["tcs", "infosys", "wipro", "accenture", "cognizant"]):
        return "High"
    if any(word in text for word in ["sales", "marketing", "associate", "executive"]):
        return "Medium"
    return "Medium to High"


def infer_cgpa_advice(company_name, jd_text):
    text = f"{company_name} {jd_text}".lower()

    if any(word in text for word in ["google", "microsoft", "amazon", "product", "developer"]):
        return "Aim for 8.0+ CGPA for stronger shortlisting."
    if any(word in text for word in ["tcs", "infosys", "wipro", "service-based"]):
        return "Try to maintain at least 7.0+ CGPA."
    if any(word in text for word in ["sales", "marketing"]):
        return "CGPA matters less than communication, confidence, and consistency."
    return "Maintain the best CGPA possible and strengthen skills/projects."


def suggest_projects(jd_text):
    jd = jd_text.lower()

    if any(word in jd for word in ["data", "analyst", "machine learning"]):
        return [
            "Sales forecasting dashboard using Python and Power BI",
            "Resume-job matching system using NLP",
            "Customer churn prediction project"
        ]
    if any(word in jd for word in ["frontend", "react", "web"]):
        return [
            "Portfolio website with animations and theme switcher",
            "Admin dashboard with charts and authentication",
            "E-commerce frontend with cart and filtering"
        ]
    if any(word in jd for word in ["backend", "api", "node", "database"]):
        return [
            "Authentication API with JWT",
            "Job portal backend with database",
            "Complaint management system with REST APIs"
        ]
    if any(word in jd for word in ["sales", "marketing"]):
        return [
            "Lead management CRM mini project",
            "Customer segmentation dashboard",
            "Sales performance analytics tool"
        ]

    return [
        "Role-specific project aligned with the target job",
        "End-to-end project with measurable results",
        "Project demonstrating problem-solving and business value"
    ]


def generate_preparation_roadmap(missing_skills, weak_projects):
    roadmap = []

    if missing_skills:
        roadmap.append(f"Learn these missing skills first: {', '.join(missing_skills)}")

    if weak_projects:
        roadmap.append("Replace or improve projects that are not aligned with the target role")

    roadmap.append("Customize resume keywords according to the job description")
    roadmap.append("Add measurable impact in projects, such as accuracy, users, or time saved")
    roadmap.append("Practice aptitude, HR questions, and role-specific interview questions")

    return roadmap


def analyze_resume(resume_text, jd_text, company_name):
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)

    matched_skills = sorted(list(set(resume_skills).intersection(set(jd_skills))))
    missing_skills = sorted(list(set(jd_skills) - set(resume_skills)))

    text_score = calculate_text_similarity(resume_text, jd_text)
    skill_score = calculate_skill_score(resume_skills, jd_skills)

    projects = extract_projects(resume_text)
    project_score, weak_projects = detect_project_relevance(projects, jd_text)

    selection_percentage = round(
        (0.45 * skill_score) +
        (0.25 * text_score) +
        (0.30 * project_score), 2
    )

    disadvantages = []

    if missing_skills:
        disadvantages.append("Important job skills are missing in the resume")
    if weak_projects:
        disadvantages.append("Some projects are not aligned with the target role")
    if text_score < 50:
        disadvantages.append("Resume wording is not closely aligned with the job description")
    if selection_percentage < 60:
        disadvantages.append("Overall shortlisting potential is weak right now")

    suggested_skills = missing_skills[:]
    suggested_projects = suggest_projects(jd_text)
    competition_rate = estimate_competition_rate(company_name, jd_text)
    cgpa_advice = infer_cgpa_advice(company_name, jd_text)
    preparation_roadmap = generate_preparation_roadmap(missing_skills, weak_projects)

    return {
        "company_name": company_name,
        "selection_percentage": selection_percentage,
        "competition_rate": competition_rate,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "weak_projects": weak_projects,
        "disadvantages": disadvantages,
        "suggested_skills": suggested_skills,
        "suggested_projects": suggested_projects,
        "cgpa_advice": cgpa_advice,
        "preparation_roadmap": preparation_roadmap,
        "text_score": text_score,
        "skill_score": skill_score,
        "project_score": project_score
    }