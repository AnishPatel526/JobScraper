import requests
import pandas as pd
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread_formatting import (
    batch_updater,
    format_cell_range,
    set_frozen,
    set_column_width,
    cellFormat,
    textFormat,
    Color,
)

# -------- API CONFIG --------
APP_ID = "INSERT_ID"
API_KEY = "INSERT_KEY"
COUNTRY = "us"
SEARCH_TERM = "software intern"
RESULTS_PER_PAGE = 50  # can increase for more jobs

# -------- GOOGLE SHEETS CONFIG --------
SHEET_NAME = "Adzuna Jobs"
CREDENTIALS_FILE = "/Users/anishpatel/Coding Projects/Job Scraper/creds.json"

# -------- FETCH JOBS FROM ADZUNA --------
url = (
    f"https://api.adzuna.com/v1/api/jobs/{COUNTRY}/search/1"
    f"?app_id={APP_ID}&app_key={API_KEY}"
    f"&results_per_page={RESULTS_PER_PAGE}"
    f"&what={SEARCH_TERM.replace(' ', '+')}"
)

print(f"[INFO] Requesting: {url}")
response = requests.get(url)

if response.status_code != 200:
    print(f"[ERROR] Failed to fetch data: {response.status_code}")
    print(response.text)
    exit()

data = response.json()
results = data.get("results", [])

jobs = []
for job in results:
    published_raw = job.get("created", "")
    published_fmt = (
        datetime.strptime(published_raw, "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y")
        if published_raw else "N/A"
    )

    jobs.append({
        "Job Title": job.get("title", "N/A"),
        "Company": job.get("company", {}).get("display_name", "N/A"),
        "Location": job.get("location", {}).get("display_name", "N/A"),
        "Type": job.get("contract_type", "Unknown") or "Unknown",
        "Category": job.get("category", {}).get("label", "N/A"),
        "Posted": published_fmt,
        "Link": job.get("redirect_url", "N/A"),
    })

# -------- SAVE TO CSV --------
df = pd.DataFrame(jobs, columns=[
    "Job Title", "Company", "Location", "Type", "Category", "Posted", "Link"
])
df.to_csv("adzuna_jobs.csv", index=False)
print(f"[INFO] Saved {len(df)} jobs to adzuna_jobs.csv ✅")

# -------- EXPORT TO GOOGLE SHEETS --------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

try:
    sheet = client.open(SHEET_NAME).sheet1
except gspread.SpreadsheetNotFound:
    print(f"[ERROR] Google Sheet '{SHEET_NAME}' not found. Make sure it exists and is shared with the service account.")
    exit()

sheet.clear()
sheet.update([df.columns.values.tolist()] + df.values.tolist())
print(f"[INFO] Exported to Google Sheet: {SHEET_NAME} ✅")

# -------- GOOGLE SHEET FORMATTING --------

# Freeze top row
set_frozen(sheet, rows=1)

# Bold header row with light gray background
format_cell_range(sheet, "A1:G1", cellFormat(
    textFormat=textFormat(bold=True),
    backgroundColor=Color(0.88, 0.88, 0.88)
))

# Set columns A–G to width 200
for col_letter in ["A", "B", "C", "D", "E", "F", "G"]:
    try:
        set_column_width(sheet, col_letter, 200)
    except Exception as e:
        print(f"[WARN] Could not set width for column {col_letter}: {e}")

# Light green row shading for rows 2–100
format_cell_range(sheet, "A2:G100", cellFormat(
    backgroundColor=Color(0.96, 1, 0.96)
))
