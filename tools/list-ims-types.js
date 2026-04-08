#!/usr/bin/env node
/**
 * Lists all Equipment Type and Subtype options from the IMS search page.
 * Opens headed browser so you can see it working.
 */

const puppeteer = require('puppeteer');
const DELAY = (ms) => new Promise(r => setTimeout(r, ms));

(async () => {
    const browser = await puppeteer.launch({ headless: false, defaultViewport: null });
    const page = await browser.newPage();

    console.log('Opening IMS search page...');
    await page.goto('https://ims.internationalprocessplants.com/search?asset=equipment', {
        waitUntil: 'networkidle2',
        timeout: 30000
    });
    await DELAY(3000);

    // Close welcome modal
    console.log('Closing welcome modal...');
    await page.evaluate(() => {
        const radios = document.querySelectorAll('input[type="radio"]');
        for (const radio of radios) {
            const label = radio.closest('li')?.querySelector('label')?.textContent || '';
            if (label.includes('US')) { radio.click(); return; }
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

    // Get all equipment types
    console.log('\nOpening Equipment Type dropdown...');
    // Find the type dropdown flexibly
    const typeDropdownClicked = await page.evaluate(() => {
        // Try by ID first
        const byId = document.querySelector('#EquipmentTypeDropdown');
        if (byId) { byId.click(); return true; }
        // Try by looking for dropdown with "Equipment Type" label nearby
        const dds = document.querySelectorAll('.k-dropdownlist');
        for (const dd of dds) {
            const text = dd.querySelector('.k-input-value-text')?.textContent || '';
            if (text.includes('Equipment Type') || text.includes('Select') || text.includes('All Equipment')) {
                dd.click();
                return true;
            }
        }
        // Just click the first dropdown
        if (dds.length > 0) { dds[0].click(); return true; }
        return false;
    });
    if (!typeDropdownClicked) {
        console.error('Could not find equipment type dropdown');
        // Dump page HTML for debugging
        const html = await page.content();
        console.log('Page snippet:', html.substring(0, 2000));
        await browser.close();
        process.exit(1);
    }
    await DELAY(1500);

    const types = await page.evaluate(() => {
        const items = document.querySelectorAll('.k-list-item, .k-item, li[role="option"]');
        return Array.from(items).map(item => item.textContent.trim());
    });

    console.log(`\n${'='.repeat(60)}`);
    console.log('EQUIPMENT TYPES (' + types.length + ' total):');
    console.log('='.repeat(60));
    types.forEach((t, i) => console.log(`  ${i + 1}. "${t}"`));

    // For each type, get subtypes
    const results = {};
    for (const typeName of types) {
        // Click the type dropdown and select this type
        await page.evaluate(() => {
            const byId = document.querySelector('#EquipmentTypeDropdown');
            if (byId) { byId.click(); return; }
            const dds = document.querySelectorAll('.k-dropdownlist');
            if (dds.length > 0) dds[0].click();
        });
        await DELAY(1000);

        await page.evaluate((target) => {
            const items = document.querySelectorAll('.k-list-item, .k-item, li[role="option"]');
            for (const item of items) {
                if (item.textContent.trim() === target) { item.click(); return; }
            }
        }, typeName);
        await DELAY(2500);

        // Try to find and open subtype dropdown
        const subtypeClicked = await page.evaluate(() => {
            const dds = document.querySelectorAll('.k-dropdownlist');
            for (const dd of dds) {
                const id = dd.id || '';
                if (id === 'EquipmentTypeDropdown') continue;
                const text = dd.querySelector('.k-input-value-text')?.textContent || '';
                if (text.includes('All') || text.includes('Subtype') || text.includes('Select')) {
                    dd.click();
                    return true;
                }
            }
            // Also try any second dropdown
            const allDds = Array.from(dds).filter(dd => (dd.id || '') !== 'EquipmentTypeDropdown');
            if (allDds.length > 0) {
                allDds[0].click();
                return true;
            }
            return false;
        });

        if (subtypeClicked) {
            await DELAY(1000);
            const subtypes = await page.evaluate(() => {
                const items = document.querySelectorAll('.k-list-item, .k-item, li[role="option"]');
                return Array.from(items).map(item => item.textContent.trim());
            });
            results[typeName] = subtypes;

            // Close the dropdown by clicking elsewhere
            await page.evaluate(() => document.body.click());
            await DELAY(500);
        } else {
            results[typeName] = ['(no subtype dropdown)'];
        }
    }

    console.log(`\n${'='.repeat(60)}`);
    console.log('COMPLETE TYPE → SUBTYPE MAPPING:');
    console.log('='.repeat(60));
    for (const [type, subtypes] of Object.entries(results)) {
        console.log(`\n  TYPE: "${type}"`);
        if (subtypes.length === 0 || (subtypes.length === 1 && subtypes[0] === '(no subtype dropdown)')) {
            console.log('    (no subtypes)');
        } else {
            subtypes.forEach((s, i) => console.log(`    ${i + 1}. "${s}"`));
        }
    }

    // Output as JSON for easy parsing
    const fs = require('fs');
    const outPath = require('path').join(__dirname, '..', 'data', 'ims-type-subtype-map.json');
    fs.writeFileSync(outPath, JSON.stringify(results, null, 2));
    console.log(`\nJSON saved to: ${outPath}`);

    await browser.close();
})();
