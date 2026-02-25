import database
import scraper
import processor
import document_engine

def run_chameleon():
    print("--- Resume Chameleon Engine Started ---")
    
    # 1. IDENTIFY USER (In a real app, this comes from a login)
    user_id = 1  # Testing with Ethan's profile
    
    # 2. GET MASTER DATA (The 'Librarian' step)
    print("Fetching master data from SQL...")
    master_data = database.get_full_user_profile(user_id)
    
    if not master_data:
        print("Error: User not found in database.")
        return

    # 3. GET JOB DESCRIPTION (The 'Researcher' step)
    job_url = input("Enter the Job Posting URL: ")
    print("Scraping job description...")
    job_desc = scraper.get_job_description(job_url)

    # 4. TAILOR CONTENT (The 'Brain' step)
    selection_results = processor.tailor_resume_content(master_data, job_desc)

    # 5. CHOOSE TEMPLATE/USER INPUT
    template_choice = input("Choose a template (e.g., 'template1'): ") or "template1"
    output_name = input("Enter output filename (e.g., 'Tailored_Resume.pdf'): ") or f"{master_data['name'].replace(' ', '_')}_Tailored.pdf"

    # 6. ASSEMBLY (Python does the heavy lifting to save tokens)
    tailored_json = {
        "name": master_data["name"],
        "email": master_data["email"],
        "phone": master_data["phone"],
        "summary": selection_results["tailored_summary"],
        "education": master_data["education"], # Keep all education
        "skills": selection_results["selected_skills"],
        "experience": []
    }

    # Filter the master experience list based on AI selection
    for exp in master_data["experience"]:
        if exp["company"] in selection_results["selected_experience_ids"]:
            tailored_json["experience"].append(exp)

    # 7. GENERATE PDF
    document_engine.generate_chameleon_pdf(output_name, tailored_json, template_choice)

    print(f"--- Process Complete! File saved as {output_name} ---")

if __name__ == "__main__":
    run_chameleon()