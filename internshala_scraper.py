# scrapers/internshala_auto_scraper.py
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from pathlib import Path
import json
import time

KEYWORDS = [
    "internship",
    "data science internship",
    "web development internship",
    "software internship",
    "python internship",
    "ai internship",
    "machine learning internship",
    "marketing internship",
    "hr internship",
    "business analyst internship",
    "backend internship",
    "frontend internship",
    "flutter internship",
    "react internship",
    "java internship"
]

def parse_internshala_card(html):
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.select_one(".main_heading") or soup.select_one("h3.job-internship-title a") or soup.select_one("h3")
    title = title_tag.get_text(strip=True) if title_tag else None

    promo = soup.select_one(".heading_tag")
    promo = promo.get_text(strip=True) if promo else None

    tagline = soup.select_one(".tagline")
    tagline = tagline.get_text(strip=True) if tagline else None

    company = None
    company_sel = soup.select_one("div.company-info a") or soup.select_one(".company_name") or soup.select_one(".internship_company")
    if company_sel:
        company = company_sel.get_text(strip=True)

    link_tag = soup.select_one("a[href]")
    apply_link = None
    if link_tag:
        href = link_tag.get("href")
        apply_link = "https://internshala.com" + href if href and href.startswith("/") else href

    location_sel = soup.select_one(".location_link") or soup.select_one(".location") or soup.select_one(".internship_location")
    location = location_sel.get_text(strip=True) if location_sel else None

    stipend_sel = soup.select_one(".stipend") or soup.select_one(".stipend-text") or soup.select_one(".salary")
    stipend = stipend_sel.get_text(strip=True) if stipend_sel else None

    duration = None
    dur_sel = soup.select_one("div.item_body > span") or soup.select_one(".duration")
    if dur_sel:
        duration = dur_sel.get_text(strip=True)

    posted_sel = soup.select_one("div.status > span") or soup.select_one(".posted") or soup.select_one(".date")
    posted = posted_sel.get_text(strip=True) if posted_sel else None

    skills = []
    for s in soup.select("div.tags div, .skills li, .internship_tags span"):
        txt = s.get_text(strip=True)
        if txt:
            skills.append(txt)

    return {
        "title": title,
        "promo": promo,
        "tagline": tagline,
        "company": company,
        "location": location,
        "stipend": stipend,
        "duration": duration,
        "skills": skills,
        "posted": posted,
        "apply_link": apply_link,
        "platform": "Internshala"
    }

def scrape_internshala_for_keyword(keyword, headless=True, scrolls=3, wait_ms=2500):
    search_url = f"https://internshala.com/internships/{keyword.replace(' ', '-')}"
    print("Internshala search URL:", search_url)
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        page.goto(search_url, timeout=60000)
        for _ in range(scrolls):
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(wait_ms/1000)
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select("div.individual_internship")
    print(f"Found {len(cards)} cards for '{keyword}'")
    for c in cards:
        results.append(parse_internshala_card(str(c)))
    return results

def scrape_internshala_all(keywords=KEYWORDS, headless=True, scrolls=3):
    all_jobs = []
    for kw in keywords:
        try:
            jobs = scrape_internshala_for_keyword(kw, headless=headless, scrolls=scrolls)
            all_jobs.extend(jobs)
        except Exception as e:
            print("Error scraping", kw, e)

    unique = {}
    for j in all_jobs:
        key = (j.get("title"), j.get("company"), j.get("apply_link"))
        if key not in unique and (j.get("title") or j.get("apply_link")):
            unique[key] = j

    final = list(unique.values())
    output_path = Path("scrapers/output")
    output_path.mkdir(parents=True, exist_ok=True)
    with open(output_path / "internshala_all_results.json", "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)
    print("Saved", len(final), "unique Internshala internships to scrapers/output/internshala_all_results.json")
    return final

if __name__ == "__main__":
    scrape_internshala_all(headless=False, scrolls=4)
