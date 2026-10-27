import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

SKILLS = [
    "Python", "Java", "C++", "JavaScript", "TypeScript", "React",
    "Node.js", "SQL", "PostgreSQL", "MongoDB", "Machine Learning",
    "Deep Learning", "Artificial Intelligence", "NLP", "TensorFlow",
    "PyTorch", "Pandas", "NumPy", "Scikit-learn", "Docker",
    "Kubernetes", "AWS", "Azure", "Git", "REST API", "FastAPI",
    "Flask", "Django", "HTML", "CSS", "Data Analysis",
    "Cloud Computing", "Software Engineering", "Data Structures",
    "Algorithms", "API Development", "Database Management", "Linux"
]

SKILL_ALIASES = {
    "Machine Learning": ["ML", "machine learning"],
    "Artificial Intelligence": ["AI", "artificial intelligence"],
    "NLP": ["natural language processing"],
    "REST API": ["RESTful API", "REST APIs"],
    "Node.js": ["NodeJS", "Node JS"],
    "PostgreSQL": ["Postgres"],
    "Scikit-learn": ["sklearn"],
    "JavaScript": ["JS"],
    "TypeScript": ["TS"],
    "Database Management": ["DBMS", "database systems"],
    "Data Structures": ["DSA", "data structures and algorithms"]
}

TRANSFERABLE_SKILLS = {
    "FastAPI": ["Flask", "Django"],
    "Flask": ["FastAPI", "Django"],
    "PostgreSQL": ["SQL", "MongoDB"],
    "React": ["JavaScript", "TypeScript"],
    "Machine Learning": ["Scikit-learn", "TensorFlow", "PyTorch"],
    "Cloud Computing": ["AWS", "Azure"],
    "API Development": ["REST API", "FastAPI", "Flask"]
}

def semantic_similarity(text1, text2):
    if not text1.strip() or not text2.strip():
        return 0.0
    embeddings = model.encode([text1, text2])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(max(0, min(100, float(score) * 100)), 2)

def calculate_similarity(resume_text, job_description):
    return semantic_similarity(resume_text, job_description)

def extract_skills(text):
    found = []
    for skill in SKILLS:
        variations = [skill] + SKILL_ALIASES.get(skill, [])
        if any(re.search(r"(?<!\w)" + re.escape(v) + r"(?!\w)", text, re.IGNORECASE) for v in variations):
            found.append(skill)
    return found

def analyze_skills(resume_text, job_description):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    matched = [s for s in job_skills if s in resume_skills]
    missing = [s for s in job_skills if s not in resume_skills]

    transferable = {}
    for skill in missing[:]:
        related = TRANSFERABLE_SKILLS.get(skill, [])
        found_related = [s for s in related if s in resume_skills]
        if found_related:
            transferable[skill] = found_related

    score = (len(matched) + 0.5 * len(transferable)) / len(job_skills) * 100 if job_skills else 0

    return {
        "resume_skills": resume_skills,
        "job_skills": job_skills,
        "matched": matched,
        "missing": missing,
        "transferable": transferable,
        "score": round(min(100, score), 2)
    }

def extract_education(text):
    degrees = {
        "PhD": [r"\bphd\b", r"\bdoctorate\b", r"\bdoctoral\b"],
        "Master's": [r"\bmaster(?:'s)?\b", r"\bmsc\b", r"\bm\.sc\b", r"\bmtech\b"],
        "Bachelor's": [r"\bbachelor(?:'s)?\b", r"\bbsc\b", r"\bb\.sc\b", r"\bbtech\b", r"\bb\.tech\b", r"\bb\.e\b"]
    }

    found = []
    for degree, patterns in degrees.items():
        if any(re.search(p, text, re.IGNORECASE) for p in patterns):
            found.append(degree)
    return found

