import scraper
import processor
import document_engine

# MOCK DATA: Simulates the output of database.get_full_user_profile(user_id)
mock_John_profile = {
    "name": "John Doe",
    "email": "email@test.edu",
    "phone": "999-999-9999",
    "linkedin": "linkedin.com",
    "summary": "Graduating senior with degrees in MIS and Finance seeking full-time employment.",
    "education": [
        {
            "school": "Technological University",
            "GPA": 3.90,
            "date": "Apr 2026",
            "majors": ["Finance", "Management Information Systems"]
        }
    ],
    "experience": [
        {
            "company": "Random Company",
            "title": "Analytics Intern",
            "location": "Remote",
            "date": "Jun 2025 - Aug 2025",
            "bullets": [
                "Automated custom emails to 200+ users using excel VBA Macros",
                "Designed an area-level dashboard to centralize performance data across 15+ users"
            ]
        },
        {
            "company": "Random, Inc.",
            "title": "Business Intern",
            "location": "Detroit, MI",
            "date": "May 2024 - Aug 2024",
            "bullets": [
                "Led a project to analyze and optimize the supply chain for a key product line, resulting in a 15% reduction in lead time.",
                "Coached leadership on AI prompt engineering and use cases."
            ]
        }
    ],
    "skills": ["Power BI", "SQL", "Python", "Advanced Excel (Macros/VBA)", "Agile (Scrum)"]
}

def run_test_chameleon():
    print("--- STARTING MOCK TEST ---")
    
    # 1. TEST SCRAPER (Using the Polaris link that worked with cloudscraper)
    target_url = "https://www.polaris.com/en-us/careers/job-categories/all/apply/r27439/" 
    print(f"Scraping job description from: {target_url}")
    job_desc = scraper.get_job_description(target_url)

    # 2. TEST AI BRAIN (The 'Selection' Step)
    print("AI is selecting relevant experiences and skills...")
    # This now returns the selection_results (IDs, Skills, and tailored summary)
    selection_results = processor.tailor_resume_content(mock_John_profile, job_desc)

    if not selection_results:
        print("Error: AI Selection failed.")
        return

    # 3. TEST ASSEMBLY (Mirroring the logic in main.py)
    print("Assembling tailored data locally...")
    template_choice = "template1"
    output_name = "John_Test_Tailored.pdf"

    tailored_json = {
        "name": mock_John_profile["name"],
        "email": mock_John_profile["email"],
        "phone": mock_John_profile["phone"],
        "linkedin": mock_John_profile.get("linkedin", ""),
        "summary": selection_results["tailored_summary"],
        "education": mock_John_profile["education"],
        "skills": selection_results["selected_skills"],
        "experience": []
    }

    # Filter mock experience based on AI selection
    # Using .strip() to ensure matching accuracy
    for exp in mock_John_profile["experience"]:
        if exp["company"].strip() in selection_results["selected_experience_ids"]:
            tailored_json["experience"].append(exp)

    # 4. TEST PRINTER
    print(f"Generating PDF: {output_name}")
    document_engine.generate_chameleon_pdf(output_name, tailored_json, template_choice)

    print(f"--- TEST COMPLETE: Check {output_name} in your folder ---")

if __name__ == "__main__":
    run_test_chameleon()