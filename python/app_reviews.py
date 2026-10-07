"""Recent App Store + Google Play reviews for one app, saved to CSV, plus the built-in insights summary.

Actor: https://apify.com/zahidthani/app-store-google-play-reviews
Cost:  $0.005 per run + $0.12 per 1,000 reviews + $0.005 per app summary. This example: about $0.02.

    export APIFY_TOKEN=your_token
    python app_reviews.py
"""
import csv
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run_input = {
    "apps": ["Duolingo"],           # app name, store URL, App Store ID or package name
    "stores": ["apple", "google"],
    "countries": ["us"],
    "maxReviewsPerApp": 20,         # per store and country
    "sort": "newest",
    # "reviewsSince": "7 days",     # handy for a weekly schedule
    # "maxRating": 2,               # complaints only
}

run = client.actor("zahidthani/app-store-google-play-reviews").call(run_input=run_input, max_total_charge_usd=0.10)
# apify-client 3.x returns a Run object; 1.x and 2.x return a dict
dataset_id = getattr(run, "default_dataset_id", None) or run["defaultDatasetId"]
items = list(client.dataset(dataset_id).iterate_items())

reviews = [i for i in items if i["type"] == "review"]
fields = ["store", "appName", "rating", "date", "appVersion", "title", "text"]
with open("app_reviews.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
    w.writeheader()
    w.writerows(reviews)
print(f"saved {len(reviews)} reviews to app_reviews.csv")

for s in (i for i in items if i["type"] == "appSummary"):
    themes = ", ".join(f'{t["theme"]} ({t["reviews"]})' for t in s["complaintThemes"][:3]) or "-"
    print(f'{s["store"]:<6} {s["name"]}: store rating {s["rating"]:.2f}, '
          f'{s["negativeShare"]:.0%} of fetched reviews are 1-2 stars; complaints: {themes}')
