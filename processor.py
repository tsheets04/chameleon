import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# 1. INITIALIZE THE CLIENT
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def tailor_resume_content(master_data, job_description):
    """
    Analyzes the job description and filters Ethan's master data 
    (Experience, Leadership, and Skills) to fit a one-page layout.
    """
    
    # SYSTEM PROMPT: Setting the professional standards
    system_instructions = (
        "You are a professional recruiter specializing in Finance and MIS roles. "
        "Your goal is to tailor a candidate's resume to a specific job description. "
        "Rules:\n"
        "1. Maintain 100% factual accuracy.\n"
        "2. Prioritize experiences and leadership roles most relevant to the job.\n"
        "3. Use industry keywords and Power Verbs.\n"
        "4. Ensure the final selection is optimized for a one-page professional resume."
    )

    # USER PROMPT: Providing the full context including Leadership
    user_prompt = f"""
    JOB DESCRIPTION:
    {job_description}

    CANDIDATE MASTER DATA:
    - Summary: {master_data.get('summary', '')}
    - Experience: {master_data.get('experience', [])}
    - Leadership: {master_data.get('leadership', [])}
    - Skills: {master_data.get('skills', [])}

    Please return a JSON object with the following keys:
    1. 'tailored_summary': A 2-3 sentence punchy professional summary.
    2. 'selected_experience_ids': A list of the 'company' names for the most relevant work experiences.
    3. 'selected_leadership_ids': A list of the 'org' names for the most relevant leadership roles.
    4. 'selected_skills': A filtered list of the top 10 most relevant technical and soft skills.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        # Convert the AI's string response into a Python dictionary
        return json.loads(response.choices[0].message.content)

    except Exception as e:
        print(f"Error in Chameleon Brain: {e}")
        return None