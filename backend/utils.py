import pdfplumber
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def extract_text_from_pdf(file_path):
    import pdfplumber

    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t

    return text.strip()


def generate_report_pdf(report_path, result):
    c = canvas.Canvas(report_path, pagesize=A4)
    width, height = A4

    y = height - 50
    line_gap = 18

    lines = [
        "AI Placement Readiness Report",
        "",
        f"Company Name: {result.get('company_name', '')}",
        f"Selection Percentage: {result.get('selection_percentage', 0)}%",
        f"Competition Rate: {result.get('competition_rate', '')}",
        "",
        f"Matched Skills: {', '.join(result.get('matched_skills', []))}",
        f"Missing Skills: {', '.join(result.get('missing_skills', []))}",
        "",
        f"Disadvantages: {', '.join(result.get('disadvantages', []))}",
        "",
        f"Suggested Skills: {', '.join(result.get('suggested_skills', []))}",
        f"Suggested Projects: {', '.join(result.get('suggested_projects', []))}",
        "",
        f"CGPA Advice: {result.get('cgpa_advice', '')}",
        "",
        "Preparation Roadmap:",
    ]

    for step in result.get("preparation_roadmap", []):
        lines.append(f"- {step}")

    for line in lines:
        c.drawString(40, y, line[:110])
        y -= line_gap
        if y < 60:
            c.showPage()
            y = height - 50

    c.save()