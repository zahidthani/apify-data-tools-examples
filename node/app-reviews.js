// Recent App Store + Google Play reviews for one app, plus the built-in insights summary.
// Actor: https://apify.com/zahidthani/app-store-google-play-reviews
// Cost:  $0.005 per run + $0.12 per 1,000 reviews + $0.005 per app summary. This example: about $0.02.
//
//   export APIFY_TOKEN=your_token
//   node app-reviews.js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const input = {
    apps: ['Duolingo'], // app name, store URL, App Store ID or package name
    stores: ['apple', 'google'],
    countries: ['us'],
    maxReviewsPerApp: 20, // per store and country
    sort: 'newest',
    // reviewsSince: '7 days', maxRating: 2,
};

const run = await client.actor('zahidthani/app-store-google-play-reviews').call(input, { maxTotalChargeUsd: 0.1 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();

const reviews = items.filter((i) => i.type === 'review');
console.log(`${reviews.length} reviews`);
for (const r of reviews.slice(0, 5)) {
    console.log(`  [${r.store}] ${r.rating}★ ${(r.title || r.text || '').slice(0, 70)}`);
}

for (const s of items.filter((i) => i.type === 'appSummary')) {
    const themes = s.complaintThemes.slice(0, 3).map((t) => `${t.theme} (${t.reviews})`).join(', ') || '-';
    console.log(`${s.store.padEnd(6)} ${s.name}: rating ${s.rating.toFixed(2)}, ${(s.negativeShare * 100).toFixed(0)}% 1-2★; complaints: ${themes}`);
}
