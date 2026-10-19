const fs = require('fs');

const html = fs.readFileSync('D:/projects/monly/АСТРА_АССЕТЫ/astra_main_app.html', 'utf8');

console.log('=== ASTRA MAIN APP INSPECTION ===');
console.log('File length:', html.length, 'characters');

// Find all IDs
const idRegex = /id=["']([^"']+)["']/g;
const ids = new Set();
let match;
while ((match = idRegex.exec(html)) !== null) {
  ids.add(match[1]);
}
console.log('\nTotal unique IDs:', ids.size);
console.log('Sample IDs:', Array.from(ids).slice(0, 40));

// Find all function declarations
const funcRegex = /function\s+([a-zA-Z0-9_]+)\s*\(/g;
const funcs = [];
while ((match = funcRegex.exec(html)) !== null) {
  funcs.push(match[1]);
}
console.log('\nTotal functions:', funcs.length);
console.log('Functions list:\n' + funcs.join(', '));

// Find all image sources
const srcRegex = /(?:src|href)=["']([^"']+\.(?:png|jpg|jpeg|svg|webp))["']/g;
const srcs = new Set();
while ((match = srcRegex.exec(html)) !== null) {
  srcs.add(match[1]);
}
console.log('\nStatic image references in HTML tags:', srcs.size);

// Look for image arrays in JS
const jsImageRegex = /['"]([^'"]+\.(?:png|jpg|jpeg|svg|webp))['"]/g;
const allImgRefs = new Set();
while ((match = jsImageRegex.exec(html)) !== null) {
  allImgRefs.add(match[1]);
}
console.log('Total image path strings in entire file:', allImgRefs.size);
