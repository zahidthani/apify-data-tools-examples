"""What is trending on Google right now? Biggest trends by search volume for one country.

Actor: https://apify.com/zahidthani/google-trends-trending-now
Cost:  $0.005 per run + $0.001 per trend delivered. This example (10 trends): about $0.015.
Set "maxItemsPerCountry": 0 for the full list (often 300-500 trends per country per day).

    export APIFY_TOKEN=your_token
    python trending_now.py
"""
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run_input = {
    "countries": ["US"],
    "timeWindow": "24",          # 4, 24, 48 or 168 hours
    "sortBy": "volume",
    "maxItemsPerCountry": 10,
    # "categories": ["Technology"],
    # "onlyNew": True, "monitorName": "my-alerts",   # scheduled alerts without repeats
}

run = client.actor("zahidthani/google-trends-trending-now").call(run_input=run_input, max_total_charge_usd=0.05)
# apify-client 3.x returns a Run object; 1.x and 2.x return a dict
dataset_id = getattr(run, "default_dataset_id", None) or run["defaultDatasetId"]

for t in client.dataset(dataset_id).iterate_items():
    category = (t["categories"] or ["-"])[0]
    status = "active" if t["isActive"] else "ended"
    print(f'{t["rank"]:>3}. {t["keyword"]:<40} {t["searchVolumeLabel"]:>6}  +{t["increasePercent"]}%  {category} ({status})')
