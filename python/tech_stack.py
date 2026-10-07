"""Which of these websites run Shopify, WordPress, HubSpot...? And which email provider does each company use?

Actor: https://apify.com/zahidthani/website-tech-stack-detector
Cost:  $0.0005 per run + $0.002 per website analysed (dead and blocked sites are free). This example: under $0.01.

    export APIFY_TOKEN=your_token
    python tech_stack.py
"""
import csv
import os

from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])

run_input = {
    "websites": ["wordpress.org", "hubspot.com", "jane@stripe.com"],  # domains, URLs or work emails
    "includeDns": True,  # email provider, DNS host, verified SaaS tools
    # "proxyConfiguration": {"useApifyProxy": True, "apifyProxyGroups": ["RESIDENTIAL"]},  # for sites that block cloud IPs
}

run = client.actor("zahidthani/website-tech-stack-detector").call(run_input=run_input, max_total_charge_usd=0.05)
# apify-client 3.x returns a Run object; 1.x and 2.x return a dict
dataset_id = getattr(run, "default_dataset_id", None) or run["defaultDatasetId"]
items = list(client.dataset(dataset_id).iterate_items())

fields = ["domain", "cms", "ecommercePlatform", "jsFramework", "cdn", "emailProvider", "dnsProvider", "technologyCount"]
sites = [i for i in items if i["type"] == "website"]
with open("tech_stack.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields + ["pageBlocked"], extrasaction="ignore")
    w.writeheader()
    w.writerows(sites)

for s in sites:
    print(f'{s["domain"]:<16} cms={s["cms"]}  shop={s["ecommercePlatform"]}  email={s["emailProvider"]}  '
          f'cdn={s["cdn"]}  ({s["technologyCount"]} technologies){"  [blocked: DNS only, free]" if s.get("pageBlocked") else ""}')
for e in (i for i in items if i["type"] == "error"):
    print(f'{e["input"]:<16} not analysed (free): {e["error"]}')
print("saved tech_stack.csv")
