# JobScraper
A Python job scraper utilizing the **Adzuna Jobs API** to fetch software internship postings and export to a **formatted Google Sheet**. Presents CSV export, Google Sheets integration, and auto-formatting for readability.


## Features

- Connects to the Adzuna Job Search API
- Exports listings to a local `adzuna_jobs.csv` file
- Updates directly onto a Google Sheet
- Applies formatting: bold headers and easy readability
- Configurable search terms (e.g., `software intern`, `remote`, etc.)

## Project Structure

job-scraper/
 - adzuna_scraper.py # Main scrip
 - requirements.txt # Python dependencies
 - .gitignore # Keeps creds.json and venv out of Git
 - README.md # Currently Reading!
 - creds.json # (Not tracked) Google Sheets API credentials / Stores API Key


---

## Setup Instructions

# 1. Clone the repo

```bash```
- git clone https://github.com/AnishPatel526/JobScraper.git
- cd JobScraper

# 2. Install Requirements (If you don't already have)

- pip install -r requirements.txt

# 3. Set up Google Sheets API

- Create a Google Cloud project
- Enable Google Sheets API & Drive API
- Generate a Service Account and download the creds.json
- Share your Google Sheet with that service account and give it Editor or Owner Access

# 4. Run the scraper!! :)

- python adzuna_scraper.py

**Contact**

- Feel free to connect with me or reach out with any questions!!
- GitHub: @AnishPatel526
- LinkedIn: www.linkedin.com/in/anish-patel-254a18264
- Email: abpatel1@unc.edu

