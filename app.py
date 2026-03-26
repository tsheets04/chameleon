import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS  # Helpful for WordPress-to-Python communication
import database
import scraper
import processor
import document_engine

app = Flask(__name__)
CORS(app)  # Allows your WordPress site to make requests to this API

@app.route('/', methods=['GET'])
def health_check():
    return "🦎 Resume Chameleon API is Live and Listening!"

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    """
    Endpoint for WordPress to trigger the Chameleon engine.
    Expects JSON: {"user_id": 1, "job_url": "...", "template": "template1"}
    """
    try:
        # 1. PARSE THE REQUEST
        request_data = request.json
        user_id = request_data.get('user_id')
        job_url = request_data.get('job_url')
        template_choice = request_data.get('template', 'template1')

        if not user_id or not job_url:
            return jsonify({"error": "Missing user_id or job_url"}), 400

        # 2. FETCH MASTER DATA (The Librarian)
        print(f"Fetching data for User {user_id}...")
        master_data = database.get_full_user_profile(user_id)
        if not master_data:
            return jsonify({"error": "User not found in database"}), 404

        # 3. SCRAPE JOB (The Researcher)
        print(f"Scraping job description: {job_url}")
        job_desc = scraper.get_job_description(job_url)
        if "Error" in job_desc:
            return jsonify({"error": f"Scraper failed: {job_desc}"}), 500

        # 4. TAILOR CONTENT (The Brain)
        print("AI is selecting best-match content...")
        selection_results = processor.tailor_resume_content(master_data, job_desc)
        if not selection_results:
            return jsonify({"error": "AI tailoring failed"}), 500

        # 5. ASSEMBLY (Logic from main.py)
        print("Assembling tailored JSON...")
        tailored_json = {
            "name": master_data["name"],
            "email": master_data["email"],
            "phone": master_data["phone"],
            "linkedin": master_data.get("linkedin", "linkedin.com/in/user"),
            "summary": selection_results["tailored_summary"],
            "education": master_data["education"], 
            "skills": selection_results["selected_skills"],
            "experience": []
        }

        # Filter the master experience list based on AI selection
        for exp in master_data["experience"]:
            # Uses .strip() for better matching
            if exp["company"].strip() in selection_results["selected_experience_ids"]:
                tailored_json["experience"].append(exp)

        # 6. GENERATE PDF (The Printer)
        output_filename = f"Resume_{user_id}_Tailored.pdf"
        document_engine.generate_chameleon_pdf(output_filename, tailored_json, template_choice)

        # 7. SEND FILE BACK
        return send_file(output_filename, as_attachment=True)

    except Exception as e:
        print(f"Server Error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    # Use port 5000 for local testing
    app.run(host='0.0.0.0', port=5000, debug=True)