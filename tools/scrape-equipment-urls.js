#!/usr/bin/env node
/**
 * IPP IMS Equipment URL Scraper
 *
 * Scrapes all product URLs for a given equipment type and subtype
 * from the IPP IMS inventory system.
 *
 * Usage:
 *   node scrape-equipment-urls.js --type "Reactor" --subtype "Batch-Type Agitated"
 *   node scrape-equipment-urls.js --type "Reactor" --subtype "Batch-Type Agitated" --output ../data/reactors/batch-type-agitated/urls.txt
 *   node scrape-equipment-urls.js --type "Agitator" --subtype "Glass Drives" --headless
 *
 * Options:
 *   --type       Equipment type (e.g., "Reactor", "Agitator", "Heat Exchanger")
 *   --subtype    Equipment subtype (e.g., "Batch-Type Agitated", "Glass Drives")
 *   --output     Output file path (default: stdout)
 *   --headless   Run browser in headless mode (default: visible)
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

const DELAY = (ms) => new Promise(r => setTimeout(r, ms));

function parseArgs() {
    const args = process.argv.slice(2);
    const opts = { headless: false };
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--type' && args[i + 1]) opts.type = args[++i];
        else if (args[i] === '--subtype' && args[i + 1]) opts.subtype = args[++i];
        else if (args[i] === '--output' && args[i + 1]) opts.output = args[++i];
        else if (args[i] === '--headless') opts.headless = true;
    }
    if (!opts.type) {
        console.error('Usage: node scrape-equipment-urls.js --type "Reactor" [--subtype "Batch-Type Agitated"] [--output file.txt] [--headless]');
        process.exit(1);
    }
    return opts;
}

(async () => {
    const opts = parseArgs();
    const browser = await puppeteer.launch({ headless: opts.headless, defaultViewport: null });
    const page = await browser.newPage();

    console.log(`Scraping IPP IMS: ${opts.type}${opts.subtype ? ' > ' + opts.subtype : ' (all subtypes)'}`);
    console.log('1. Opening IMS search page...');
    await page.goto('https://ims.internationalprocessplants.com/search?asset=equipment', {
        waitUntil: 'networkidle2',
        timeout: 30000
    });
    await DELAY(3000);

    // Step 1: Handle Welcome modal — select US/Standard and close
    console.log('2. Selecting US/Standard and closing welcome modal...');
    await page.evaluate(() => {
        const radios = document.querySelectorAll('input[type="radio"]');
        for (const radio of radios) {
            const label = radio.closest('li')?.querySelector('label')?.textContent || '';
            const parentText = radio.parentElement?.parentElement?.textContent || '';
            if (label.includes('US') || parentText.includes('US')) {
                radio.click();
                return;
            }
        }
    });
    await DELAY(500);
    await page.evaluate(() => {
        const buttons = document.querySelectorAll('button');
        for (const btn of buttons) {
            if (btn.textContent.trim() === 'Close') { btn.click(); return; }
        }
    });
    await DELAY(2000);

    // Step 2: Select Equipment Type
    console.log(`3. Selecting Equipment Type: ${opts.type}...`);
    await page.click('#EquipmentTypeDropdown');
    await DELAY(1500);
    const typeResult = await page.evaluate((targetType) => {
        const items = document.querySelectorAll('.k-list-item, .k-item, li[role="option"]');
        const available = [];
        // Normalize for comparison: lowercase, collapse whitespace, strip special chars
        const normalize = (s) => s.toLowerCase().replace(/[&]/g, 'and').replace(/[-–—]/g, ' ').replace(/\s+/g, ' ').trim();
        const target = normalize(targetType);
        for (const item of items) {
            const text = item.textContent.trim();
            available.push(text);
            if (text === targetType) { item.click(); return { found: true, matched: text }; }
        }
        // Fuzzy: try normalized match
        for (const item of items) {
            const text = item.textContent.trim();
            if (normalize(text) === target) { item.click(); return { found: true, matched: text }; }
        }
        // Fuzzy: try includes
        for (const item of items) {
            const text = item.textContent.trim();
            if (normalize(text).includes(target) || target.includes(normalize(text))) { item.click(); return { found: true, matched: text }; }
        }
        return { found: false, available };
    }, opts.type);
    if (!typeResult.found) {
        console.error(`ERROR: Could not find equipment type "${opts.type}"`);
        console.error('Available types:', typeResult.available.join(', '));
        await browser.close();
        process.exit(1);
    }
    console.log(`   Matched: "${typeResult.matched}"`);
    await DELAY(3000);

    // Step 3: Select Equipment Subtype (if provided)
    if (opts.subtype) {
        console.log(`4. Selecting Equipment Subtype: ${opts.subtype}...`);
        const subtypeClicked = await page.evaluate(() => {
            const allText = document.querySelectorAll('h4, .filterRow h4');
            for (const el of allText) {
                if (el.textContent.includes('Subtype') || el.textContent.includes('Equipment Subtype')) {
                    const container = el.closest('.filtersContainer') || el.closest('div')?.parentElement;
                    const dd = container?.querySelector('.k-dropdownlist');
                    if (dd) { dd.click(); return true; }
                }
            }
            const dds = document.querySelectorAll('.k-dropdownlist');
            for (const dd of dds) {
                const text = dd.querySelector('.k-input-value-text')?.textContent || '';
                const id = dd.id || '';
                if (id !== 'EquipmentTypeDropdown' && (text.includes('All') || text.includes('Subtype'))) {
                    dd.click();
                    return true;
                }
            }
            return false;
        });
        if (!subtypeClicked) {
            console.error('ERROR: Could not find subtype dropdown');
            await browser.close();
            process.exit(1);
        }
        await DELAY(1500);

        const subtypeResult = await page.evaluate((targetSubtype) => {
            const items = document.querySelectorAll('.k-list-item, .k-item, li[role="option"]');
            const available = [];
            const normalize = (s) => s.toLowerCase().replace(/[&]/g, 'and').replace(/[-–—]/g, ' ').replace(/[\/]/g, ' ').replace(/\s+/g, ' ').trim();
            const target = normalize(targetSubtype);
            for (const item of items) {
                const text = item.textContent.trim();
                available.push(text);
                if (text === targetSubtype) { item.click(); return { found: true, matched: text }; }
            }
            for (const item of items) {
                const text = item.textContent.trim();
                if (normalize(text) === target) { item.click(); return { found: true, matched: text }; }
            }
            for (const item of items) {
                const text = item.textContent.trim();
                if (normalize(text).includes(target) || target.includes(normalize(text))) { item.click(); return { found: true, matched: text }; }
            }
            return { found: false, available };
        }, opts.subtype);
        if (!subtypeResult.found) {
            console.error(`ERROR: Could not find subtype "${opts.subtype}"`);
            console.error('Available subtypes:', subtypeResult.available.join(', '));
            await browser.close();
            process.exit(1);
        }
        console.log(`   Matched: "${subtypeResult.matched}"`);
        await DELAY(4000);
    } else {
        console.log('4. No subtype specified — using all subtypes for this type.');
        await DELAY(2000);
    }

    // Check result count
    let paginationInfo = await page.evaluate(() => {
        const text = document.body.innerText;
        const match = text.match(/(\d+)\s*-\s*(\d+)\s*of\s*(\d+)\s*items/);
        return match ? { start: parseInt(match[1]), end: parseInt(match[2]), total: parseInt(match[3]) } : null;
    });
    console.log(`   Results: ${paginationInfo ? paginationInfo.total + ' items' : 'unknown'}`);

    // Step 4: Set items per page to 100
    console.log('5. Setting items per page to 100...');
    const ippClicked = await page.evaluate(() => {
        const dds = document.querySelectorAll('.k-dropdownlist');
        for (const dd of dds) {
            const text = dd.querySelector('.k-input-value-text')?.textContent?.trim();
            if (text === '25' || text === '50') { dd.click(); return true; }
        }
        return false;
    });
    await DELAY(1000);
    if (ippClicked) {
        await page.evaluate(() => {
            const items = document.querySelectorAll('.k-list-item, .k-item, li[role="option"]');
            for (const item of items) {
                if (item.textContent.trim() === '100') { item.click(); return; }
            }
        });
        await DELAY(4000);
    }

    // Step 5: Extract stock numbers from all pages
    let allStockNumbers = [];
    let pageNum = 1;

    while (true) {
        console.log(`\n6. Extracting from page ${pageNum}...`);
        await DELAY(2000);

        const stockNumbers = await page.evaluate(() => {
            const links = document.querySelectorAll('a[href*="/inventory/equipment/detail/"], a.productLink');
            const ids = new Set();
            for (const link of links) {
                const href = link.href || link.getAttribute('href') || '';
                const match = href.match(/\/detail\/(\d+)/);
                if (match) ids.add(match[1]);
            }
            return Array.from(ids);
        });

        console.log(`   Found ${stockNumbers.length} stock numbers`);
        allStockNumbers.push(...stockNumbers);

        paginationInfo = await page.evaluate(() => {
            const text = document.body.innerText;
            const match = text.match(/(\d+)\s*-\s*(\d+)\s*of\s*(\d+)\s*items/);
            return match ? { start: parseInt(match[1]), end: parseInt(match[2]), total: parseInt(match[3]) } : null;
        });

        if (!paginationInfo || paginationInfo.end >= paginationInfo.total) {
            console.log('   Last page reached.');
            break;
        }

        const nextClicked = await page.evaluate(() => {
            const arrows = document.querySelectorAll('.k-i-caret-alt-right, .k-svg-i-caret-alt-right, .k-i-arrow-60-right');
            for (const arrow of arrows) {
                const btn = arrow.closest('button, a');
                if (btn) { btn.click(); return true; }
            }
            const pagerButtons = document.querySelectorAll('button[aria-label*="next" i], button[title*="next" i], a[aria-label*="next" i]');
            for (const btn of pagerButtons) { btn.click(); return true; }
            return false;
        });

        if (!nextClicked) { console.log('   No next button found.'); break; }
        pageNum++;
        await DELAY(3000);
    }

    const unique = [...new Set(allStockNumbers)];
    console.log(`\n========================================`);
    console.log(`TOTAL: ${unique.length} unique stock numbers`);
    console.log(`========================================`);

    const base = 'https://ims.internationalprocessplants.com/inventory/equipment/detail/';
    const urls = unique.map(id => base + id);
    const output = urls.join('\n') + '\n';

    if (opts.output) {
        const dir = path.dirname(opts.output);
        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(opts.output, output);
        console.log(`Written to ${opts.output}`);
    } else {
        process.stdout.write(output);
    }

    await browser.close();
})();
