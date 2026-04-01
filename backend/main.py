from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Backend running"}


@app.post("/analyze")
async def analyze(
    job_description: str = Form(...),
    resume: UploadFile = File(...)
):
    try:
        # 🔥 PDF ko text me convert karne ka basic trick
        content = await resume.read()

        try:
            text = content.decode("latin-1").lower()
        except:
            return {"error": "PDF read nahi ho pa raha"}

        jd = job_description.lower()

        skills = [
            "python","java","c++","javascript","react","node","mongodb",
            "sql","mysql","machine learning","deep learning",
            "pandas","numpy","excel","power bi","git","github"
        ]

        resume_skills = [s for s in skills if s in text]
        jd_skills = [s for s in skills if s in jd]

        matched = [s for s in jd_skills if s in resume_skills]
        missing = [s for s in jd_skills if s not in resume_skills]

        score = int((len(matched) / len(jd_skills)) * 100) if jd_skills else 0

        return {
            "score": score,
            "chance": "High" if score > 70 else "Medium" if score > 40 else "Low",
            "matched": matched,
            "missing": missing
        }

    except Exception as e:
        return {"error": str(e)}