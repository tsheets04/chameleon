from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

def render(filename, data):
    """
    Ethan's specific high-density layout.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=35, leftMargin=35, topMargin=35, bottomMargin=35)
    styles = getSampleStyleSheet()
    story = []

    # Styles (Specific to Template 1)
    name_style = ParagraphStyle('Name', fontSize=16, alignment=TA_CENTER, fontName='Helvetica-Bold')
    contact_style = ParagraphStyle('Contact', fontSize=9, alignment=TA_CENTER, spaceAfter=8)
    section_hdr = ParagraphStyle('Section', fontSize=11, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4)

    # 1. Header & Summary
    story.append(Paragraph(data['name'].upper(), name_style))
    contact = f"{data['email']} | {data['phone']} | {data['linkedin']}"
    story.append(Paragraph(contact, contact_style))
    story.append(Paragraph(data.get('summary', ''), styles['Normal']))

    # 2. Education (Dual Degree Support)
    story.append(Paragraph("EDUCATION", section_hdr))
    for edu in data.get('education', []):
        header = [[Paragraph(f"<b>{edu['school']}</b>", styles['Normal']), 
                   Paragraph(f"GPA: {edu['GPA']} | {edu['date']}", ParagraphStyle('R', alignment=TA_RIGHT))]]
        t = Table(header, colWidths=[400, 140])
        story.append(t)
        # Displays: B.S. Finance, B.S. Management Information Systems [cite: 5]
        story.append(Paragraph(f"B.S. {', '.join(edu['majors'])}", styles['Normal']))

    # 3. Professional Experience (The 'Chameleon' Content)
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_hdr))
    for job in data.get('experience', []):
        exp_row = [[Paragraph(f"<b>{job['company']}</b>, {job['title']}", styles['Normal']),
                    Paragraph(f"{job['location']} | {job['date']}", ParagraphStyle('R', alignment=TA_RIGHT))]]
        story.append(Table(exp_row, colWidths=[380, 160]))
        for bullet in job['bullets']:
            story.append(Paragraph(f"• {bullet}", ParagraphStyle('B', leftIndent=12)))

    doc.build(story)