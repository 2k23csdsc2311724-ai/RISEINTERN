# imports ...
from pymongo import MongoClient
from datetime import datetime
import json
from pathlib import Path
from internshala_scraper import scrape_internshala_all


def save_jobs_to_db(jobs, mongo_uri="mongodb://localhost:27017/"):
    client = MongoClient(mongo_uri)
    db = client["riseintern"]
    coll = db["internships"]
    coll.create_index(
        [("title", 1), ("company", 1), ("apply_link", 1)],
        unique=True
    )
    for job in jobs:
        job["scraped_at"] = datetime.utcnow()
        coll.update_one(
            {
                "title": job.get("title"),
                "company": job.get("company"),
                "apply_link": job.get("apply_link"),
            },
            {"$set": job},
            upsert=True
        )

if __name__ == "__main__":
    jobs = scrape_internshala_all(headless=False, scrolls=4)
    print("Scraped", len(jobs), "jobs — now inserting/updating into MongoDB")
    save_jobs_to_db(jobs)
    print("Done.")
