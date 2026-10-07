// Which of these websites run Shopify, WordPress, HubSpot...? And which email provider does each company use?
// Actor: https://apify.com/zahidthani/website-tech-stack-detector
// Cost:  $0.0005 per run + $0.002 per website analysed (dead and blocked sites are free). This example: under $0.01.
//
//   export APIFY_TOKEN=your_token
//   node tech-stack.js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });

const input = {
    websites: ['wordpress.org', 'hubspot.com', 'jane@stripe.com'], // domains, URLs or work emails
    includeDns: true, // email provider, DNS host, verified SaaS tools
    // proxyConfiguration: { useApifyProxy: true, apifyProxyGroups: ['RESIDENTIAL'] }, // sites that block cloud IPs
};

const run = await client.actor('zahidthani/website-tech-stack-detector').call(input, { maxTotalChargeUsd: 0.05 });
const { items } = await client.dataset(run.defaultDatasetId).listItems();

for (const s of items) {
    if (s.type !== 'website') {
        console.log(`${s.input.padEnd(16)} not analysed (free): ${s.error}`);
        continue;
    }
    console.log(`${s.domain.padEnd(16)} cms=${s.cms}  shop=${s.ecommercePlatform}  email=${s.emailProvider}  cdn=${s.cdn}  (${s.technologyCount} technologies)${s.pageBlocked ? '  [blocked: DNS only, free]' : ''}`);
}
