const fs = require('fs');
const path = require('path');

const srcDir = 'C:/Users/Александр/Downloads/moonly_extracted/apk_contents/res/drawable';
const srcNodpi = 'C:/Users/Александр/Downloads/moonly_extracted/apk_contents/res/drawable-nodpi-v4';
const destDir = 'D:/projects/monly/АСТРА_АССЕТЫ/moonly_3d_icons';

if (!fs.existsSync(destDir)) {
  fs.mkdirSync(destDir, { recursive: true });
}

let count = 0;
for (let i = 1; i <= 29; i++) {
  const srcFile = i === 15 ? path.join(srcDir, 'full_moon_15.png') : path.join(srcDir, 'moon' + i + '.png');
  if (fs.existsSync(srcFile)) {
    fs.copyFileSync(srcFile, path.join(destDir, 'moon_' + i + '.png'));
    fs.copyFileSync(srcFile, path.join(destDir, 'moon' + i + '.png'));
    count++;
  } else {
    console.warn('Missing: ' + srcFile);
  }
}

const moon30 = path.join(srcNodpi, 'new_moon_30.png');
if (fs.existsSync(moon30)) {
  fs.copyFileSync(moon30, path.join(destDir, 'moon_30.png'));
  fs.copyFileSync(moon30, path.join(destDir, 'moon30.png'));
  count++;
}

// Also check for calendar icon
const icCal = path.join(srcNodpi, 'ic_calendar_v2_moon_header.png');
if (fs.existsSync(icCal)) {
  fs.copyFileSync(icCal, path.join(destDir, 'ic_calendar_v2_moon_header.png'));
  console.log('Copied calendar header icon');
}

console.log('Successfully copied ' + count + ' authentic 3D moon spheres!');
