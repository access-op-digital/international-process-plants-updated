// Format/size optimization of the original photographs. No generated imagery.
const fs = require('node:fs');
const path = require('node:path');
const sharp = require(process.env.SHARP_MODULE || 'sharp');
const root = path.resolve(__dirname, '..');
const records = JSON.parse(fs.readFileSync(path.join(root, 'docs/chemical-build/inventory-detail.json'), 'utf8'));
(async () => {
  for (const row of records) {
    if (!row.local_image) { delete row.detail_text; continue; }
    const out = path.join(root, 'public', row.local_image);
    await sharp(path.join(root, row.original_asset)).rotate().resize({width:900, height:650, fit:'inside', withoutEnlargement:true}).webp({quality:80}).toFile(out);
    const {width,height} = await sharp(out).metadata();
    row.image_width = width; row.image_height = height;
    row.image_bytes = fs.statSync(out).size;
    if(row.image_bytes > 200000) throw new Error(`Image over budget: ${row.id}`);
    delete row.detail_text;
  }
  fs.writeFileSync(path.join(root, 'docs/chemical-build/inventory.json'), JSON.stringify(records,null,2));
  console.log('Encoded and checked', records.length, 'original listing images below 200 KB each.');
})();
