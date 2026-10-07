// Google Trends for a few keywords: trend summary + rising related searches per keyword.
// Actor: https://apify.com/zahidthani/google-trends-scraper
// Cost:  $0.01 per run + $0.004 per keyword (failed keywords are free). This example: about $0.02.
//
//   export APIFY_TOKEN=your_token
//   node google-trends.js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const input = {
    searchTerms: ['air fryer', 'instant pot'],
    geo: 'US', // '' = worldwide
    timeRange: 'today 12-m', // now 7-d, today 3-m, today 5-y, all ...
    compareTerms: true, // one shared 0-100 scale
    includeInterestByRegion: false,
    includeRelatedTopics: false,
};

const run = await client.actor('zahidthani/google-trends-scraper').call(input, { maxTotalChargeUsd: 0.1 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();

for (const item of items) {
    if (item.status !== 'ok') {
        console.log('failed (not charged):', item.searchTerm, item.errors);
        continue;
    }
    const s = item.summary;
    console.log(`${item.searchTerm.padEnd(12)} avg ${s.average}  latest ${s.latest}  ${s.trend}  ${s.changePercent}%  peak ${s.peak.date.slice(0, 10)}`);
    console.log('   rising:', item.relatedQueries.rising.slice(0, 3).map((q) => q.query).join(', ') || '-');
}
