# 🚀 LinkedIn Guest Job Scraper (Easy-Apply Edition)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Playwright](https://img.shields.io/badge/Playwright-Enabled-green)
![License](https://img.shields.io/badge/License-MIT-orange)

A lightweight, interactive command-line tool built with **Python and Playwright** that scrapes LinkedIn job postings *without* requiring an account. 

It aggressively bypasses LinkedIn's guest login popups and iframe walls, navigates the public job board, and exports highly targeted "Easy Apply" roles directly to a CSV file.

## ✨ Features

* 🚫 **No Account Needed:** Operates entirely on LinkedIn's public-facing job board. Safe from account bans!
* 💥 **Iframe Assassin:** Automatically detects and nukes LinkedIn's aggressive login popups and overlay walls using native JavaScript DOM manipulation.
* 🎨 **Interactive TUI:** Features a clean, color-coded terminal user interface (TUI) to easily configure your search parameters.
* 🎯 **Custom Targeting:** Filter jobs by **Role**, **Country**, **City**, and specific **Experience Levels** (Internship, Fresher, Mid-Senior, etc.).
* 📁 **CSV Export:** Neatly packages your extracted data (`Job Title`, `Company`, `Location`, `Easy Apply`, `Job Link`) into a uniquely named CSV file.

## ⚠️ Important Note: The "60-Job" Limit
When scraping LinkedIn without an active login session, LinkedIn's backend servers impose a hard limit of approximately **60 jobs per search query**. 

This script relies entirely on guest access. If it stops extracting at ~60 jobs, **this is not a bug**. It means the server has refused to send further pagination data for that specific search. 
* *Pro Tip:* If you need hundreds of jobs, simply run the script multiple times targeting different specific cities (e.g., one run for "Pune", another for "Bengaluru").

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/linkedin-guest-scraper.git](https://github.com/YOUR_USERNAME/linkedin-guest-scraper.git)
   cd linkedin-guest-scraper

   Install the required Python packages:
This script relies on Playwright to handle advanced browser automation.

Bash
pip install playwright
Install the Playwright Chromium binaries:
Crucial step: Playwright needs its own set of browser binaries to run.

Bash
playwright install chromium
🚀 Usage
Run the script directly from your terminal:

Bash
python scraper.py
You will be greeted by the interactive setup menu:

Plaintext
============================================================
   🚀 LINKEDIN GUEST SCRAPER: EASY-APPLY EDITION 🚀
============================================================

► STEP 1: Job Details
  Enter job role/type (e.g., Python Developer, BPO, IT): Python Developer

► STEP 2: Location
  Enter Country (e.g., India, United States): India
  Enter City/State (e.g., Pune) or press Enter to skip: Pune

► STEP 3: Experience Level
  [1] Internship
  [2] Entry level / Fresher
  [3] Associate
  [4] Mid-Senior level
  [5] Director
  [6] Executive
  [0] Any / All
  Select option (0-6): 2
The bot will automatically launch a visible Chrome instance, destroy any login popups that attempt to block its path, scroll to collect the jobs, and save them to a file (e.g., linkedin_jobs_pythondevelop_60.csv).

👨‍💻 Tech Stack
Language: Python

Automation Framework: Playwright (sync_playwright)

Data Processing: Native Python csv module

📜 Disclaimer
This tool is for educational purposes only. Web scraping may violate the Terms of Service of some websites. The authors are not responsible for any misuse of this software. Please scrape responsibly and respect rate limits.

🤝 Contributing
Pull requests are welcome! If you find a new class name or ID that LinkedIn is using for their guest-wall popups, feel free to submit a PR to add it to the badElements array in the destroy_popup_via_js() function.
