// What is trending on Google right now? Biggest trends by search volume for one country.
// Actor: https://apify.com/zahidthani/google-trends-trending-now
// Cost:  $0.005 per run + $0.001 per trend delivered. This example (10 trends): about $0.015.
// Set maxItemsPerCountry: 0 for the full list (often 300-500 trends per country per day).
//
//   export APIFY_TOKEN=your_token
//   node trending-now.js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const input = {
    countries: ['US'],
    timeWindow: '24', // 4, 24, 48 or 168 hours
    sortBy: 'volume',
    maxItemsPerCountry: 10,
    // categories: ['Technology'],
    // onlyNew: true, monitorName: 'my-alerts', // scheduled alerts without repeats
};

const run = await client.actor('zahidthani/google-trends-trending-now').call(input, { maxTotalChargeUsd: 0.05 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();

for (const t of items) {
    const status = t.isActive ? 'active' : 'ended';
    console.log(`${String(t.rank).padStart(3)}. ${t.keyword.padEnd(40)} ${t.searchVolumeLabel.padStart(6)}  +${t.increasePercent}%  ${t.categories[0] ?? '-'} (${status})`);
}
