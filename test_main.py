import scraper
import processor
import document_engine

# MOCK DATA: Simulates the updated output of database.get_full_user_profile(user_id)
mock_John_profile = {
    "name": "John Doe",
    "email": "email@test.edu",
    "phone": "999-999-9999",
    "linkedin": "linkedin.com/in/johndoe",
    "summary": "Graduating senior with degrees in MIS and Finance seeking full-time employment.",
    "education": [
        {
            "school": "Michigan Technological University",
            "GPA": 3.90,
            "date": "Apr 2026", # Aliased from graduation_date in database.py
            "majors": ["Finance", "Management Information Systems"]
        }
    ],
    "experience": [
        {
            "company": "Random Company",
            "title": "Analytics Intern",
            "location": "Remote",
            "date": "Jun 2025 - Aug 2025",
            # Simulating a single text block from the database
            "bullets": "- Spearheaded a KPI-driven escalation framework by orchestrating data from multiple enterprise sources, including DMS and financial reporting tools, to identify high-impact dealers and establish national standard operating procedures - Automated custom emails to 200+ dealerships using a dynamic Excel macro allowing monthly vs yearly communications - Designed an area-level dashboard to centralize and compare performance data across 15+ dealerships, equipping managers to efficiently improve prioritizations - Created a JavaScript-enabled digital tool for parts escalation, streamlining manual procedures"
        },
        {
            "company": "Random, Inc.",
            "title": "Business Intern",
            "location": "Detroit, MI",
            "date": "May 2024 - Aug 2024",
            "bullets": "- Led a workflow redesign for part monitoring that cut cycle time by 75%, directly improving throughput - Redesigned the Post Qualification Management Excel Database to enhance user accessibility and streamline data entry - Co-developed a Gen Z–focused business solution with fellow interns highlighting cross-functional insights - Coached leadership on AI prompt engineering and use cases - Acted as a functional liaison between international teams to standardize data-sharing requirements"
        },
        {
            "company": "Mcdonald's Corporation",
            "title": "Data Analyst Intern",
            "location": "Remote",
            "date": "Jun 2023 - Aug 2023",
            "bullets": "- Facilitated high-volume point-of-sale transactions and resolved guest inquiries - Collaborated with a diverse team to meet strict speed-of-service targets during peak hours - Maintained rigorous food safety and sanitation standards - Actively promoted loyalty programs and upselling to contribute to restaurant profitability"
        }
    ],
    "leadership": [
        {
            "org": "Overland Club",
            "title": "Co-Founder / Treasurer",
            "date": "Sep 2023 - Present",
            "bullets": ["Managed $10k annual budget", "Organized 3 multi-day retreats"]
        },
        {
            "org": "Finance Club",
            "title": "Vice President",
            "date": "Jan 2024 - Present",
            "bullets": ["Coordinated guest speakers", "Increased membership by 20%"]
        }
    ],
    "skills": ["Power BI", "SQL", "Python", "Advanced Excel (Macros/VBA)", "Agile (Scrum)"]
}

def run_test_chameleon():
    print("--- 🦎 STARTING UPDATED MOCK TEST ---")
    
    # 1. TEST SCRAPER
    target_url = "https://www.polaris.com/en-us/careers/job-categories/all/apply/r28845/" 
    print(f"Scraping job description from: {target_url}")
    job_desc = scraper.get_job_description(target_url)

    # 2. TEST AI BRAIN (New logic with bullet splitting)
    print("AI is tailoring content and splitting bullet points...")
    selection_results = processor.tailor_resume_content(mock_John_profile, job_desc)

    if not selection_results:
        print("Error: AI Selection failed.")
        return

    # 3. TEST ASSEMBLY (Mirroring the updated app.py logic)
    print("Assembling tailored data structure...")
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
        "experience": [],
        "leadership": []
    }

    # FILTER EXPERIENCE: Map AI's split bullets back to the static data
    for ai_exp in selection_results.get("tailored_experience", []):
        company_name = ai_exp["company"]
        # Match against our mock profile
        original_data = next((item for item in mock_John_profile["experience"] if item["company"].strip() == company_name.strip()), None)
        
        if original_data:
            tailored_json["experience"].append({
                "company": company_name,
                "title": original_data["title"],
                "location": original_data["location"],
                "date": original_data["date"],
                "bullets": ai_exp["bullets"] # Uses the AI's clean list of strings
            })

    # FILTER LEADERSHIP: Match org names
    for lead in mock_John_profile.get("leadership", []):
        if lead["org"].strip() in selection_results.get("selected_leadership_ids", []):
            tailored_json["leadership"].append(lead)

    # 4. TEST PRINTER
    print(f"Generating PDF: {output_name}")
    document_engine.generate_chameleon_pdf(output_name, tailored_json, template_choice)

    print(f"--- ✅ TEST COMPLETE: Check {output_name} in your folder ---")

if __name__ == "__main__":
    run_test_chameleon()