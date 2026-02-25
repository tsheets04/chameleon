import cloudscraper
from bs4 import BeautifulSoup
import time
import random

def get_job_description(url):
    # 1. CREATE SCRAPER: This replaces the standard requests/session object
    # It automatically handles the TLS fingerprinting and Cloudflare challenges
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )

    try:
        # HUMAN-LIKE DELAY
        time.sleep(random.uniform(2, 4))

        # GET THE PAGE
        response = scraper.get(url, timeout=15)
        response.raise_for_status() 

        # 1. INITIAL PARSE
        soup = BeautifulSoup(response.text, 'html.parser')

        # --- NEW CLEANING LOGIC STARTS HERE ---
        
        # 2. DELETE TRASH TAGS
        # This nukes the header, footer, and nav menus before we even look at the text
        for tag in soup(["header", "footer", "nav", "aside", "script", "style"]):
            tag.decompose()

        # 3. TARGET THE BODY
        # Most job boards use <main> or <article> for the actual job description
        # If they don't, we just fall back to the whole body
        main_content = soup.find('main') or soup.find('article') or soup.find('body') or soup

        # 4. EXTRACT WITH SEPARATOR
        # Using a space separator prevents words in different divs from sticking together
        raw_text = main_content.get_text(separator=' ')

        # 5. LINE-BY-LINE CLEANUP
        # This removes the massive chunks of whitespace often found in HTML
        lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
        clean_text = '\n'.join(lines)

        # 6. SURGICAL REMOVAL
        # If specific phrases slip through, target them here.
        garbage_phrases = ["Account Home", "My Garage", "Order Status", "Sign In", "Cart", "Log in", "Apply Now", "Share this job", "Similar Jobs", "Job ID:", "Posted on:", "Location:"]
        for phrase in garbage_phrases:
            clean_text = clean_text.replace(phrase, "")

        # --- NEW CLEANING LOGIC ENDS HERE ---

        return clean_text[:5000].strip()

    except Exception as e:
        return f"Error scraping: {e}"


if __name__ == "__main__":
    # Use the specific Polaris link you were testing
    test_url = "https://www.polaris.com/en-us/careers/job-categories/all/apply/r27439/" 
    print(get_job_description(test_url))