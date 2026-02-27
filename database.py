import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 1. DATABASE CONNECTION SETUP
# REPLACE WITH NEEDED CREDENTIALS
load_dotenv()
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "resume_chameleon_db")

DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

engine = sa.create_engine(DB_URL)
Session = sessionmaker(bind=engine)

# 2. FUNCTION TO FETCH FULL USER PROFILE
#This collects data from the user, education, experience, and leadership tables.
def get_full_user_profile(user_id):
    session = Session()
    try:
        # --- A. FETCH BASIC USER INFO ---
        # Corresponds to 'user' table
        user_query = sa.text("SELECT * FROM user WHERE userId = :uid")
        user_row = session.execute(user_query, {"uid": user_id}).mappings().first()
        
        if not user_row:
            return None

        profile = {
            "name": f"{user_row['first']} {user_row['last']}",
            "email": user_row['email'],
            "phone": user_row['phone'],
            "summary": "",
            "experience": [],
            "education": [],
            "leadership": [],
            "skills": []
        }

        # --- B. FETCH EDUCATION ---
        edu_query = sa.text("""
            SELECT e.school, e.GPA, m.major 
            FROM education e 
            JOIN eduMajor m ON e.eduId = m.eduId 
            WHERE e.userId = :uid
        """)
        edu_results = session.execute(edu_query, {"uid": user_id}).mappings().all()
        profile["education"] = [dict(row) for row in edu_results]

        # --- C. FETCH EXPERIENCE & DESCRIPTIONS ---
        exp_query = sa.text("""
            SELECT e.expId, e.employer, e.title, e.city, e.state, e.startDate, e.endDate, d.descr 
            FROM experience e
            LEFT JOIN expDesc d ON e.expId = d.expId
            WHERE e.userId = :uid
            ORDER BY e.startDate DESC
        """)
        exp_results = session.execute(exp_query, {"uid": user_id}).mappings().all()
        
        # We group the descriptions (bullets) by the experience ID since they come in separate rows due to the LEFT JOIN. This way we can build a structured experience entry with its associated bullets.
        temp_exp = {}
        for row in exp_results:
            eid = row['expId']
            if eid not in temp_exp:
                temp_exp[eid] = {
                    "company": row['employer'],
                    "title": row['title'],
                    "location": f"{row['city']}, {row['state']}",
                    "date": f"{row['startDate']} - {row['endDate']}",
                    "bullets": []
                }
            if row['descr']:
                temp_exp[eid]["bullets"].append(row['descr'])
        
        profile["experience"] = list(temp_exp.values())

        # --- D. FETCH ADDITIONAL SKILLS ---
        # Collects skills like Power BI, SQL, and Python [cite: 40]
        skill_query = sa.text("SELECT skill FROM addSkill WHERE userId = :uid")
        skill_results = session.execute(skill_query, {"uid": user_id}).mappings().all()
        profile["skills"] = [s['skill'] for s in skill_results]

        return profile

    finally:
        session.close()
        
        
#Test Case HERE once we have data in the database.
#if __name__ == "__main__":
#    test_profile = get_full_user_profile(1) # Assuming 1 is the userId
#    print(test_profile)