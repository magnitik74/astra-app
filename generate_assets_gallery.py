# -*- coding: utf-8 -*-
import os
import json

MANIFEST_FILE = r"D:\projects\monly\ОРИГИНАЛЬНЫЕ_АССЕТЫ_MOONLY\manifest_moonly_original_assets.json"
OUTPUT_HTML = r"D:\projects\monly\ОРИГИНАЛЬНЫЕ_АССЕТЫ_MOONLY\index.html"
OUTPUT_ROOT_HTML = r"D:\projects\monly\moonly_original_assets_gallery.html"

with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
    items = json.load(f)

# Sort by size descending
items.sort(key=lambda x: x["size_bytes"], reverse=True)

embedded_json = json.dumps(items, ensure_ascii=False)

html_template = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Moonly Original Assets Gallery — 1022 оригинальных файла</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0D0D12;
      --card-bg: #15151F;
      --card-border: rgba(255, 255, 255, 0.08);
      --gold: #F7B64D;
      --purple: #8A63FF;
      --text: #FFFFFF;
      --text-sub: #8E8E9E;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      padding: 24px;
      min-height: 100vh;
    }

    .header-bar {
      max-width: 1400px;
      margin: 0 auto 20px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .title-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      flex-wrap: wrap;
      gap: 12px;
    }

    .main-title {
      font-size: 26px;
      font-weight: 800;
      letter-spacing: -0.4px;
      background: linear-gradient(135deg, #FFFFFF 0%, #D8C7FF 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .sub-title {
      font-size: 13.5px;
      color: var(--text-sub);
      margin-top: 4px;
    }

    .stats-badge {
      background: rgba(247, 182, 77, 0.12);
      border: 1px solid rgba(247, 182, 77, 0.3);
      color: var(--gold);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 13px;
      font-weight: 700;
    }

    .controls-row {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
    }

    .search-box {
      flex: 1;
      min-width: 260px;
      height: 44px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 0 16px;
      color: #FFF;
      font-size: 14px;
      outline: none;
      transition: border-color 0.2s;
    }

    .search-box:focus {
      border-color: var(--purple);
    }

    .sort-select {
      height: 44px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 0 14px;
      color: #FFF;
      font-size: 13px;
      outline: none;
      cursor: pointer;
    }

    .category-pills {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      max-width: 1400px;
      margin: 0 auto 20px;
    }

    .cat-pill {
      padding: 8px 16px;
      border-radius: 14px;
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      color: var(--text-sub);
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      user-select: none;
    }

    .cat-pill:hover {
      color: #FFF;
      border-color: rgba(255, 255, 255, 0.2);
    }

    .cat-pill.active {
      background: var(--purple);
      border-color: var(--purple);
      color: #FFF;
      box-shadow: 0 4px 16px rgba(138, 99, 255, 0.35);
    }

    .grid-container {
      max-width: 1400px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
      gap: 16px;
    }

    .asset-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      overflow: hidden;
      cursor: pointer;
      transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
      display: flex;
      flex-direction: column;
    }

    .asset-card:hover {
      transform: translateY(-4px);
      border-color: rgba(247, 182, 77, 0.45);
      box-shadow: 0 12px 28px rgba(0, 0, 0, 0.65);
    }

    .asset-thumb-wrap {
      width: 100%;
      height: 180px;
      background: radial-gradient(circle at 50% 50%, #1A1A26 0%, #0C0C12 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
      padding: 8px;
    }

    .asset-thumb {
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
      transition: transform 0.25s ease;
      display: block;
    }

    .asset-card:hover .asset-thumb {
      transform: scale(1.06);
    }

    .badge-dim {
      position: absolute;
      bottom: 8px;
      left: 8px;
      background: rgba(0, 0, 0, 0.8);
      backdrop-filter: blur(8px);
      padding: 3px 8px;
      border-radius: 6px;
      font-size: 10px;
      font-weight: 700;
      color: #FFF;
    }

    .badge-size {
      position: absolute;
      top: 8px;
      right: 8px;
      background: rgba(247, 182, 77, 0.25);
      border: 1px solid rgba(247, 182, 77, 0.4);
      color: var(--gold);
      padding: 2px 7px;
      border-radius: 6px;
      font-size: 10px;
      font-weight: 800;
    }

    .asset-info {
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      flex: 1;
    }

    .asset-name {
      font-size: 12.5px;
      font-weight: 700;
      color: #FFF;
      word-break: break-all;
      line-height: 1.3;
    }

    .asset-cat {
      font-size: 11px;
      color: var(--text-sub);
    }

    .load-more-btn {
      display: block;
      margin: 32px auto 60px;
      padding: 14px 36px;
      border-radius: 24px;
      background: var(--purple);
      border: none;
      color: #FFF;
      font-size: 14px;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 6px 20px rgba(138, 99, 255, 0.4);
      transition: transform 0.18s, box-shadow 0.18s;
    }

    .load-more-btn:hover {
      transform: scale(1.03);
      box-shadow: 0 8px 26px rgba(138, 99, 255, 0.55);
    }

    /* Zoom Modal */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(5, 5, 8, 0.94);
      backdrop-filter: blur(14px);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 20px;
    }

    .modal-content {
      max-width: 900px;
      width: 100%;
      max-height: 90vh;
      background: #14141E;
      border: 1px solid rgba(255, 255, 255, 0.15);
      border-radius: 24px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      align-items: center;
      position: relative;
      box-shadow: 0 24px 60px rgba(0, 0, 0, 0.95);
      overflow-y: auto;
    }

    .modal-close-btn {
      position: absolute;
      top: 16px;
      right: 16px;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.1);
      border: none;
      color: #FFF;
      font-size: 18px;
      font-weight: 700;
      cursor: pointer;
    }

    .modal-img-wrap {
      width: 100%;
      max-height: 55vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: radial-gradient(circle at 50% 50%, #1F1F2E 0%, #0A0A10 100%);
      border-radius: 14px;
      padding: 16px;
      overflow: hidden;
    }

    .modal-img {
      max-width: 100%;
      max-height: 52vh;
      object-fit: contain;
    }

    .modal-meta-row {
      margin-top: 18px;
      width: 100%;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 12px;
    }

    .modal-title {
      font-size: 17px;
      font-weight: 800;
      color: #FFF;
      word-break: break-all;
    }

    .modal-details {
      font-size: 12.5px;
      color: var(--text-sub);
      margin-top: 4px;
    }

    .modal-copy-btn {
      padding: 10px 18px;
      border-radius: 14px;
      background: var(--purple);
      border: none;
      color: #FFF;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: background 0.2s;
    }
  </style>
</head>
<body>

  <div class="header-bar">
    <div class="title-row">
      <div>
        <h1 class="main-title">🌙 Moonly Original Assets Gallery</h1>
        <div class="sub-title">1022 оригинальных фона, иллюстрации, пейвола, аркана Таро и 3D-иконки из APK и веб-архивов</div>
      </div>
      <div class="stats-badge" id="stats-counter">Всего: 1022 файла (41.5 MB)</div>
    </div>

    <div class="controls-row">
      <input type="text" id="search-box" class="search-box" placeholder="🔍 Поиск по названию (например, female, tarot, paywall, bg, sun)..." oninput="handleSearch()">
      <select id="sort-select" class="sort-select" onchange="handleSort()">
        <option value="size-desc">Сортировка: Размер (сначала большие)</option>
        <option value="size-asc">Сортировка: Размер (сначала маленькие)</option>
        <option value="res-desc">Сортировка: Разрешение (сначала Ultra-HD)</option>
        <option value="name-asc">Сортировка: По имени (А-Я)</option>
      </select>
    </div>
  </div>

  <div class="category-pills" id="category-pills"></div>

  <div class="grid-container" id="grid"></div>

  <button class="load-more-btn" id="load-more-btn" onclick="loadMore()">Показать еще 48 файлов</button>

  <div class="modal-overlay" id="zoom-modal" onclick="closeModal(event)">
    <div class="modal-content" onclick="event.stopPropagation()">
      <button class="modal-close-btn" onclick="closeModal()">✕</button>
      <div class="modal-img-wrap">
        <img id="modal-img" class="modal-img" src="" alt="Zoom">
      </div>
      <div class="modal-meta-row">
        <div>
          <div class="modal-title" id="modal-title"></div>
          <div class="modal-details" id="modal-details"></div>
        </div>
        <button class="modal-copy-btn" id="modal-copy-btn" onclick="copyPath()">Копировать путь к файлу</button>
      </div>
    </div>
  </div>

  <script>
    const ALL_ITEMS = EMBEDDED_ITEMS_PLACEHOLDER;
    let currentCategory = 'all';
    let searchQuery = '';
    let currentSort = 'size-desc';
    let currentZoomItem = null;
    let visibleCount = 48;
    const PAGE_SIZE = 48;

    const CATEGORIES_DEF = [
      { id: 'all', label: 'Все файлы' },
      { id: '01_ФОНЫ_И_БАННЕРЫ_ВЫСОКОГО_РАЗРЕШЕНИЯ', label: '🌄 Фоны и Баннеры HD' },
      { id: '02_ИЛЛЮСТРАЦИИ_И_ОНБОРДИНГ', label: '🎨 Иллюстрации и Онбординг' },
      { id: '03_ПЕЙВОЛЫ_И_ПОДПИСКА', label: '👑 Пейволы и Тарифы' },
      { id: '04_ТАРО_И_РУНЫ', label: '🔮 Таро и Руны' },
      { id: '05_ЗОДИАК_И_НАТАЛЬНАЯ_КАРТА', label: '🪐 Зодиак и Натал' },
      { id: '06_МЕДИТАЦИИ_И_ПРАКТИКИ', label: '🧘 Медитации' },
      { id: '07_3D_ИКОНКИ_И_ЭЛЕМЕНТЫ', label: '✨ 3D-Иконки' },
      { id: '08_UI_И_ИНТЕРФЕЙС', label: '📱 UI Графика' }
    ];

    function initPills() {
      const container = document.getElementById('category-pills');
      container.innerHTML = '';
      
      const counts = {};
      ALL_ITEMS.forEach(it => counts[it.category] = (counts[it.category] || 0) + 1);

      CATEGORIES_DEF.forEach(cat => {
        const btn = document.createElement('div');
        btn.className = `cat-pill ${cat.id === currentCategory ? 'active' : ''}`;
        const cnt = cat.id === 'all' ? ALL_ITEMS.length : (counts[cat.id] || 0);
        btn.innerText = `${cat.label} (${cnt})`;
        btn.onclick = () => {
          currentCategory = cat.id;
          visibleCount = PAGE_SIZE;
          document.querySelectorAll('.cat-pill').forEach(p => p.classList.remove('active'));
          btn.classList.add('active');
          renderGrid();
        };
        container.appendChild(btn);
      });
    }

    function getFilteredList() {
      let filtered = ALL_ITEMS.filter(it => {
        if (currentCategory !== 'all' && it.category !== currentCategory) return false;
        if (searchQuery) {
          const q = searchQuery.toLowerCase();
          if (!it.filename.toLowerCase().includes(q) && !it.category.toLowerCase().includes(q)) return false;
        }
        return true;
      });

      if (currentSort === 'size-desc') filtered.sort((a,b) => b.size_bytes - a.size_bytes);
      else if (currentSort === 'size-asc') filtered.sort((a,b) => a.size_bytes - b.size_bytes);
      else if (currentSort === 'res-desc') filtered.sort((a,b) => (b.width * b.height) - (a.width * a.height));
      else if (currentSort === 'name-asc') filtered.sort((a,b) => a.filename.localeCompare(b.filename));

      return filtered;
    }

    function renderGrid() {
      const grid = document.getElementById('grid');
      grid.innerHTML = '';

      const filtered = getFilteredList();
      document.getElementById('stats-counter').innerText = `Показано: ${Math.min(visibleCount, filtered.length)} из ${filtered.length}`;

      const itemsToShow = filtered.slice(0, visibleCount);

      itemsToShow.forEach(it => {
        const card = document.createElement('div');
        card.className = 'asset-card';
        card.onclick = () => openModal(it);

        const dimText = (it.width && it.height) ? `${it.width}×${it.height}` : it.format;
        const sizeText = it.size_kb > 1024 ? `${(it.size_kb/1024).toFixed(1)} MB` : `${it.size_kb} KB`;

        card.innerHTML = `
          <div class="asset-thumb-wrap">
            <img class="asset-thumb" src="ОРИГИНАЛЬНЫЕ_АССЕТЫ_MOONLY/${it.rel_path}" alt="${it.filename}">
            <div class="badge-dim">${dimText}</div>
            <div class="badge-size">${sizeText}</div>
          </div>
          <div class="asset-info">
            <div class="asset-name">${it.filename}</div>
            <div class="asset-cat">${it.category.substring(3)}</div>
          </div>
        `;
        grid.appendChild(card);
      });

      const moreBtn = document.getElementById('load-more-btn');
      if (visibleCount < filtered.length) {
        moreBtn.style.display = 'block';
        moreBtn.innerText = `Показать еще (осталось ${filtered.length - visibleCount})`;
      } else {
        moreBtn.style.display = 'none';
      }
    }

    function loadMore() {
      visibleCount += PAGE_SIZE;
      renderGrid();
    }

    function handleSearch() {
      searchQuery = document.getElementById('search-box').value.trim();
      visibleCount = PAGE_SIZE;
      renderGrid();
    }

    function handleSort() {
      currentSort = document.getElementById('sort-select').value;
      renderGrid();
    }

    function openModal(item) {
      currentZoomItem = item;
      document.getElementById('modal-img').src = "ОРИГИНАЛЬНЫЕ_АССЕТЫ_MOONLY/" + item.rel_path;
      document.getElementById('modal-title').innerText = item.filename;
      const dim = (item.width && item.height) ? `${item.width} × ${item.height} px` : 'Вектор / N/A';
      document.getElementById('modal-details').innerText = `${dim} • ${item.size_kb} KB • Источник: ${item.source} • Папка: ${item.category}`;
      document.getElementById('zoom-modal').style.display = 'flex';
    }

    function closeModal() {
      document.getElementById('zoom-modal').style.display = 'none';
      currentZoomItem = null;
    }

    function copyPath() {
      if (!currentZoomItem) return;
      const fullPath = "D:\\\\projects\\\\monly\\\\ОРИГИНАЛЬНЫЕ_АССЕТЫ_MOONLY\\\\" + currentZoomItem.rel_path.split('/').join('\\\\');
      navigator.clipboard.writeText(fullPath).then(() => {
        const btn = document.getElementById('modal-copy-btn');
        btn.innerText = '✓ Скопировано в буфер!';
        setTimeout(() => btn.innerText = 'Копировать путь к файлу', 2000);
      });
    }

    window.addEventListener('DOMContentLoaded', () => {
      initPills();
      renderGrid();
    });
  </script>
</body>
</html>"""

final_html = html_template.replace("EMBEDDED_ITEMS_PLACEHOLDER", embedded_json)

# Root gallery
with open(OUTPUT_ROOT_HTML, "w", encoding="utf-8") as f:
    f.write(final_html)

# Inner gallery
inner_html = final_html.replace('src="ОРИГИНАЛЬНЫЕ_АССЕТЫ_MOONLY/${it.rel_path}"', 'src="${it.rel_path}"').replace('document.getElementById(\'modal-img\').src = "ОРИГИНАЛЬНЫЕ_АССЕТЫ_MOONLY/" + item.rel_path;', 'document.getElementById(\'modal-img\').src = item.rel_path;')
with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
    f.write(inner_html)

print("Both gallery files written successfully.")
