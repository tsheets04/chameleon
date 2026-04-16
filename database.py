import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# 1. DATABASE CONNECTION SETUP
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "resume_chameleon_db")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = sa.create_engine(DB_URL)
Session = sessionmaker(bind=engine)

def get_full_user_profile(user_id):
    session = Session()
    try:
        # --- A. FETCH BASIC USER INFO ---
        # Note: Assuming standard WP 'users' table or custom 'wpresume_user' if created.
        # If your user table isn't wpresume_user, update this table name.
        user_query = sa.text("SELECT * FROM wpusers WHERE ID = :uid")
        user_row = session.execute(user_query, {"uid": user_id}).mappings().first()
        
        profile = {
            "name": user_row['display_name'] if user_row else "User",
            "email": user_row['user_email'] if user_row else "",
            "phone": "", # Phone is often in wp_usermeta
            "summary": "",
            "experience": [],
            "education": [],
            "leadership": [],
            "skills": []
        }

        # --- B. FETCH SUMMARY ---
        sum_query = sa.text("SELECT summary_text FROM wpresume_summary WHERE wp_user_id = :uid")
        sum_row = session.execute(sum_query, {"uid": user_id}).mappings().first()
        if sum_row:
            profile["summary"] = sum_row['summary_text']

        # --- C. FETCH EDUCATION ---
        edu_query = sa.text("""
            SELECT e.institution_name as school, e.gpa as GPA, e.graduation_date as date, m.major_name as major 
            FROM wpresume_education e 
            JOIN wpresume_edumajor m ON e.education_id = m.education_id 
            WHERE e.wp_user_id = :uid
        """)
        edu_results = session.execute(edu_query, {"uid": user_id}).mappings().all()
        # Group majors by education_id to handle dual degrees/majors
        temp_edu = {}
        for row in edu_results:
            eid = row['education_id']
            if eid not in temp_edu:
                temp_edu[eid] = {
                    "school": row['school'],
                    "GPA": row['GPA'],
                    "date": row['date'],
                    "majors": []
                }
            # Add this specific major to the list for this school
            temp_edu[eid]["majors"].append(row['major'])
        
        profile["education"] = list(temp_edu.values())

        # --- D. FETCH EXPERIENCE & DESCRIPTIONS ---
        exp_query = sa.text("""
            SELECT e.experience_id, e.employer, e.job_title as title, e.city, e.state, e.start_date, e.end_date, d.description as descr 
            FROM wpresume_experience e
            LEFT JOIN wpresume_expdesc d ON e.experience_id = d.experience_id
            WHERE e.wp_user_id = :uid
            ORDER BY e.start_date DESC
        """)
        exp_results = session.execute(exp_query, {"uid": user_id}).mappings().all()
        
        temp_exp = {}
        for row in exp_results:
            eid = row['experience_id']
            if eid not in temp_exp:
                temp_exp[eid] = {
                    "company": row['employer'],
                    "title": row['title'],
                    "location": f"{row['city']}, {row['state']}",
                    "date": f"{row['start_date']} - {row['end_date']}",
                    "bullets": []
                }
            if row['descr']:
                temp_exp[eid]["bullets"].append(row['descr'])
        profile["experience"] = list(temp_exp.values())

        # --- E. FETCH LEADERSHIP ---
        lead_query = sa.text("""
            SELECT l.leadership_id, l.organization_name as org, l.role_title as title, l.start_date, l.end_date, ld.description as descr 
            FROM wpresume_leadership l
            LEFT JOIN wpresume_leaddesc ld ON l.leadership_id = ld.leadership_id
            WHERE l.wp_user_id = :uid
            ORDER BY l.start_date DESC
        """)
        lead_results = session.execute(lead_query, {"uid": user_id}).mappings().all()
        
        temp_lead = {}
        for row in lead_results:
            lid = row['leadership_id']
            if lid not in temp_lead:
                temp_lead[lid] = {
                    "org": row['org'],
                    "title": row['title'],
                    "date": f"{row['start_date']} - {row['end_date']}",
                    "bullets": []
                }
            if row['descr']:
                temp_lead[lid]["bullets"].append(row['descr'])
        profile["leadership"] = list(temp_lead.values())

        # --- F. FETCH ADDITIONAL SKILLS ---
        skill_query = sa.text("SELECT skill_name as skill FROM wpresume_addskill WHERE wp_user_id = :uid")
        skill_results = session.execute(skill_query, {"uid": user_id}).mappings().all()
        profile["skills"] = [s['skill'] for s in skill_results]

        return profile

    finally:
        session.close()