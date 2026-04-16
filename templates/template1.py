from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

def render(filename, data):
    """
    High-density layout.
    """
    doc = SimpleDocTemplate(filename, pagesize=letter, rightMargin=35, leftMargin=35, topMargin=35, bottomMargin=35)
    styles = getSampleStyleSheet()
    story = []

    # Styles (Specific to Template 1)
    name_style = ParagraphStyle('Name', fontSize=16, alignment=TA_CENTER, fontName='Helvetica-Bold', spaceAfter=6)
    contact_style = ParagraphStyle('Contact', fontSize=9, alignment=TA_CENTER, spaceAfter=8)
    section_hdr = ParagraphStyle('Section', fontSize=11, fontName='Helvetica-Bold', spaceBefore=10, spaceAfter=4)

    # 1. Header & Summary
    story.append(Paragraph(data['name'].upper(), name_style))
    contact = f"{data['email']} | {data['phone']} | {data['linkedin']}"
    story.append(Paragraph(contact, contact_style))
    story.append(Paragraph(data.get('summary', ''), styles['Normal']))

    # 2. Education (Safer keys and Dual Degree Support)
    story.append(Paragraph("EDUCATION", section_hdr))
    for edu in data.get('education', []):
        # We use .get() so the code doesn't crash if a key is missing
        school = edu.get('school', 'University Name')
        gpa = edu.get('GPA', 'N/A')
        # Database uses 'graduation_date', but template was looking for 'date'
        grad_date = edu.get('date', edu.get('graduation_date', '')) 
        
        header = [[Paragraph(f"<b>{school}</b>", styles['Normal']), Paragraph(f"GPA: {gpa} | {grad_date}", ParagraphStyle('R', alignment=TA_RIGHT))]]
        
        t = Table(header, colWidths=[400, 140])
        story.append(t)

        # Handle majors (Check if it's a list or a single string)
        majors_data = edu.get('majors', edu.get('major', 'Major Not Listed'))
        if isinstance(majors_data, list):
            majors_str = ", ".join(majors_data)
        else:
            majors_str = majors_data
            
        story.append(Paragraph(f"B.S. {majors_str}", styles['Normal']))

    # 3. Professional Experience (The 'Chameleon' Content)
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_hdr))
    for job in data.get('experience', []):
        exp_row = [[Paragraph(f"<b>{job['company']}</b>, {job['title']} | {job['location']}", styles['Normal']),
                    Paragraph(f"{job['date']}", ParagraphStyle('R', alignment=TA_RIGHT))]]
        story.append(Table(exp_row, colWidths=[360, 180]))
        for bullet in job['bullets']:
            story.append(Paragraph(f"• {bullet}", ParagraphStyle('B', leftIndent=12)))

    # 4. Leadership & Activities
    if data.get('leadership'):
        story.append(Paragraph("LEADERSHIP & ACTIVITIES", section_hdr))
        for lead in data['leadership']:
            lead_row = [[Paragraph(f"<b>{lead['org']}</b>, {lead['title']}", styles['Normal']), Paragraph(lead.get('date', ''), ParagraphStyle('R', alignment=TA_RIGHT))]]
            story.append(Table(lead_row, colWidths=[420, 120]))
            for bullet in lead.get('bullets', []):
                story.append(Paragraph(f"• {bullet}", styles['Normal']))

    # 5. Skills
    if data.get('skills'):
        story.append(Paragraph("SKILLS", section_hdr))
        skills_str = ", ".join(data['skills'])
        story.append(Paragraph(skills_str, styles['Normal']))

    doc.build(story)