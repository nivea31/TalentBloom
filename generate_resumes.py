import pandas as pd
from fpdf import FPDF
import os

df = pd.read_csv("form_data.csv")

os.makedirs("resumes", exist_ok=True)

def generate_resume(row, index):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, str(row['name']), ln=True)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Email: {row['email']}", ln=True)
    pdf.cell(0, 10, f"Phone: {row['phone']}", ln=True)
    pdf.cell(0, 10, f"Age: {row['age']}", ln=True)
    pdf.cell(0, 10, f"Education: {row['education']}", ln=True)
    pdf.cell(0, 10, f"Experience: {row['experience']} years", ln=True)
    pdf.cell(0, 10, f"Industry: {row['industry']}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Skills:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, str(row['skills']))

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Projects:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, str(row['projects']))

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "LinkedIn:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, str(row['linkedin']))

    pdf.ln(2)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "GitHub:", ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, str(row['github']))

    filename = f"resume_{index+1}_{str(row['name']).replace(' ', '_')}.pdf"
    filepath = os.path.join("resumes", filename)
    pdf.output(filepath)

    return filename
df['resume'] = [generate_resume(row, idx) for idx, row in df.iterrows()]

df.to_csv("form_data.csv", index=False)
print(" Resumes generated and saved in 'resumes/' folder.")
