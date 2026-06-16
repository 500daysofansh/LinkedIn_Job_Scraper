import os
import time
import csv
import random
import urllib.parse
from playwright.sync_api import sync_playwright

TARGET_JOBS = 60

# --- Terminal UI Colors & Formatting ---
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
MAGENTA = '\033[95m'
RESET = '\033[0m'
BOLD = '\033[1m'

def clear_screen():
    """Clears the terminal screen for a clean UI."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Prints the ASCII art title."""
    clear_screen()
    print(f"{CYAN}{BOLD}")
    print("============================================================")
    print("   🚀 LINKEDIN GUEST SCRAPER: EASY-APPLY EDITION 🚀")
    print("============================================================")
    print(f"{RESET}")

def get_user_inputs():
    """Interactive TUI for gathering search parameters."""
    print_banner()
    
    print(f"{YELLOW}► STEP 1: Job Details{RESET}")
    job_type = input(f"  Enter job role/type {CYAN}(e.g., Python Developer, BPO, IT){RESET}: ").strip()
    
    print(f"\n{YELLOW}► STEP 2: Location{RESET}")
    country = input(f"  Enter Country {CYAN}(e.g., India, United States){RESET}: ").strip()
    location = input(f"  Enter City/State {CYAN}(e.g., Pune) or press Enter to skip{RESET}: ").strip()
    
    print(f"\n{YELLOW}► STEP 3: Experience Level{RESET}")
    print(f"  {CYAN}[1]{RESET} Internship")
    print(f"  {CYAN}[2]{RESET} Entry level / Fresher")
    print(f"  {CYAN}[3]{RESET} Associate")
    print(f"  {CYAN}[4]{RESET} Mid-Senior level")
    print(f"  {CYAN}[5]{RESET} Director")
    print(f"  {CYAN}[6]{RESET} Executive")
    print(f"  {CYAN}[0]{RESET} Any / All")
    exp_choice = input(f"  Select option {CYAN}(0-6){RESET}: ").strip()

    # Format the location
    full_location = f"{location}, {country}" if location else country
    
    # URL Encoding
    encoded_keywords = urllib.parse.quote(job_type)
    encoded_location = urllib.parse.quote(full_location)
    
    # Base URL with Easy Apply (f_AL=true) and Sort by Recent (sortBy=DD)
    search_url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_keywords}&location={encoded_location}&f_AL=true&sortBy=DD"
    
    # Add experience filter if selected
    if exp_choice in ["1", "2", "3", "4", "5", "6"]:
        search_url += f"&f_E={exp_choice}"

    # Create a dynamic filename
    safe_job = "".join(x if x.isalnum() else "_" for x in job_type).lower()
    csv_file = f"linkedin_jobs_{safe_job[:15]}_60.csv"

    # Experience label for the summary
    exp_labels = {"1": "Internship", "2": "Fresher", "3": "Associate", "4": "Mid-Senior", "5": "Director", "6": "Executive", "0": "Any"}
    exp_text = exp_labels.get(exp_choice, "Any")

    print_banner()
    print(f"{GREEN}{BOLD}✓ Target Locked!{RESET}")
    print(f"  {BOLD}Role:{RESET}       {job_type}")
    print(f"  {BOLD}Location:{RESET}   {full_location}")
    print(f"  {BOLD}Experience:{RESET} {exp_text}")
    print(f"  {BOLD}Output:{RESET}     {csv_file}\n")
    
    return search_url, csv_file, full_location, job_type

def destroy_popup_via_js(page):
    """Destroys the iframe holding the login popup and re-enables scrolling."""
    try:
        page.evaluate("""() => {
            const badElements = [
                'iframe', // NUKE ALL IFRAMES
                '#base-contextual-sign-in-modal',
                '.modal__overlay',
                '.artdeco-modal-overlay',
                '.contextual-sign-in-modal',
                '[data-test-modal]',
                '#artdeco-modal-outlet' 
            ];
            
            badElements.forEach(selector => {
                document.querySelectorAll(selector).forEach(el => el.remove());
            });
            
            document.body.style.overflow = 'auto';
            document.documentElement.style.overflow = 'auto';
        }""")
    except:
        pass

