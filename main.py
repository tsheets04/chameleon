import database
import scraper
import processor
import document_engine

def run_local_chameleon_test():
    print("--- 🦎 STARTING LOCAL CHAMELEON TEST ---")
    
    # 1. SETTINGS: Change these for your specific test
    # Ensure this user_id exists in Ty's 'wpresume_education' and other tables
    user_id = 1 
    target_url = "https://www.polaris.com/en-us/careers/job-categories/all/apply/r27439/"
    template_choice = "template1"
    output_name = "Local_Test_Tailored.pdf"

    # 2. FETCH DATA: Uses the new 'wpresume_' schema
    print(f"Reading data for User ID {user_id} from SQL...")
    master_data = database.get_full_user_profile(user_id)
    
    if not master_data:
        print("Error: User not found. Check Ty's database tables.")
        return

    # 3. SCRAPE JOB: Uses cloudscraper to bypass 403 blocks
    print(f"Scraping job description: {target_url}")
    job_desc = scraper.get_job_description(target_url)

    # 4. AI TAILORING: Decides what fits on one page
    print("AI Brain is selecting the best Experience and Leadership roles...")
    selection_results = processor.tailor_resume_content(master_data, job_desc)

    if not selection_results:
        print("Error: AI Selection failed. Check your API key and OpenAI credits.")
        return

    # 5. ASSEMBLY: Formatting data exactly like app.py
    print("Assembling the final resume structure...")
    tailored_json = {
        "name": master_data["name"],
        "email": master_data["email"],
        "phone": master_data["phone"],
        "linkedin": master_data.get("linkedin", "linkedin.com/in/user"),
        "summary": selection_results["tailored_summary"],
        "education": master_data["education"], # Education usually passes through
        "skills": selection_results["selected_skills"],
        "experience": [],
        "leadership": []
    }

    # Filter Work Experience based on AI choice
    for exp in master_data["experience"]:
        if exp["company"].strip() in selection_results["selected_experience_ids"]:
            tailored_json["experience"].append(exp)

    # Filter Leadership Roles based on AI choice
    for lead in master_data["leadership"]:
        if lead["org"].strip() in selection_results["selected_leadership_ids"]:
            tailored_json["leadership"].append(lead)

    # 6. GENERATE PDF: The final output
    print(f"Generating PDF: {output_name}")
    document_engine.generate_chameleon_pdf(output_name, tailored_json, template_choice)

    print(f"--- ✅ TEST COMPLETE: Check {output_name} in your folder ---")

if __name__ == "__main__":
    run_local_chameleon_test()