def analyze_education(resume_text, job_description):
    resume_degrees = extract_education(resume_text)
    required_degrees = extract_education(job_description)

    levels = {"Bachelor's": 1, "Master's": 2, "PhD": 3}
    candidate_level = max([levels[d] for d in resume_degrees], default=0)
    required_level = min([levels[d] for d in required_degrees], default=0)

    score = 100 if required_level == 0 or candidate_level >= required_level else 0

    return {
        "resume_degrees": resume_degrees,
        "required_degrees": required_degrees,
        "score": score
    }

def extract_experience(text):
    patterns = [
        r"(\d+)\+?\s*years?\s+(?:of\s+)?experience",
        r"minimum\s+(?:of\s+)?(\d+)\s*years?",
        r"at\s+least\s+(\d+)\s*years?"
    ]

    years = []
    for pattern in patterns:
        years.extend(int(x) for x in re.findall(pattern, text.lower()))

    return max(years) if years else 0

def analyze_experience(resume_text, job_description):
    candidate_years = extract_experience(resume_text)
    required_years = extract_experience(job_description)

    internships = len(re.findall(r"\bintern(?:ship)?\b", resume_text, re.IGNORECASE))

    if required_years == 0:
        score = 100
    else:
        score = min(100, (candidate_years + internships * 0.25) / required_years * 100)

    return {
        "candidate_years": candidate_years,
        "required_years": required_years,
        "internships_detected": internships,
        "score": round(score, 2)
    }

def analyze_projects(resume_text, job_description):
    lines = [
        line.strip() for line in resume_text.splitlines()
        if any(word in line.lower() for word in ["project", "developed", "built", "implemented", "designed"])
    ]

    if not lines:
        return {"projects_detected": 0, "score": 0}

    scores = [semantic_similarity(line, job_description) for line in lines]

    return {
        "projects_detected": len(lines),
        "score": round(max(scores), 2)
    }

def analyze_job_titles(resume_text, job_description):
    titles = [
        "Software Engineer", "Software Developer", "Backend Developer",
        "Frontend Developer", "Full Stack Developer", "Data Analyst",
        "Data Scientist", "Machine Learning Engineer", "AI Engineer",
        "Data Engineer", "DevOps Engineer", "Cloud Engineer",
        "Python Developer"
    ]

    resume_titles = [t for t in titles if t.lower() in resume_text.lower()]
    job_titles = [t for t in titles if t.lower() in job_description.lower()]
    matched = [t for t in job_titles if t in resume_titles]

    score = 100 if matched else 0

    return {
        "resume_titles": resume_titles,
        "job_titles": job_titles,
        "matched": matched,
        "score": score
    }

def analyze_resume(resume_text, job_description):
    semantic_score = semantic_similarity(resume_text, job_description)
    skills = analyze_skills(resume_text, job_description)
    education = analyze_education(resume_text, job_description)
    experience = analyze_experience(resume_text, job_description)
    projects = analyze_projects(resume_text, job_description)
    titles = analyze_job_titles(resume_text, job_description)

    overall_score = (
        semantic_score * 0.30 +
        skills["score"] * 0.30 +
        education["score"] * 0.10 +
        experience["score"] * 0.15 +
        projects["score"] * 0.10 +
        titles["score"] * 0.05
    )

    suggestions = []

    if skills["missing"]:
        suggestions.append("Consider developing or demonstrating these skills: " + ", ".join(skills["missing"]))

    if skills["transferable"]:
        suggestions.append("Transferable skills detected: " + str(skills["transferable"]))

    if education["score"] == 0:
        suggestions.append("Review the educational qualifications requested.")

    if experience["score"] < 100:
        suggestions.append("Highlight relevant internships and practical experience.")

    if projects["score"] < 50:
        suggestions.append("Highlight projects related to the job requirements.")

    if semantic_score < 50:
        suggestions.append("Improve the description of relevant experience and technical skills.")

    return {
        "overall_score": round(overall_score, 2),
        "semantic_score": semantic_score,
        "skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "titles": titles,
        "suggestions": suggestions
    }