# apify-data-tools-examples

Small, runnable Python, Node.js and n8n examples for four public-data tools on the Apify Store:

| Tool (Apify Actor) | What you get | Price |
|---|---|---|
| [Google Trends Scraper](https://apify.com/zahidthani/google-trends-scraper) | Interest over time, by region, related queries and topics for any keyword, plus a trend summary (rising/falling, % change, peak). A pytrends alternative that handles Google's 429 rate limits. | $0.004 per keyword + $0.01 per run |
| [App Store & Google Play Reviews](https://apify.com/zahidthani/app-store-google-play-reviews) | Reviews from both stores by app name or URL, with dates, versions and developer replies, plus a complaint-theme summary per app. | $0.12 per 1,000 reviews + $0.005 per run |
| [Website Tech Stack Detector](https://apify.com/zahidthani/website-tech-stack-detector) | CMS, Shopify and other e-commerce platforms, analytics, pixels, email marketing (Klaviyo, Mailchimp...) and the company's email provider from DNS, for a list of domains. | $2 per 1,000 websites + $0.0005 per run |
| [Google Trends Trending Now](https://apify.com/zahidthani/google-trends-trending-now) | The full Trending Now list per country (hundreds of trends, not the RSS top 10) with search volume and categories, and an only-new mode for alerts. | $1 per 1,000 trends + $0.005 per run |

Disclosure: I built and maintain these four Actors. The examples use only Apify's official client libraries and
public HTTP API, so you can adapt them to any other Actor too.

## What's inside

```
python/   google_trends.py  app_reviews.py  tech_stack.py  trending_now.py
node/     google-trends.js  app-reviews.js  tech-stack.js  trending-now.js
n8n/      google-trends-trending-now.json   (importable workflow: Manual Trigger -> HTTP Request)
```

Every example is a single file that reads your token from the `APIFY_TOKEN` environment variable, starts one small
run (a few cents at most, with a hard cap set through `max_total_charge_usd` / `maxTotalChargeUsd`) and prints the
results. The Python examples also write a CSV next to the script.

## Quick start

1. Create a free Apify account and copy your API token from **Console > Settings > API & Integrations**.
   Apify's free plan includes monthly platform credit, which covers these examples many times over.
2. Put the token in your environment (never commit it):
   ```bash
   export APIFY_TOKEN=your_token_here
   ```

### Python (3.9+)
```bash
cd python
pip install -r requirements.txt
python google_trends.py
```
The examples work with `apify-client` 1.x, 2.x and 3.x. (3.x returns a `Run` object instead of a dict, which is
why each script reads the dataset ID with a one-line fallback.)

### Node.js (18+)
```bash
cd node
npm install
node google-trends.js      # or: npm run google-trends
```

### n8n
1. In n8n, create a credential of type **Header Auth**: Name `Authorization`, Value `Bearer <your Apify token>`.
2. **Workflows > Import from file** and pick `n8n/google-trends-trending-now.json`.
3. Open the **HTTP Request** node, select your credential, and click **Execute workflow**. Each trend comes back as
   one n8n item, ready for a Slack, Google Sheets or email node.
4. For alerts, swap the Manual Trigger for a **Schedule Trigger** (e.g. hourly) and add `"onlyNew": true,
   "monitorName": "n8n-alerts"` to the JSON body so each run returns only trends you haven't seen yet.

The node calls Apify's `run-sync-get-dataset-items` endpoint, which starts the Actor, waits for it and returns the
results in one request. The same pattern works for the other three Actors: change the Actor name in the URL and
the JSON body (see the input examples on each Actor's Store page).

## Example output

`python/trending_now.py` (US, 6 October 2026):
```
  1. freddie jackson                           200K+  +1000%  Entertainment (active)
  2. argentina - benín                         200K+  +1000%  Sports (active)
  3. dodgers vs braves                         200K+  +1000%  Sports (active)
...
```

`python/google_trends.py` (US, past 12 months, compared on one scale):
```
air fryer    avg  64.4  latest  53  stable   +4.8%  peak 2026-04-12
             rising searches: best air fryer 2026, ninja crispi pro air fryer, ninja glass air fryer
instant pot  avg  20.8  latest  16  falling  -31.2%  peak 2026-04-12
             rising searches: how to use an instant pot, instant pot ice cream maker, instant pot pro
saved google_trends_timeline.csv (53 weeks)
```

`python/tech_stack.py`:
```
wordpress.org    cms=WordPress  shop=None  email=None  cdn=None  (4 technologies)
stripe.com       cms=None  shop=None  email=Google Workspace  cdn=None  (9 technologies)
hubspot.com      cms=HubSpot CMS  shop=None  email=Google Workspace  cdn=Cloudflare  (12 technologies)
```

## Tips
- **Budget cap:** every example passes a maximum charge for the run. The Actor stops cleanly when it's reached.
- **Failed items are free** on all four Actors (keywords Google can't serve, dead domains, blocked pages, filtered-out trends).
- **Schedules:** in Apify Console, save your input as a task and add a schedule, or schedule the script yourself.
- **AI agents:** each Actor is also available as an MCP tool, e.g.
  `https://mcp.apify.com?tools=zahidthani/google-trends-scraper`.

## Feedback
Found a bug in an example? Open an issue here. Problems with the data itself are best reported on the Actor's
**Issues** tab on Apify, where they're monitored daily.

## License
MIT. See [LICENSE](LICENSE).
