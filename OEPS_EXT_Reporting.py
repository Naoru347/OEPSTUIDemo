import json
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

DATA_FILE = "OEPS_data.json"
OUTPUT_PDF = "EAP_Requirements_Report.pdf"

def load_data():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def determine_eap_requirement(total_score):
    if total_score < 2:
        return "EAP 6016 Required"
    else:
        return "No EAP Required"

def compile_student_list(data):
    student_list = []
    one_year_ago = datetime.now() - timedelta(days=365)
    for entry in data:
        assessment_date = datetime.fromisoformat(entry['date'])
        if assessment_date >= one_year_ago:
            student_name = entry['student']
            total_score = entry['total score']
            eap_requirement = determine_eap_requirement(total_score)
            student_list.append([student_name, eap_requirement])
    return sorted(student_list, key=lambda x: x[1])  # Sort by EAP requirement

def create_pdf_report(student_list):
    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=letter)
    elements = []

    # Add title
    styles = getSampleStyleSheet()
    elements.append(Paragraph("EAP Requirements Report", styles['Title']))

    # Create table
    table_data = [['Student Name', 'EAP Requirement']] + student_list
    table = Table(table_data)

    # Add style to table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('TOPPADDING', (0, 1), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ])

    # Add color coding based on EAP requirement
    for i in range(1, len(table_data)):
        if table_data[i][1] == "EAP 6016 Required":
            style.add('BACKGROUND', (0, i), (-1, i), colors.lightpink)
        else:
            style.add('BACKGROUND', (0, i), (-1, i), colors.lightgreen)

    table.setStyle(style)
    elements.append(table)

    # Build PDF
    doc.build(elements)

def main():
    data = load_data()
    student_list = compile_student_list(data)
    create_pdf_report(student_list)
    print(f"Report generated: {OUTPUT_PDF}")

if __name__ == "__main__":
    main()
