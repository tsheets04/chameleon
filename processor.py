import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load your API key safely from a .env file
load_dotenv()

# 1. INITIALIZE THE CLIENT
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def tailor_resume_content(master_data, job_description):
    """
    Acts as a 'Filter'. Instead of rewriting, it selects the most 
    impactful experiences and skills for the specific job.
    """
    
    system_instructions = (
        "You are a talent acquisition specialist. Your task is to analyze a job description "
        "and select the best matching elements from a candidate's profile. "
        "Do not rewrite the content. Simply select which items should be included."
    )

    # We send a simplified version of the master_data to save tokens
    user_prompt = f"""
    JOB DESCRIPTION:
    {job_description}

    CANDIDATE DATA:
    {master_data}

    Return a JSON object with:
    1. 'selected_experience_ids': A list of company names or expIds that are most relevant.
    2. 'selected_skills': The top 6 skills that match the job keywords.
    3. 'tailored_summary': A 2-sentence summary specifically for this role.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Using the cheaper model
            messages=[
                {"role": "system", "content": system_instructions},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error in Selection Brain: {e}")
        return None