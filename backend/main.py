import os
import urllib.parse

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from analyzer import analyze_resume
from utils import extract_text_from_pdf, generate_report_pdf
from database import reports_collection

app = FastAPI()

# ================= CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= FOLDERS =================
UPLOAD_DIR = "uploads"
REPORT_DIR = "reports"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


# ================= ROOT =================
@app.get("/")
def home():
    return {"message": "Backend running"}


# ================= ADMIN =================
@app.get("/admin")
def admin_data():
    data = list(reports_collection.find({}, {"_id": 0}))
    return data


# ================= DOWNLOAD REPORT =================
@app.get("/reports/{file_name}")
def get_report(file_name: str):
    file_path = os.path.join(REPORT_DIR, file_name)

    if not os.path.exists(file_path):
        return {"error": "Report not found"}

    return FileResponse(
        file_path,
        media_type="application/pdf",
        filename=file_name
    )


# ================= ANALYZE =================
@app.post("/analyze")
async def analyze(
    company_name: str = Form(...),
    job_description: str = Form(...),
    user_email: str = Form(...),
    resume: UploadFile = File(...)
):
    try:
        # 🔹 Save Resume
        file_path = os.path.join(UPLOAD_DIR, resume.filename)
        with open(file_path, "wb") as f:
            f.write(await resume.read())

        # 🔹 Extract Text
        text = extract_text_from_pdf(file_path)

        print("\n========== DEBUG ==========")
        print("RESUME TEXT:", text[:300])
        print("JD TEXT:", job_description[:300])

        if not text.strip():
            return {"error": "Resume text not extracted. Use text-based PDF."}

        # 🔹 Analyze
        result = analyze_resume(text, job_description, company_name)

        # 🔹 Add user email
        result["user_email"] = user_email

        # 🔥 FIX: REMOVE DOUBLE .PDF
        base_name = resume.filename.replace(".pdf", "").replace(" ", "_")
        report_name = f"{base_name}.pdf"

        report_path = os.path.join(REPORT_DIR, report_name)

        # 🔹 Generate PDF
        generate_report_pdf(report_path, result)

        print("PDF SAVED AT:", report_path)

        # 🔥 SAFE URL (spaces fix)
        safe_name = urllib.parse.quote(report_name)
        result["report_download_path"] = f"/reports/{safe_name}"

        # 🔹 Save to DB
        inserted = reports_collection.insert_one(result)
        result["_id"] = str(inserted.inserted_id)

        return result

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}