"""Google Trends for a few keywords: trend summary per keyword + a weekly timeline CSV.

Actor: https://apify.com/zahidthani/google-trends-scraper
Cost:  $0.01 per run + $0.004 per keyword (failed keywords are free). This example: about $0.02.

    export APIFY_TOKEN=your_token
    python google_trends.py
"""
import csv
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run_input = {
    "searchTerms": ["air fryer", "instant pot"],
    "geo": "US",                 # empty string = worldwide
    "timeRange": "today 12-m",   # now 7-d, today 3-m, today 5-y, all ...
    "compareTerms": True,        # put the terms on one 0-100 scale
    "includeInterestByRegion": False,
    "includeRelatedTopics": False,
}

run = client.actor("zahidthani/google-trends-scraper").call(run_input=run_input, max_total_charge_usd=0.10)
# apify-client 3.x returns a Run object; 1.x and 2.x return a dict
dataset_id = getattr(run, "default_dataset_id", None) or run["defaultDatasetId"]
items = list(client.dataset(dataset_id).iterate_items())

rows = {}
for item in items:
    if item["status"] != "ok":
        print("failed (not charged):", item["searchTerm"], item["errors"])
        continue
    s = item["summary"]
    print(f'{item["searchTerm"]:<12} avg {s["average"]:>5}  latest {s["latest"]:>3}  {s["trend"]:<8} '
          f'{s["changePercent"]:+.1f}%  peak {s["peak"]["date"][:10]}')
    rising = [q["query"] for q in item["relatedQueries"]["rising"][:3]]
    print("             rising searches:", ", ".join(rising) or "-")
    for point in item["interestOverTime"]:
        rows.setdefault(point["date"][:10], {})[item["searchTerm"]] = point["value"]

terms = [i["searchTerm"] for i in items if i["status"] == "ok"]
with open("google_trends_timeline.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["week"] + terms)
    for week in sorted(rows):
        w.writerow([week] + [rows[week].get(t) for t in terms])
print(f"saved google_trends_timeline.csv ({len(rows)} weeks)")