def scrape_jobs_playwright(page, search_url, target_count):
    all_unique_jobs = {}
    stuck_counter = 0

    print(f"{MAGENTA}[*] Initializing connection to LinkedIn...{RESET}")
    page.goto(search_url, wait_until="domcontentloaded")
    
    time.sleep(random.uniform(4.0, 6.0))
    
    print(f"{MAGENTA}[*] Executing anti-popup measures...{RESET}")
    destroy_popup_via_js(page)
    time.sleep(1) 

    while len(all_unique_jobs) < target_count:
        previous_total = len(all_unique_jobs)

        extracted = page.evaluate("""() => {
            let extractedJobs = [];
            let jobCards = document.querySelectorAll('ul.jobs-search__results-list > li');
            
            jobCards.forEach(card => {
                let titleElement = card.querySelector('.base-search-card__title');
                let companyElement = card.querySelector('.base-search-card__subtitle');
                let locationElement = card.querySelector('.job-search-card__location');
                let linkElement = card.querySelector('a.base-card__full-link');
                
                if (titleElement && linkElement) {
                    let rawLink = linkElement.getAttribute('href');
                    let cleanLink = rawLink.split('?')[0]; 
                    
                    extractedJobs.push({
                        title: titleElement.innerText.trim().replace(/\\n/g, ' '),
                        company: companyElement ? companyElement.innerText.trim() : 'Unknown',
                        location: locationElement ? locationElement.innerText.trim() : 'Unknown',
                        easy_apply: 'Yes',
                        link: cleanLink
                    });
                }
            });
            return extractedJobs;
        }""")

        for job in extracted:
            all_unique_jobs[job['link']] = job

        print(f"{CYAN} ➔ Extracted {len(all_unique_jobs)} unique jobs...{RESET}")
        
        if len(all_unique_jobs) >= target_count:
            break

        destroy_popup_via_js(page)

        page.evaluate("window.scrollBy(0, window.innerHeight);")
        time.sleep(random.uniform(1.5, 2.5))

        try:
            see_more_btn = page.locator('button:has-text("See more jobs")').first
            if see_more_btn.is_visible(timeout=1000):
                print(f"{YELLOW} 🖱️ Clicking 'See more jobs'...{RESET}")
                see_more_btn.click(force=True)
                
                loader = page.locator("div.loader.loader--show").first
                if loader.is_visible(timeout=2000):
                    loader.wait_for(state="hidden", timeout=10000)
                time.sleep(random.uniform(1.5, 2.5))
        except:
            pass

        if len(all_unique_jobs) == previous_total:
            stuck_counter += 1
            if stuck_counter >= 3:
                print(f"\n{RED}⚠️ Reached the 60-job guest limit. Server denied further pagination.{RESET}")
                break
        else:
            stuck_counter = 0

    return list(all_unique_jobs.values())[:target_count]

def main():
    search_url, csv_file, location_str, job_type = get_user_inputs()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        page = context.new_page()

        try:
            print(f"{YELLOW}▶ Booting Playwright engine...{RESET}")
            final_list = scrape_jobs_playwright(page, search_url, TARGET_JOBS)

            print(f"\n{GREEN}💾 Saving {len(final_list)} jobs to {csv_file}...{RESET}")
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Job Title', 'Company', 'Location', 'Easy Apply', 'Job Link'])
                for job in final_list:
                    writer.writerow([job['title'], job['company'], job['location'], job['easy_apply'], job['link']])

            print(f"{GREEN}{BOLD}🎉 Mission Complete! You can now review your CSV.{RESET}\n")

        except Exception as e:
            print(f"\n{RED}❌ An error occurred: {e}{RESET}\n")

        finally:
            browser.close()

if __name__ == "__main__":
    main()
