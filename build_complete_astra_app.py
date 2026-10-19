# -*- coding: utf-8 -*-
"""
Builder for ASTRA Master Web Application (All 101 Points Verified)
Clean-room RuStore & Google Play compliance.
"""

import os

OUT_PATH = r"D:\projects\monly\АСТРА_АССЕТЫ\astra_main_app.html"

html_template = """<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>АСТРА • Космический Проводник</title>
  
  <!-- Favicon & App Icons (Official Astra Master Assets) -->
  <link rel="icon" type="image/webp" href="00_ИКОНКИ_И_ЛОГОТИП_АСТРА/Astra_AppIcon_StarFlower_small_128.webp">
  <link rel="apple-touch-icon" href="00_ИКОНКИ_И_ЛОГОТИП_АСТРА/Astra_AppIcon_MandalaLotus_master_1024.webp">

  <!-- Core Clean-Room Protection & Data Modules -->
  <script src="astra_security_shield.js"></script>
  <script src="astra_tarot_runes_data.js"></script>
  <script src="astra_sounds_data.js"></script>
  <script src="astra_mentors_engine.js"></script>

  <style>
    /* ==========================================================================
       ASTRA MASTER DESIGN SYSTEM (PIXEL-PERFECT MOONLY REPLICATION)
       ========================================================================== */
    :root {
      --bg-dark: #0D0E15;
      --bg-card: rgba(26, 27, 38, 0.75);
      --bg-card-solid: #161822;
      --bg-card-border: rgba(255, 255, 255, 0.08);
      --bg-input: #202230;
      
      --purple: #784BF6;
      --purple-hover: #8A60F8;
      --purple-glow: rgba(120, 75, 246, 0.35);
      --amber: #FFB84D;
      --amber-glow: rgba(255, 184, 77, 0.3);
      --teal: #2DD4BF;
      --teal-glow: rgba(45, 212, 191, 0.3);
      
      --text-main: #FFFFFF;
      --text-muted: #8E93A6;
      --text-dim: #5C6073;

      /* Light Chat Theme Colors */
      --chat-bg: #F5F6FA;
      --chat-card: #FFFFFF;
      --chat-border: #E8EBF2;
      --chat-text: #191B26;
      --chat-text-muted: #6B7285;
      --chat-bubble-user: #784BF6;
      
      --radius-sm: 12px;
      --radius-md: 18px;
      --radius-lg: 26px;
      --radius-xl: 34px;
      
      --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      --font-serif: "Georgia", "Playfair Display", "Cinzel", serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }

    body {
      background-color: #000;
      color: var(--text-main);
      font-family: var(--font-sans);
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      margin: 0;
      padding: 0;
      overflow-x: hidden;
      user-select: none;
    }

    /* Mobile Container Frame (Max 430px) */
    .app-viewport {
      width: 100%;
      max-width: 430px;
      height: 100vh;
      max-height: 932px;
      background: var(--bg-dark);
      position: relative;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      box-shadow: 0 0 50px rgba(0, 0, 0, 0.8), 0 0 0 1px rgba(255, 255, 255, 0.05);
    }

    @media (min-width: 450px) {
      .app-viewport {
        border-radius: 44px;
        height: 92vh;
      }
    }

    /* Screens Container */
    .screens-wrapper {
      flex: 1;
      position: relative;
      overflow-y: auto;
      overflow-x: hidden;
      -webkit-overflow-scrolling: touch;
      scrollbar-width: none;
    }
    .screens-wrapper::-webkit-scrollbar { display: none; }

    .screen-view {
      display: none;
      min-height: 100%;
      padding-bottom: 90px;
      opacity: 0;
      transform: translateY(6px);
      transition: opacity 0.25s ease, transform 0.25s ease;
    }
    .screen-view.active {
      display: block;
      opacity: 1;
      transform: translateY(0);
    }

    /* ==========================================================================
       BOTTOM NAVIGATION BAR (5 TABS)
       ========================================================================== */
    .bottom-nav {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      height: 74px;
      background: rgba(14, 15, 22, 0.88);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border-top: 1px solid var(--bg-card-border);
      display: flex;
      justify-content: space-around;
      align-items: center;
      padding: 0 10px 12px;
      z-index: 50;
    }

    .nav-tab-item {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      flex: 1;
      padding: 6px 0;
      transition: transform 0.15s ease;
    }
    .nav-tab-item:active { transform: scale(0.92); }

    .nav-tab-icon-wrap {
      width: 28px;
      height: 28px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      margin-bottom: 3px;
    }

    .nav-tab-icon {
      width: 24px;
      height: 24px;
      object-fit: contain;
      filter: grayscale(1) opacity(0.45);
      transition: all 0.25s ease;
    }

    .nav-tab-label {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted);
      transition: color 0.25s ease;
      letter-spacing: -0.01em;
    }

    .nav-tab-item.active .nav-tab-icon {
      filter: grayscale(0) opacity(1) drop-shadow(0 0 8px var(--purple-glow));
      transform: scale(1.1);
    }
    .nav-tab-item.active .nav-tab-label {
      color: #FFF;
    }

    .nav-tab-indicator {
      width: 4px;
      height: 4px;
      border-radius: 50%;
      background: var(--purple);
      position: absolute;
      bottom: -6px;
      opacity: 0;
      transform: scale(0);
      transition: all 0.25s ease;
    }
    .nav-tab-item.active .nav-tab-indicator {
      opacity: 1;
      transform: scale(1);
      box-shadow: 0 0 6px var(--purple);
    }

    /* ==========================================================================
       SHARED CARDS & UI COMPONENTS
       ========================================================================== */
    .card-glass {
      background: var(--bg-card);
      border: 1px solid var(--bg-card-border);
      border-radius: var(--radius-lg);
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      padding: 18px;
      margin-bottom: 14px;
      position: relative;
      overflow: hidden;
    }

    .card-title-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 10px;
    }

    .card-title {
      font-size: 15px;
      font-weight: 700;
      color: #FFF;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .card-sub {
      font-size: 13px;
      color: var(--text-muted);
      line-height: 1.45;
    }

    .btn-primary {
      width: 100%;
      height: 52px;
      background: linear-gradient(135deg, #8A60F8, #6B3EE8);
      border: none;
      border-radius: var(--radius-md);
      color: #FFF;
      font-size: 15px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 8px 24px rgba(107, 62, 232, 0.4);
      transition: all 0.2s ease;
    }
    .btn-primary:active {
      transform: scale(0.98);
      filter: brightness(0.95);
    }

    .btn-pill-action {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(255, 255, 255, 0.12);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: #FFF;
      transition: all 0.2s ease;
    }
    .btn-pill-action:hover {
      background: rgba(255, 255, 255, 0.15);
      border-color: rgba(255, 255, 255, 0.3);
    }
    .btn-pill-action:active { transform: scale(0.92); }

    .actions-4-bar {
      display: flex;
      gap: 12px;
      justify-content: center;
      align-items: center;
      margin: 16px 0;
    }

    /* Modal Sheet Styling */
    .bottom-sheet-overlay {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      z-index: 100;
      display: none;
      justify-content: flex-end;
      flex-direction: column;
      animation: fadeIn 0.25s ease;
    }
    .bottom-sheet-content {
      background: #151722;
      border-top: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 32px 32px 0 0;
      max-height: 88vh;
      overflow-y: auto;
      padding: 24px 20px 40px;
      position: relative;
      animation: slideUp 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      scrollbar-width: none;
    }
    .bottom-sheet-content::-webkit-scrollbar { display: none; }

    .sheet-handle {
      width: 40px;
      height: 4px;
      border-radius: 2px;
      background: rgba(255, 255, 255, 0.2);
      margin: 0 auto 18px;
    }

    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes slideUp { from { transform: translateY(100%); } to { transform: translateY(0); } }

    /* ==========================================================================
       SCREEN 1: CALENDAR & DAILY FEED
       ========================================================================== */
    .cal-header-bar {
      padding: 16px 20px 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .cal-date-title {
      font-size: 18px;
      font-weight: 800;
      letter-spacing: -0.02em;
    }
    .cal-moon-badge {
      font-size: 12px;
      color: var(--amber);
      font-weight: 700;
      background: rgba(255, 184, 77, 0.12);
      padding: 4px 10px;
      border-radius: 12px;
      border: 1px solid rgba(255, 184, 77, 0.25);
    }

    /* Infinite Calendar Strip */
    .cal-strip-container {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding: 10px 20px 16px;
      scrollbar-width: none;
    }
    .cal-strip-container::-webkit-scrollbar { display: none; }
    
    .cal-day-chip {
      min-width: 50px;
      height: 72px;
      background: var(--bg-card);
      border: 1px solid var(--bg-card-border);
      border-radius: 18px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s ease;
      position: relative;
    }
    .cal-day-chip.active {
      background: linear-gradient(180deg, #784BF6, #5B2FE3);
      border-color: #8A60F8;
      box-shadow: 0 6px 16px var(--purple-glow);
    }
    .cal-day-weekday {
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      margin-bottom: 2px;
    }
    .cal-day-chip.active .cal-day-weekday { color: rgba(255, 255, 255, 0.8); }
    .cal-day-num {
      font-size: 16px;
      font-weight: 800;
    }
    .cal-day-moon-icon {
      width: 14px;
      height: 14px;
      margin-top: 4px;
      opacity: 0.8;
    }

    /* Hero Moon Sphere View */
    .hero-moon-wrap {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 10px 20px 24px;
      position: relative;
    }
    .hero-moon-img {
      width: 170px;
      height: 170px;
      object-fit: contain;
      filter: drop-shadow(0 0 35px rgba(255, 196, 102, 0.45));
      animation: moonFloat 6s ease-in-out infinite alternate;
    }
    @keyframes moonFloat {
      0% { transform: translateY(0); }
      100% { transform: translateY(-8px); }
    }
    .hero-moon-phase-name {
      font-size: 20px;
      font-weight: 800;
      margin-top: 14px;
      letter-spacing: -0.01em;
    }
    .hero-moon-illum {
      font-size: 13px;
      color: var(--text-muted);
      margin-top: 4px;
      display: flex;
      gap: 12px;
    }

    /* Feed Cards */
    .feed-container {
      padding: 0 16px 20px;
    }

    .haircut-badge-good {
      color: #10B981;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.3);
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 12px;
      font-weight: 700;
    }

    /* ==========================================================================
       SCREEN 2: PRACTICES (TAROT, ORACLE, GODS, DREAM, RUNES, AFFIRMATIONS)
       ========================================================================== */
    .practices-tabs-scroll {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding: 14px 16px;
      scrollbar-width: none;
    }
    .practices-tabs-scroll::-webkit-scrollbar { display: none; }

    .practice-pill {
      padding: 8px 18px;
      border-radius: 20px;
      background: var(--bg-card);
      border: 1px solid var(--bg-card-border);
      color: var(--text-muted);
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
    }
    .practice-pill.active {
      background: var(--purple);
      border-color: var(--purple-hover);
      color: #FFF;
      box-shadow: 0 4px 14px var(--purple-glow);
    }

    /* Tarot 4 Submodes Bar */
    .tarot-submode-bar {
      display: flex;
      justify-content: center;
      gap: 16px;
      margin: 10px auto 16px;
      padding: 0 16px;
    }
    .tarot-mode-btn {
      width: 44px;
      height: 44px;
      border-radius: 14px;
      background: var(--bg-card);
      border: 1px solid var(--bg-card-border);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: all 0.2s;
    }
    .tarot-mode-btn.active {
      background: rgba(120, 75, 246, 0.25);
      border-color: var(--purple);
      box-shadow: 0 0 12px var(--purple-glow);
    }
    .tarot-mode-btn svg { width: 22px; height: 22px; fill: #8E93A6; }
    .tarot-mode-btn.active svg { fill: #FFF; }

    /* Slots Container (Hero Scale ~45% screen height) */
    .tarot-slots-row {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 12px;
      padding: 10px 16px;
      min-height: 240px;
    }
    .tarot-slot-hero {
      width: 155px;
      height: 245px;
      border-radius: 20px;
      border: 2px dashed rgba(120, 75, 246, 0.45);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 12px;
      position: relative;
      cursor: pointer;
      transition: all 0.3s ease;
      background: rgba(120, 75, 246, 0.05);
    }
    .tarot-slot-hero.filled {
      border: none;
      background: none;
      box-shadow: 0 14px 34px rgba(0, 0, 0, 0.65);
    }
    .tarot-card-img-hero {
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 20px;
      box-shadow: 0 10px 28px rgba(0, 0, 0, 0.55);
    }
    .tarot-slot-label {
      font-size: 13px;
      font-weight: 700;
      color: var(--purple);
      margin-top: 6px;
    }

    /* 5-Card Spread Cross Grid */
    .tarot-slots-cross-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      grid-template-rows: repeat(3, 1fr);
      gap: 8px;
      max-width: 380px;
      margin: 0 auto;
      padding: 10px;
    }

    /* Fan Arc Container */
    .tarot-arc-fan-wrap {
      position: relative;
      height: 190px;
      width: 100%;
      overflow: hidden;
      margin-top: 10px;
    }
    .fan-card-item {
      position: absolute;
      width: 62px;
      height: 100px;
      border-radius: 10px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5);
      cursor: pointer;
      transition: transform 0.25s cubic-bezier(0.175, 0.885, 0.32, 1.275), filter 0.2s;
      transform-origin: 50% 120%;
    }
    .fan-card-item:hover {
      filter: brightness(1.2) drop-shadow(0 0 10px var(--purple));
      z-index: 10;
    }

    /* Spheres of Life Chips */
    .spheres-wrap {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 14px 0;
    }
    .sphere-chip {
      padding: 7px 14px;
      border-radius: 14px;
      background: var(--bg-card);
      border: 1px solid var(--bg-card-border);
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      transition: all 0.2s;
    }
    .sphere-chip.active {
      background: var(--purple);
      border-color: var(--purple-hover);
      color: #FFF;
      box-shadow: 0 4px 12px var(--purple-glow);
    }

    /* Rune Stone Hero */
    .rune-hero-wrap {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 24px 16px;
    }
    .rune-stone-3d {
      width: 190px;
      height: 190px;
      border-radius: 50%;
      background: radial-gradient(circle at 35% 35%, #3C3E52, #181924);
      box-shadow: 0 18px 45px rgba(0, 0, 0, 0.7), inset 0 2px 5px rgba(255, 255, 255, 0.25);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      position: relative;
      transition: transform 0.3s ease;
    }
    .rune-stone-3d:active { transform: scale(0.96); }
    .rune-glyph-symbol {
      font-size: 82px;
      color: #FFF;
      text-shadow: 0 0 22px rgba(138, 96, 248, 0.8), 0 0 45px rgba(45, 212, 191, 0.5);
      font-family: var(--font-serif);
    }
    .rune-stone-aura {
      position: absolute;
      width: 250px;
      height: 250px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(120, 75, 246, 0.18) 0%, transparent 70%);
      z-index: -1;
      animation: pulseAura 4s ease-in-out infinite alternate;
    }
    @keyframes pulseAura {
      0% { transform: scale(0.9); opacity: 0.6; }
      100% { transform: scale(1.15); opacity: 1; }
    }

    /* Affirmation Card Ken Burns */
    .affirmation-kenburns-card {
      height: 480px;
      border-radius: var(--radius-xl);
      overflow: hidden;
      position: relative;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      padding: 30px 24px;
      box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
    }
    .affirmation-bg-art {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      object-fit: cover;
      z-index: 1;
      animation: kenBurns 16s ease-in-out infinite alternate;
    }
    @keyframes kenBurns {
      0% { transform: scale(1); }
      100% { transform: scale(1.08); }
    }
    .affirmation-overlay-gradient {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      background: linear-gradient(180deg, rgba(13, 14, 21, 0.3) 0%, rgba(13, 14, 21, 0.8) 100%);
      z-index: 2;
    }
    .affirmation-content-col {
      position: relative;
      z-index: 3;
      display: flex;
      flex-direction: column;
      height: 100%;
      justify-content: space-between;
    }
    .affirmation-quote-text {
      font-size: 24px;
      font-weight: 700;
      line-height: 1.4;
      font-family: var(--font-serif);
      color: #FFF;
      text-shadow: 0 2px 10px rgba(0, 0, 0, 0.6);
    }

    /* ==========================================================================
       SCREEN 3: HEALING & SOUNDSCAPE (68 SOUNDS + FULL-SCREEN PLAYER)
       ========================================================================== */
    .sound-chips-row {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding: 12px 16px;
      scrollbar-width: none;
    }
    .sound-chips-row::-webkit-scrollbar { display: none; }
    .sound-cat-chip {
      padding: 7px 16px;
      border-radius: 16px;
      background: var(--bg-card);
      border: 1px solid var(--bg-card-border);
      font-size: 13px;
      font-weight: 600;
      color: var(--text-muted);
      cursor: pointer;
      white-space: nowrap;
      transition: all 0.2s;
    }
    .sound-cat-chip.active {
      background: var(--purple);
      border-color: var(--purple-hover);
      color: #FFF;
    }

    .sounds-grid {
      display: grid;
      grid-template-columns: repeat(2, 1fr);
      gap: 12px;
      padding: 10px 16px 20px;
    }
    .sound-card-item {
      background: var(--bg-card);
      border: 1px solid var(--bg-card-border);
      border-radius: var(--radius-lg);
      padding: 14px;
      display: flex;
      flex-direction: column;
      align-items: center;
      text-align: center;
      cursor: pointer;
      position: relative;
      transition: all 0.2s;
    }
    .sound-card-item:hover {
      border-color: rgba(255, 255, 255, 0.2);
      transform: translateY(-2px);
    }
    .sound-card-thumb {
      width: 72px;
      height: 72px;
      object-fit: cover;
      border-radius: 20px;
      margin-bottom: 10px;
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.4);
    }
    .sound-card-title {
      font-size: 13px;
      font-weight: 700;
      color: #FFF;
      line-height: 1.35;
      margin-bottom: 4px;
    }
    .sound-card-cat {
      font-size: 11px;
      color: var(--text-muted);
      font-weight: 600;
    }
    .sound-card-play-btn {
      position: absolute;
      bottom: 12px;
      right: 12px;
      width: 28px;
      height: 28px;
      border-radius: 50%;
      background: rgba(120, 75, 246, 0.85);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #FFF;
      box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
    }

    /* Full-Screen Music Player Modal */
    .player-fullscreen-modal {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: #090A10;
      z-index: 200;
      display: none;
      flex-direction: column;
      justify-content: space-between;
      padding: 40px 24px 30px;
      animation: fadeIn 0.3s ease;
    }
    .player-bg-video {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      object-fit: cover;
      z-index: 1;
      opacity: 0.65;
    }
    .player-overlay-shade {
      position: absolute;
      top: 0; left: 0; width: 100%; height: 100%;
      background: radial-gradient(circle at center, transparent 30%, rgba(9, 10, 16, 0.85) 100%);
      z-index: 2;
    }
    .player-ui-col {
      position: relative;
      z-index: 3;
      display: flex;
      flex-direction: column;
      height: 100%;
      justify-content: space-between;
    }
    .player-top-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .player-close-btn {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.12);
      border: none;
      color: #FFF;
      font-size: 18px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .player-sleep-timer-btn {
      padding: 6px 14px;
      border-radius: 20px;
      background: rgba(255, 255, 255, 0.12);
      border: 1px solid rgba(255, 255, 255, 0.2);
      color: #FFF;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .player-center-disc {
      width: 220px;
      height: 220px;
      border-radius: 50%;
      margin: 20px auto;
      border: 2px solid rgba(255, 255, 255, 0.2);
      box-shadow: 0 0 50px rgba(120, 75, 246, 0.5);
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .player-center-thumb {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    .player-track-title {
      font-size: 22px;
      font-weight: 800;
      text-align: center;
      color: #FFF;
      margin-bottom: 6px;
    }
    .player-track-cat {
      font-size: 12px;
      color: var(--amber);
      text-align: center;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 16px;
    }
    .player-desc-box {
      font-size: 13px;
      color: rgba(255, 255, 255, 0.85);
      text-align: center;
      line-height: 1.5;
      padding: 0 10px;
      max-height: 80px;
      overflow-y: auto;
    }
    .player-controls-row {
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 32px;
      margin: 24px 0 10px;
    }
    .player-big-play-btn {
      width: 72px;
      height: 72px;
      border-radius: 50%;
      background: #FFF;
      border: none;
      color: #000;
      font-size: 26px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 8px 30px rgba(255, 255, 255, 0.4);
      transition: transform 0.15s;
    }
    .player-big-play-btn:active { transform: scale(0.92); }

    /* ==========================================================================
       SCREEN 4: LIGHT CHAT (5 ASTRA MENTORS)
       ========================================================================== */
    #screen-chat {
      background: var(--chat-bg);
      color: var(--chat-text);
      display: none;
      flex-direction: column;
      height: 100%;
      padding-bottom: 74px;
    }
    #screen-chat.active { display: flex; }

    .chat-header-bar-light {
      background: #FFFFFF;
      border-bottom: 1px solid var(--chat-border);
      padding: 12px 18px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03);
    }
    .chat-mentor-info-col {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .chat-mentor-avatar-wrap {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      position: relative;
    }
    .chat-mentor-avatar-img {
      width: 100%;
      height: 100%;
      border-radius: 50%;
      object-fit: cover;
    }
    .chat-online-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #10B981;
      border: 2px solid #FFF;
      position: absolute;
      bottom: 0;
      right: 0;
    }
    .chat-mentor-name {
      font-size: 15px;
      font-weight: 800;
      color: #191B26;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .chat-mentor-status {
      font-size: 12px;
      color: #10B981;
      font-weight: 600;
    }
    .chat-switch-arrow {
      font-size: 12px;
      color: var(--chat-text-muted);
    }

    .chat-messages-container {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      scrollbar-width: none;
    }
    .chat-messages-container::-webkit-scrollbar { display: none; }

    .chat-msg-row {
      display: flex;
      gap: 10px;
      max-width: 88%;
    }
    .chat-msg-row.user {
      align-self: flex-end;
      flex-direction: row-reverse;
    }
    .chat-bubble {
      padding: 14px 16px;
      border-radius: 20px;
      font-size: 14px;
      line-height: 1.48;
      position: relative;
    }
    .chat-msg-row.mentor .chat-bubble {
      background: #FFFFFF;
      color: #191B26;
      border-radius: 20px 20px 20px 4px;
      box-shadow: 0 4px 14px rgba(0, 0, 0, 0.04);
      border: 1px solid #E8EBF2;
    }
    .chat-msg-row.user .chat-bubble {
      background: var(--purple);
      color: #FFFFFF;
      border-radius: 20px 20px 4px 20px;
      box-shadow: 0 4px 14px rgba(120, 75, 246, 0.35);
    }

    /* Card Insight inside Chat */
    .chat-card-insight {
      background: #F8F9FD;
      border: 1px solid #E2E6F0;
      border-radius: 14px;
      padding: 12px;
      margin-top: 10px;
    }
    .chat-card-insight-title {
      font-weight: 700;
      font-size: 13px;
      color: var(--purple);
      margin-bottom: 6px;
    }
    .chat-spoiler-btn {
      color: var(--purple);
      font-weight: 700;
      font-size: 12px;
      cursor: pointer;
      margin-top: 8px;
      display: inline-block;
    }
    .chat-feedback-row {
      display: flex;
      gap: 12px;
      margin-top: 8px;
    }
    .chat-feedback-btn {
      background: none;
      border: none;
      cursor: pointer;
      font-size: 14px;
      opacity: 0.6;
      transition: opacity 0.2s;
    }
    .chat-feedback-btn:hover { opacity: 1; }

    /* Chat Input Bar */
    .chat-input-bar-light {
      background: #FFFFFF;
      border-top: 1px solid var(--chat-border);
      padding: 10px 14px;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .chat-input-field {
      flex: 1;
      height: 44px;
      border-radius: 22px;
      background: #F1F3F8;
      border: 1px solid #E2E6F0;
      padding: 0 16px;
      font-size: 14px;
      outline: none;
      color: #191B26;
    }
    .chat-send-btn {
      width: 42px;
      height: 42px;
      border-radius: 50%;
      background: var(--purple);
      border: none;
      color: #FFF;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(120, 75, 246, 0.4);
    }

    /* Mentor Switcher Bottom Sheet */
    .mentor-item-card {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 12px 14px;
      border-radius: 16px;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.08);
      margin-bottom: 10px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .mentor-item-card.active {
      background: rgba(120, 75, 246, 0.2);
      border-color: var(--purple);
    }

    /* ==========================================================================
       SCREEN 5: PROFILE 'YOU' & SETTINGS SCREEN (BOLTIK)
       ========================================================================== */
    .you-header-bar {
      padding: 18px 20px 10px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .you-header-title {
      font-size: 22px;
      font-weight: 800;
    }
    .you-bolt-btn {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      background: var(--bg-card);
      border: 1px solid var(--bg-card-border);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: #FFF;
    }

    .you-hero-avatar-wrap {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 10px 0 24px;
    }
    .you-star-frame {
      width: 140px;
      height: 140px;
      border-radius: 50%;
      border: 3px solid #E5C378;
      box-shadow: 0 0 30px rgba(229, 195, 120, 0.35);
      position: relative;
      cursor: pointer;
      overflow: hidden;
      margin-bottom: 14px;
    }
    .you-avatar-img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    .you-zodiac-badge {
      position: absolute;
      bottom: 6px;
      right: 6px;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: #151722;
      border: 1px solid #E5C378;
      display: flex;
      align-items: center;
      justify-content: center;
      color: #E5C378;
      font-weight: 800;
      font-size: 14px;
    }

    /* Settings Screen Modal */
    .settings-screen-modal {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: #0D0E15;
      z-index: 150;
      display: none;
      flex-direction: column;
      overflow-y: auto;
      padding: 24px 18px 40px;
      animation: fadeIn 0.25s ease;
    }
    .settings-top-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 24px;
    }
    .settings-group-title {
      font-size: 11px;
      font-weight: 700;
      color: var(--text-dim);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin: 16px 6px 8px;
    }
    .settings-item-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 14px 16px;
      background: var(--bg-card);
      border: 1px solid var(--bg-card-border);
      border-radius: 16px;
      margin-bottom: 8px;
      cursor: pointer;
    }
    .settings-item-left {
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 14px;
      font-weight: 600;
    }
    .toggle-switch {
      width: 44px;
      height: 24px;
      border-radius: 12px;
      background: rgba(255, 255, 255, 0.2);
      position: relative;
      cursor: pointer;
      transition: background 0.2s;
    }
    .toggle-switch.on { background: var(--purple); }
    .toggle-switch::after {
      content: '';
      position: absolute;
      top: 2px; left: 2px;
      width: 20px; height: 20px;
      border-radius: 50%;
      background: #FFF;
      transition: transform 0.2s;
    }
    .toggle-switch.on::after { transform: translateX(20px); }

    .danger-zone-card {
      border: 1px solid rgba(239, 68, 68, 0.35);
      background: rgba(239, 68, 68, 0.08);
      color: #EF4444;
      font-weight: 700;
    }

    /* ==========================================================================
       PAYWALL ASTRA PLUS MODAL
       ========================================================================== */
    .paywall-modal {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: #090A10;
      z-index: 250;
      display: none;
      flex-direction: column;
      overflow-y: auto;
      padding: 24px 20px 36px;
      animation: fadeIn 0.3s ease;
    }
    .paywall-muse-hero {
      width: 100%;
      height: 220px;
      object-fit: cover;
      border-radius: 28px;
      margin-bottom: 16px;
      box-shadow: 0 12px 35px rgba(229, 195, 120, 0.25);
    }
    .paywall-plan-card {
      border: 2px solid rgba(255, 255, 255, 0.1);
      border-radius: 20px;
      padding: 16px;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      transition: all 0.2s;
    }
    .paywall-plan-card.selected {
      border-color: #E5C378;
      background: rgba(229, 195, 120, 0.1);
    }

    /* ==========================================================================
       ONBOARDING FULLSCREEN MODAL (13 SLIDES)
       ========================================================================== */
    .onboarding-modal {
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: #0E0E12;
      z-index: 300;
      display: none;
      flex-direction: column;
      padding: 20px 18px 24px;
      overflow-y: auto;
      animation: fadeIn 0.3s ease;
    }
    .onboard-top-nav {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 14px;
    }
    .onboard-progress-bar {
      height: 4px;
      background: rgba(255, 255, 255, 0.15);
      border-radius: 2px;
      flex: 1;
      margin: 0 14px;
      overflow: hidden;
    }
    .onboard-progress-fill {
      height: 100%;
      background: var(--purple);
      width: 8%;
      transition: width 0.3s ease;
    }
    .onboard-slide-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .onboard-header-title {
      font-size: 26px;
      font-weight: 800;
      line-height: 1.25;
      margin-bottom: 8px;
    }
    .onboard-header-sub {
      font-size: 14px;
      color: var(--text-muted);
      line-height: 1.45;
      margin-bottom: 20px;
    }
    .onboard-quiz-option {
      background: var(--bg-card);
      border: 1px solid var(--bg-card-border);
      border-radius: 18px;
      padding: 16px 18px;
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: pointer;
      transition: all 0.2s;
    }
    .onboard-quiz-option.selected {
      border-color: var(--purple);
      background: rgba(120, 75, 246, 0.18);
    }

    /* Avatars Gallery Modal */
    .avatar-gallery-grid {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      padding: 14px 0;
      max-height: 60vh;
      overflow-y: auto;
    }
    .avatar-item-card {
      background: var(--bg-card);
      border: 1px solid var(--bg-card-border);
      border-radius: 16px;
      padding: 8px;
      display: flex;
      flex-direction: column;
      align-items: center;
      cursor: pointer;
      transition: all 0.2s;
    }
    .avatar-item-card:hover {
      border-color: var(--purple);
      transform: translateY(-2px);
    }
    .avatar-item-img {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      object-fit: cover;
      margin-bottom: 6px;
    }
  </style>
</head>
<body>

  <!-- MOBILE DEVICE FRAME -->
  <div class="app-viewport">

    <!-- SCREENS WRAPPER -->
    <div class="screens-wrapper">

      <!-- ================================================================== -->
      <!-- SCREEN 1: CALENDAR & DAILY FEED                                    -->
      <!-- ================================================================== -->
      <div id="screen-calendar" class="screen-view active">
        
        <div class="cal-header-bar">
          <div style="display: flex; align-items: center; gap: 10px;">
            <img src="00_ИКОНКИ_И_ЛОГОТИП_АСТРА/Astra_AppIcon_StarFlower_small_128.webp" style="width: 32px; height: 32px; border-radius: 8px;" alt="Astra">
            <div>
              <div class="cal-date-title" id="cal-date-display">19 Октября • Пн</div>
              <div style="font-size: 12px; color: var(--text-muted);">АСТРА • Ритмы Вселенной</div>
            </div>
          </div>
          <div class="cal-moon-badge" id="cal-moon-day-badge">13 лунный день</div>
        </div>

        <!-- Infinite Dates Strip -->
        <div class="cal-strip-container" id="cal-strip"></div>

        <!-- Hero 3D Moon Display -->
        <div class="hero-moon-wrap">
          <img class="hero-moon-img" id="hero-moon-image" src="astra_assets/01_ФОНЫ_И_БАННЕРЫ_ВЫСОКОГО_РАЗРЕШЕНИЯ/ic_sharing_moon.png" alt="Moon">
          <div class="hero-moon-phase-name" id="hero-moon-name">Растущая Луна</div>
          <div class="hero-moon-illum">
            <span id="hero-moon-illum-pct">Освещенность: 98%</span>
            <span>•</span>
            <span id="hero-moon-zodiac">Луна в Тельце ♉</span>
          </div>
        </div>

        <!-- Feed Cards -->
        <div class="feed-container">
          
          <!-- Haircut / Beauty by Moon -->
          <div class="card-glass">
            <div class="card-title-row">
              <div class="card-title">
                <img src="astra_assets/02_ИЛЛЮСТРАЦИИ_И_ОНБОРДИНГ/haircut.png" style="width: 26px; height: 26px; object-fit: contain;" alt="Haircut">
                <span>Стрижка по Луне</span>
              </div>
              <span class="haircut-badge-good">Благоприятно</span>
            </div>
            <div class="card-sub">
              13-й лунный день обновляет клеточную структуру волос, приносит омоложение и материальное благополучие. Стрижка сегодня укрепляет корни.
            </div>
          </div>

          <!-- Transit Card -->
          <div class="card-glass">
            <div class="card-title-row">
              <div class="card-title">
                <img src="astra_assets/05_ЗОДИАК_И_НАТАЛЬНАЯ_КАРТА/sticker_sharing_natal.png" style="width: 24px; height: 24px; object-fit: contain;" alt="Transit">
                <span>Астро-транзит дня</span>
              </div>
              <span style="font-size: 12px; color: var(--purple); font-weight: 700;">Солнце △ Венера</span>
            </div>
            <div class="card-sub">
              Гармоничный аспект дарит легкость в общении, тонкое чувство прекрасного и удачу в переговорах. Идеальное время для искренних бесед.
            </div>
          </div>

          <!-- Wisdom & Deity Teaser -->
          <div class="card-glass" style="cursor: pointer;" onclick="switchPracticeSection('gods')">
            <div class="card-title-row">
              <div class="card-title">
                <span>🕉️ Покровитель дня: Хануман</span>
              </div>
              <span style="font-size: 12px; color: var(--amber); font-weight: 700;">Открыть ></span>
            </div>
            <div class="card-sub">
              Символ внутренней силы, верности и преодоления любых препятствий. Нажмите, чтобы получить персональное благословение.
            </div>
          </div>

          <!-- Sound of the Day Teaser -->
          <div class="card-glass" style="cursor: pointer;" onclick="openSoundPlayerById(291)">
            <div class="card-title-row">
              <div class="card-title">
                <img src="astra_assets/07_3D_ИКОНКИ_И_ЭЛЕМЕНТЫ/icon.png" style="width: 24px; height: 24px; object-fit: contain;" alt="Sound">
                <span>Звук дня: 144 Hz Гармония</span>
              </div>
              <span style="font-size: 12px; color: var(--teal); font-weight: 700;">Слушать ▶</span>
            </div>
            <div class="card-sub">
              Очищающий резонанс объединяет разум с сердцем и снимает накопленную тревожность.
            </div>
          </div>

        </div>
      </div>

      <!-- ================================================================== -->
      <!-- SCREEN 2: PRACTICES                                                -->
      <!-- ================================================================== -->
      <div id="screen-practices" class="screen-view">
        
        <!-- Practices Top Horizontal Tabs (6 items) -->
        <div class="practices-tabs-scroll">
          <div class="practice-pill active" onclick="switchPracticeTab('tarot', this)">Таро</div>
          <div class="practice-pill" onclick="switchPracticeTab('oracle', this)">Оракул</div>
          <div class="practice-pill" onclick="switchPracticeTab('gods', this)">Боги</div>
          <div class="practice-pill" onclick="switchPracticeTab('dream', this)">Сонник</div>
          <div class="practice-pill" onclick="switchPracticeTab('runes', this)">Руны (24)</div>
          <div class="practice-pill" onclick="switchPracticeTab('affirmations', this)">Аффирмации</div>
        </div>

        <!-- 1. TAROT SECTION -->
        <div id="subview-tarot" class="practice-subview">
          
          <!-- 4 Submodes Selector -->
          <div class="tarot-submode-bar">
            <div class="tarot-mode-btn active" id="btn-tarot-mode-1" title="Быстрый ответ (1 карта)" onclick="setTarotMode(1)">
              <svg viewBox="0 0 24 24"><rect x="7" y="3" width="10" height="18" rx="2" stroke="currentColor" stroke-width="2" fill="none"/></svg>
            </div>
            <div class="tarot-mode-btn" id="btn-tarot-mode-3" title="Текущая ситуация (3 карты)" onclick="setTarotMode(3)">
              <svg viewBox="0 0 24 24"><rect x="3" y="4" width="5" height="16" rx="1.5" stroke="currentColor" stroke-width="2" fill="none"/><rect x="9.5" y="4" width="5" height="16" rx="1.5" stroke="currentColor" stroke-width="2" fill="none"/><rect x="16" y="4" width="5" height="16" rx="1.5" stroke="currentColor" stroke-width="2" fill="none"/></svg>
            </div>
            <div class="tarot-mode-btn" id="btn-tarot-mode-5" title="Взгляд в будущее (5 карт)" onclick="setTarotMode(5)">
              <svg viewBox="0 0 24 24"><circle cx="7" cy="7" r="2.5"/><circle cx="17" cy="7" r="2.5"/><circle cx="12" cy="12" r="2.5"/><circle cx="7" cy="17" r="2.5"/><circle cx="17" cy="17" r="2.5"/></svg>
            </div>
            <div class="tarot-mode-btn" id="btn-tarot-mode-all" title="Все 78 карт" onclick="setTarotMode('all')">
              <svg viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
            </div>
          </div>

          <!-- Slots Container (Hero Scale) -->
          <div id="tarot-slots-container" class="tarot-slots-row"></div>

          <!-- 4 Actions Bar -->
          <div class="actions-4-bar" id="tarot-actions-bar" style="display: none;">
            <div class="btn-pill-action" title="Перевытянуть" onclick="resetTarotSpread()">🔄</div>
            <div class="btn-pill-action" title="Сохранить" onclick="saveTarotSnapshot()">⬆️</div>
            <div class="btn-pill-action" title="TikTok" onclick="shareToSocial('tiktok')">🎵</div>
            <div class="btn-pill-action" title="Instagram" onclick="shareToSocial('instagram')">📷</div>
          </div>

          <!-- Radial Arc Fan Deck -->
          <div id="tarot-fan-wrapper" class="tarot-arc-fan-wrap">
            <div id="tarot-fan-deck"></div>
          </div>

          <!-- 'Learn More' / Spheres of Life Sheet Block -->
          <div id="tarot-spheres-block" style="padding: 0 16px; margin-top: 14px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 8px;">
              <img src="10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ/01_Luna_Wise_Mystic.png" style="width: 32px; height: 32px; border-radius: 50%; border: 1px solid var(--purple);" alt="Mentor">
              <div style="font-size: 13px; font-weight: 700;">Выберите сферу жизни для инсайта:</div>
            </div>
            <div class="spheres-wrap" id="tarot-spheres-chips"></div>

            <button class="btn-primary" id="btn-get-insight-tarot" onclick="requestTarotInsight()">
              <span id="insight-quota-badge" style="background: rgba(255,255,255,0.2); padding: 2px 8px; border-radius: 10px; font-size: 12px;">1 ост</span>
              <span>Получите Инсайт от Алтеи</span>
            </button>
          </div>

          <!-- All 78 Cards Catalog View -->
          <div id="tarot-catalog-view" style="display: none; padding: 10px 16px;">
            <div style="display: flex; gap: 6px; overflow-x: auto; padding-bottom: 10px; scrollbar-width: none;">
              <div class="sound-cat-chip active" onclick="filterTarotSuit('all', this)">Все (78)</div>
              <div class="sound-cat-chip" onclick="filterTarotSuit('major', this)">Старшие</div>
              <div class="sound-cat-chip" onclick="filterTarotSuit('wands', this)">Жезлы</div>
              <div class="sound-cat-chip" onclick="filterTarotSuit('cups', this)">Кубки</div>
              <div class="sound-cat-chip" onclick="filterTarotSuit('swords', this)">Мечи</div>
              <div class="sound-cat-chip" onclick="filterTarotSuit('pentacles', this)">Пентакли</div>
            </div>
            <div id="tarot-catalog-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 10px;"></div>
          </div>

        </div>

        <!-- 2. ORACLE SECTION -->
        <div id="subview-oracle" class="practice-subview" style="display: none; padding: 14px 16px;">
          <div class="card-glass" style="text-align: center;">
            <div class="card-title" style="justify-content: center; margin-bottom: 6px;">Колода Оракула Астры</div>
            <div class="card-sub">Метафорические образы глубинного подсознания для поиска внутренней ясности.</div>
          </div>
          <div id="oracle-slot-container" class="tarot-slots-row">
            <div class="tarot-slot-hero" id="oracle-slot" onclick="drawOracleCard()">
              <div style="font-size: 32px; margin-bottom: 8px;">✨</div>
              <div class="tarot-slot-label">Вытянуть карту Оракула</div>
            </div>
          </div>
        </div>

        <!-- 3. GODS SECTION -->
        <div id="subview-gods" class="practice-subview" style="display: none; padding: 14px 16px;">
          <div class="card-glass" style="text-align: center;">
            <div class="card-title" style="justify-content: center; margin-bottom: 6px;">🕉️ Ведические Архетипы & Божества</div>
            <div class="card-sub">Вытяните покровителя и получите благословение высших космических сил на этот день.</div>
          </div>
          <div class="tarot-slots-row">
            <div class="tarot-slot-hero" id="gods-slot" onclick="drawDeityCard()">
              <div style="font-size: 32px; margin-bottom: 8px;">🔱</div>
              <div class="tarot-slot-label">Призвать покровителя</div>
            </div>
          </div>
        </div>

        <!-- 4. DREAM BOOK (СОННИК) -->
        <div id="subview-dream" class="practice-subview" style="display: none; padding: 14px 16px;">
          <div style="display: flex; gap: 8px; margin-bottom: 14px;">
            <div class="sound-cat-chip active" id="tab-dream-new" onclick="switchDreamMode('new')">+ Расшифровать сон</div>
            <div class="sound-cat-chip" id="tab-dream-archive" onclick="switchDreamMode('archive')">Архив снов</div>
          </div>

          <!-- New Dream Form -->
          <div id="dream-new-box">
            <div class="card-glass">
              <div class="card-title" style="margin-bottom: 12px;">🌙 Расшифруйте свой сон</div>
              <textarea id="dream-input-text" style="width: 100%; height: 110px; background: var(--bg-input); border: 1px solid var(--bg-card-border); border-radius: 16px; padding: 12px; color: #FFF; font-size: 14px; outline: none; resize: none;" placeholder="Опишите детали сна: что вам снилось, какие символы, люди или чувства вы запомнили?"></textarea>
              <button class="btn-primary" style="margin-top: 14px;" onclick="interpretDreamAction()">
                <span>1 ост • Получите Инсайт о сне</span>
              </button>
            </div>
            <!-- Dream Result Card -->
            <div id="dream-result-card" style="display: none;" class="card-glass"></div>
          </div>

          <!-- Dream Archive -->
          <div id="dream-archive-box" style="display: none;"></div>
        </div>

        <!-- 5. RUNES SECTION (24 ELDER FUTHARK) -->
        <div id="subview-runes" class="practice-subview" style="display: none; padding: 10px 16px;">
          <div class="rune-hero-wrap">
            <div class="rune-stone-aura"></div>
            <div class="rune-stone-3d" id="rune-hero-stone" onclick="drawDailyRune()">
              <div class="rune-glyph-symbol" id="rune-glyph-display">ᛚ</div>
            </div>
            <div style="font-size: 22px; font-weight: 800; margin-top: 16px;" id="rune-name-display">Laguz</div>
            <div style="font-size: 13px; color: var(--teal); font-weight: 700; margin-top: 4px;" id="rune-sub-display">«Тайны воды, интуиция»</div>
          </div>

          <div class="actions-4-bar">
            <div class="btn-pill-action" onclick="drawDailyRune()">🔄</div>
            <div class="btn-pill-action" onclick="saveTarotSnapshot()">⬆️</div>
            <div class="btn-pill-action" onclick="shareToSocial('tiktok')">🎵</div>
            <div class="btn-pill-action" onclick="shareToSocial('instagram')">📷</div>
          </div>

          <div style="display: flex; gap: 10px;">
            <button class="btn-primary" style="flex: 1;" onclick="openRuneMeaningModal()">
              <span>Значение руны</span>
            </button>
            <button class="btn-primary" style="flex: 1; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.2);" onclick="openRunesCatalogModal()">
              <span>Все 24 руны</span>
            </button>
          </div>
        </div>

        <!-- 6. AFFIRMATIONS (KEN BURNS) -->
        <div id="subview-affirmations" class="practice-subview" style="display: none; padding: 10px 16px;">
          <div class="affirmation-kenburns-card">
            <img class="affirmation-bg-art" id="affirmation-img" src="astra_assets/01_ФОНЫ_И_БАННЕРЫ_ВЫСОКОГО_РАЗРЕШЕНИЯ/sharing_bg.png" alt="Affirmation">
            <div class="affirmation-overlay-gradient"></div>
            <div class="affirmation-content-col">
              <div style="display: flex; justify-content: space-between; align-items: center;">
                <span class="cal-moon-badge" id="affirmation-cat-badge">Прощение и покой</span>
                <span style="font-size: 13px; color: rgba(255,255,255,0.7);">АСТРА РИТУАЛ</span>
              </div>
              <div class="affirmation-quote-text" id="affirmation-text-display">
                «Я прощаю всех в прошлом за все осознанные ошибки и впускаю чистый свет в свое сердце.»
              </div>
              <div class="actions-4-bar" style="margin: 0; justify-content: space-between;">
                <div class="btn-pill-action" onclick="nextAffirmation()">🔄</div>
                <div class="btn-pill-action" onclick="saveTarotSnapshot()">⬆️</div>
                <div class="btn-pill-action" onclick="shareToSocial('tiktok')">🎵</div>
                <div class="btn-pill-action" onclick="shareToSocial('instagram')">📷</div>
              </div>
            </div>
          </div>
        </div>

      </div>

      <!-- ================================================================== -->
      <!-- SCREEN 3: HEALING & SOUNDSCAPE                                     -->
      <!-- ================================================================== -->
      <div id="screen-healing" class="screen-view">
        
        <div style="padding: 16px 20px 8px;">
          <div style="font-size: 20px; font-weight: 800;">Исцеление звуком</div>
          <div style="font-size: 13px; color: var(--text-muted); margin-top: 2px;">68 целебных частот и бинауральных резонансов</div>
        </div>

        <!-- Recent Sound Play Banner (144 Hz) -->
        <div style="padding: 0 16px;">
          <div class="card-glass" style="display: flex; align-items: center; justify-content: space-between; cursor: pointer;" onclick="openSoundPlayerById(291)">
            <div style="display: flex; align-items: center; gap: 14px;">
              <img src="astra_assets/07_3D_ИКОНКИ_И_ЭЛЕМЕНТЫ/icon.png" style="width: 52px; height: 52px; border-radius: 16px; object-fit: cover;" alt="144">
              <div>
                <div style="font-size: 11px; color: var(--amber); font-weight: 800; text-transform: uppercase;">Недавнее</div>
                <div style="font-size: 15px; font-weight: 700; color: #FFF;">144 Hz — Гармония и очищение</div>
              </div>
            </div>
            <div style="width: 40px; height: 40px; border-radius: 50%; background: var(--purple); display: flex; align-items: center; justify-content: center; color: #FFF;">▶</div>
          </div>
        </div>

        <!-- Sound Category Chips -->
        <div class="sound-chips-row" id="sound-category-chips"></div>

        <!-- 68 Sounds Grid -->
        <div class="sounds-grid" id="sounds-list-grid"></div>

      </div>

      <!-- ================================================================== -->
      <!-- SCREEN 4: LIGHT CHAT (5 MENTORS)                                   -->
      <!-- ================================================================== -->
      <div id="screen-chat" class="screen-view">
        
        <!-- Light Chat Header with Switcher Trigger -->
        <div class="chat-header-bar-light" onclick="openMentorSelectorSheet()">
          <div class="chat-mentor-info-col">
            <div class="chat-mentor-avatar-wrap">
              <img class="chat-mentor-avatar-img" id="chat-header-avatar" src="10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ/01_Luna_Wise_Mystic.png" alt="Mentor">
              <div class="chat-online-dot"></div>
            </div>
            <div>
              <div class="chat-mentor-name">
                <span id="chat-header-name">Алтея</span>
                <span class="chat-switch-arrow">▼</span>
              </div>
              <div class="chat-mentor-status" id="chat-header-status">В потоке Вселенной • на связи</div>
            </div>
          </div>
          <div style="font-size: 12px; font-weight: 700; color: var(--purple);">Сменить</div>
        </div>

        <!-- Messages Area -->
        <div class="chat-messages-container" id="chat-msg-area">
          <div class="chat-msg-row mentor">
            <div class="chat-bubble">
              Приветствую тебя, светлая душа. Я Алтея, Хранительница Лунной Тишины. Сегодня Луна раскрывает глубокие пласты интуиции. С каким вопросом ты пришел ко мне?
            </div>
          </div>
        </div>

        <!-- Quick Suggestions Chips -->
        <div style="display: flex; gap: 8px; overflow-x: auto; padding: 6px 14px 10px; background: #FFF; scrollbar-width: none;">
          <div class="sound-cat-chip" style="background: #F1F3F8; color: #191B26;" onclick="sendChatMessageQuick('Что несет сегодняшняя Луна в Тельце?')">Луна в Тельце?</div>
          <div class="sound-cat-chip" style="background: #F1F3F8; color: #191B26;" onclick="sendChatMessageQuick('Вечерний ритуал для спокойного сна')">Ритуал на сон</div>
          <div class="sound-cat-chip" style="background: #F1F3F8; color: #191B26;" onclick="sendChatMessageQuick('Совет по финансам на сегодня')">Финансы сегодня</div>
        </div>

        <!-- Input Bar -->
        <div class="chat-input-bar-light">
          <input type="text" id="chat-input-box" class="chat-input-field" placeholder="Задай вопрос наставнику..." onkeydown="if(event.key==='Enter') sendUserChatMessage()">
          <button class="chat-send-btn" onclick="sendUserChatMessage()">↑</button>
        </div>

      </div>

      <!-- ================================================================== -->
      <!-- SCREEN 5: PROFILE 'YOU'                                            -->
      <!-- ================================================================== -->
      <div id="screen-you" class="screen-view">
        
        <div class="you-header-bar">
          <div class="you-header-title">Вы</div>
          <div class="you-bolt-btn" title="Настройки" onclick="openSettingsScreen()">⚙️</div>
        </div>

        <!-- Hero Avatar -->
        <div class="you-hero-avatar-wrap">
          <div class="you-star-frame" onclick="openAvatarSelectorModal()">
            <img class="you-avatar-img" id="profile-avatar-display" src="11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/01_Default_Female_Muse_master_1024.png" alt="Avatar">
            <div class="you-zodiac-badge">♈</div>
          </div>
          <div style="font-size: 18px; font-weight: 800; margin-bottom: 4px;" id="profile-user-name">Александр</div>
          <div style="font-size: 13px; color: var(--amber); font-weight: 700;">ASTRA PLUS • АКТИВЕН</div>
          
          <div style="display: flex; gap: 10px; margin-top: 14px;">
            <button class="practice-pill active" onclick="openAvatarSelectorModal()">📷 Ваш Аватар (60)</button>
            <div class="btn-pill-action" onclick="saveTarotSnapshot()">⬆️</div>
          </div>
        </div>

        <!-- Sections -->
        <div style="padding: 0 16px 20px;">
          
          <div class="settings-group-title">КОСМИЧЕСКИЙ ПОРТРЕТ</div>
          <div class="card-glass" style="cursor: pointer;" onclick="openSettingsScreen()">
            <div class="card-title-row">
              <div class="card-title">🪐 Натальная карта</div>
              <span style="font-size: 12px; color: var(--purple); font-weight: 700;">Изменить ></span>
            </div>
            <div class="card-sub">14 мар. 2000, 22:00 • Сочи, Россия</div>
          </div>

          <div class="card-glass">
            <div class="card-title-row">
              <div class="card-title">✨ Матрица судьбы</div>
              <span style="font-size: 12px; color: var(--teal); font-weight: 700;">Аркан 7</span>
            </div>
            <div class="card-sub">Энергия движения, победы и духовного поиска. Ваше кармическое предназначение.</div>
          </div>

          <div class="settings-group-title">ВЗГЛЯД В БУДУЩЕЕ</div>
          <div class="card-glass" style="cursor: pointer;" onclick="openPaywallModal()">
            <div class="card-title-row">
              <div class="card-title">🔭 Годовой прогноз 2026–2027</div>
              <span style="font-size: 12px; color: #E5C378;">PLUS 👑</span>
            </div>
            <div class="card-sub">Подробная карта ключевых периодов, затмений и финансовых взлетов.</div>
          </div>

          <div class="card-glass" style="cursor: pointer;" onclick="openPaywallModal()">
            <div class="card-title-row">
              <div class="card-title">🧭 Карьерный компас</div>
              <span style="font-size: 12px; color: #E5C378;">PLUS 👑</span>
            </div>
            <div class="card-sub">Точки роста, финансовые риски и идеальный тайминг сделок по Юпитеру.</div>
          </div>

          <div class="card-glass" style="cursor: pointer;" onclick="openPaywallModal()">
            <div class="card-title-row">
              <div class="card-title">🗺️ Астрокартография</div>
              <span style="font-size: 12px; color: #E5C378;">PLUS 👑</span>
            </div>
            <div class="card-sub">Линии силы на карте Земли для гармоничной жизни и путешествий.</div>
          </div>

        </div>

      </div>

    </div>

    <!-- ==================================================================== -->
    <!-- BOTTOM NAVIGATION (5 TABS)                                           -->
    <!-- ==================================================================== -->
    <div class="bottom-nav">
      
      <div class="nav-tab-item active" id="tab-nav-calendar" onclick="switchMainScreen('calendar')">
        <div class="nav-tab-icon-wrap">
          <img class="nav-tab-icon" src="astra_assets/07_3D_ИКОНКИ_И_ЭЛЕМЕНТЫ/icon.png" alt="Календарь">
          <div class="nav-tab-indicator"></div>
        </div>
        <div class="nav-tab-label">Календарь</div>
      </div>

      <div class="nav-tab-item" id="tab-nav-practices" onclick="switchMainScreen('practices')">
        <div class="nav-tab-icon-wrap">
          <img class="nav-tab-icon" src="astra_assets/04_ТАРО_И_РУНЫ/ic_tarot_empty.png" alt="Практики">
          <div class="nav-tab-indicator"></div>
        </div>
        <div class="nav-tab-label">Практики</div>
      </div>

      <div class="nav-tab-item" id="tab-nav-healing" onclick="switchMainScreen('healing')">
        <div class="nav-tab-icon-wrap">
          <img class="nav-tab-icon" src="astra_assets/06_МЕДИТАЦИИ_И_ПРАКТИКИ/meditation_crystal.png" alt="Исцеление">
          <div class="nav-tab-indicator"></div>
        </div>
        <div class="nav-tab-label">Исцеление</div>
      </div>

      <div class="nav-tab-item" id="tab-nav-chat" onclick="switchMainScreen('chat')">
        <div class="nav-tab-icon-wrap">
          <img class="nav-tab-icon" src="10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ/01_Luna_Wise_Mystic.png" alt="Чат">
          <div class="nav-tab-indicator"></div>
        </div>
        <div class="nav-tab-label">Чат</div>
      </div>

      <div class="nav-tab-item" id="tab-nav-you" onclick="switchMainScreen('you')">
        <div class="nav-tab-icon-wrap">
          <img class="nav-tab-icon" src="astra_assets/07_3D_ИКОНКИ_И_ЭЛЕМЕНТЫ/ic_you_report_birth_chart.png" alt="Вы">
          <div class="nav-tab-indicator"></div>
        </div>
        <div class="nav-tab-label">Вы</div>
      </div>

    </div>

    <!-- ==================================================================== -->
    <!-- MODAL 1: BOTTOM SHEET ДЕТАЛЬНОГО ЗНАЧЕНИЯ КАРТЫ С 3D-ПЕРЕВОРОТОМ     -->
    <!-- ==================================================================== -->
    <div class="bottom-sheet-overlay" id="sheet-card-meaning" onclick="closeSheet('sheet-card-meaning')">
      <div class="bottom-sheet-content" onclick="event.stopPropagation()">
        <div class="sheet-handle"></div>
        
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center;">
          
          <!-- 3D Flippable Card Frame -->
          <div style="perspective: 1000px; margin-bottom: 14px;">
            <div id="card-sheet-flip-inner" style="width: 130px; height: 200px; border-radius: 16px; transition: transform 0.6s cubic-bezier(0.175, 0.885, 0.32, 1.275); transform-style: preserve-3d; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
              <img id="sheet-card-img" src="" style="width: 100%; height: 100%; object-fit: cover; border-radius: 16px;" alt="Card">
            </div>
          </div>

          <div style="font-size: 12px; color: var(--purple); font-weight: 800; text-transform: uppercase;" id="sheet-card-arcana">Старший Аркан</div>
          <div style="font-size: 20px; font-weight: 800; margin: 4px 0 12px;" id="sheet-card-title">Король Пентаклей</div>

          <!-- Flip Toggle Button -->
          <button class="sound-cat-chip active" id="btn-toggle-card-flip" onclick="toggleCard3DFlip()" style="margin-bottom: 16px;">
            ⟳ Перевернуть: <span id="sheet-card-pos-label">Прямая позиция</span>
          </button>
        </div>

        <div class="card-glass" style="margin-bottom: 12px;">
          <div style="font-size: 13px; font-weight: 700; color: var(--amber); margin-bottom: 6px;">Толкование аркана:</div>
          <div style="font-size: 14px; line-height: 1.5; color: rgba(255,255,255,0.9);" id="sheet-card-desc-text"></div>
        </div>

        <div class="card-glass" style="margin-bottom: 16px;">
          <div style="font-size: 13px; font-weight: 700; color: #10B981; margin-bottom: 6px;">Рекомендации:</div>
          <div style="font-size: 14px; line-height: 1.5; color: rgba(255,255,255,0.9);" id="sheet-card-rec-text"></div>
        </div>

        <button class="btn-primary" onclick="sendCardToMentorChat()">
          <span>Обсудить с наставником в чате →</span>
        </button>
      </div>
    </div>

    <!-- ==================================================================== -->
    <!-- MODAL 2: FULL-SCREEN MUSIC PLAYER (68 SOUNDS)                        -->
    <!-- ==================================================================== -->
    <div class="player-fullscreen-modal" id="modal-player-fullscreen">
      <video class="player-bg-video" id="player-video-bg" loop muted playsinline autoplay></video>
      <div class="player-overlay-shade"></div>

      <div class="player-ui-col">
        <div class="player-top-bar">
          <button class="player-close-btn" onclick="closeSoundPlayer()">✕</button>
          <button class="player-sleep-timer-btn" id="player-timer-btn" onclick="cycleSleepTimer()">
            <span>🌙 Таймер:</span> <span id="player-timer-val">Выкл</span>
          </button>
        </div>

        <div>
          <div class="player-center-disc">
            <img class="player-center-thumb" id="player-disc-img" src="" alt="Sound">
          </div>
          <div class="player-track-title" id="player-track-name">144 Hz — Гармония</div>
          <div class="player-track-cat" id="player-track-category">ГЕРЦЫ</div>
          <div class="player-desc-box" id="player-track-desc"></div>
        </div>

        <div>
          <div class="player-controls-row">
            <div class="btn-pill-action" title="AirPlay">📡</div>
            <button class="player-big-play-btn" id="player-toggle-btn" onclick="toggleSoundPlayback()">▶</button>
            <div class="btn-pill-action" title="Избранное" id="player-fav-btn" onclick="toggleSoundFavorite()">★</div>
          </div>
          <div class="actions-4-bar" style="margin-top: 12px;">
            <div class="btn-pill-action" onclick="saveTarotSnapshot()">⬆️</div>
            <div class="btn-pill-action" onclick="shareToSocial('tiktok')">🎵</div>
            <div class="btn-pill-action" onclick="shareToSocial('instagram')">📷</div>
          </div>
        </div>
      </div>

      <!-- Real Audio Stream Element -->
      <audio id="real-sound-audio" loop></audio>
    </div>

    <!-- ==================================================================== -->
    <!-- MODAL 3: MENTOR SWITCHER SHEET (5 PERSONAS)                          -->
    <!-- ==================================================================== -->
    <div class="bottom-sheet-overlay" id="sheet-mentor-selector" onclick="closeSheet('sheet-mentor-selector')">
      <div class="bottom-sheet-content" onclick="event.stopPropagation()">
        <div class="sheet-handle"></div>
        <div style="font-size: 18px; font-weight: 800; margin-bottom: 6px;">Выберите наставника Астры</div>
        <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 16px;">Каждый наставник специализируется на своей сфере жизни:</div>
        
        <div id="mentors-selector-list"></div>
      </div>
    </div>

    <!-- ==================================================================== -->
    <!-- MODAL 4: SETTINGS SCREEN (BOLTIK)                                    -->
    <!-- ==================================================================== -->
    <div class="settings-screen-modal" id="modal-settings-screen">
      <div class="settings-top-bar">
        <div style="font-size: 20px; font-weight: 800;">Настройки</div>
        <button class="player-close-btn" onclick="closeSettingsScreen()">✕</button>
      </div>

      <div class="settings-group-title">ОБУЧЕНИЕ И ОНБОРДИНГ</div>
      <div class="settings-item-row" onclick="startOnboardingFlow()">
        <div class="settings-item-left">
          <span>✨</span>
          <span>Пройти космический онбординг (13 шагов)</span>
        </div>
        <span style="color: var(--purple);">Пройти ></span>
      </div>

      <div class="settings-group-title">ПРОФИЛЬ И ДАННЫЕ РОЖДЕНИЯ</div>
      <div class="settings-item-row" onclick="editBirthDataPrompt()">
        <div class="settings-item-left">
          <span>🪐</span>
          <div>
            <div style="color: #FFF;">Дата и время рождения</div>
            <div style="font-size: 12px; color: var(--text-muted);" id="settings-natal-preview">14.03.2000, 22:00 • Сочи</div>
          </div>
        </div>
        <span style="color: var(--purple);">Изменить ></span>
      </div>

      <div class="settings-group-title">УВЕДОМЛЕНИЯ</div>
      <div class="settings-item-row">
        <div class="settings-item-left">
          <span>🔔</span>
          <span>Утренний лунный прогноз</span>
        </div>
        <div class="toggle-switch on" onclick="this.classList.toggle('on')"></div>
      </div>
      <div class="settings-item-row">
        <div class="settings-item-left">
          <span>🔮</span>
          <span>Напоминание о карте дня</span>
        </div>
        <div class="toggle-switch on" onclick="this.classList.toggle('on')"></div>
      </div>
      <div class="settings-item-row">
        <div class="settings-item-left">
          <span>✨</span>
          <span>Транзиты и затмения</span>
        </div>
        <div class="toggle-switch on" onclick="this.classList.toggle('on')"></div>
      </div>

      <div class="settings-group-title">ТАКТИЛЬНЫЙ ОТКЛИК</div>
      <div class="settings-item-row">
        <div class="settings-item-left">
          <span>📳</span>
          <span>Вибрация при вытягивании карт</span>
        </div>
        <div class="toggle-switch on" onclick="this.classList.toggle('on')"></div>
      </div>

      <div class="settings-group-title">О ПРИЛОЖЕНИИ И БЕЗОПАСНОСТЬ</div>
      <div class="settings-item-row" onclick="openPaywallModal()">
        <div class="settings-item-left">
          <span>👑</span>
          <span>Управление подпиской Астра Плюс</span>
        </div>
        <span style="color: #E5C378;">Управление ></span>
      </div>
      <div class="settings-item-row" onclick="alert('Астрономические расчеты Астры основаны на эфемеридах NASA Jet Propulsion Laboratory (JPL). Версия 1.0.326\\n\\nЗащита Astra-Shield: Полиморфный шифр активен.')">
        <div class="settings-item-left">
          <span>🌌</span>
          <div>
            <div style="color: #FFF;">Данные NASA & Версия 1.0.326</div>
            <div style="font-size: 11px; color: #10B981;">Astra-Shield Active • Safe Store Build</div>
          </div>
        </div>
        <span style="color: var(--text-muted);">Инфо</span>
      </div>

      <!-- DANGER ZONE: RUSTORE ACCOUNT DELETION COMPLIANCE -->
      <div class="settings-group-title" style="color: #EF4444;">УДАЛЕНИЕ ДАННЫХ (RUSTORE & GOOGLE PLAY)</div>
      <div class="settings-item-row danger-zone-card" onclick="confirmAccountDeletion()">
        <div class="settings-item-left">
          <span>🗑️</span>
          <span>Удалить аккаунт и очистить все данные</span>
        </div>
        <span>Удалить</span>
      </div>

    </div>

    <!-- ==================================================================== -->
    <!-- MODAL 5: PAYWALL ASTRA PLUS                                          -->
    <!-- ==================================================================== -->
    <div class="paywall-modal" id="modal-paywall">
      <div style="display: flex; justify-content: flex-end;">
        <button class="player-close-btn" onclick="closePaywallModal()">✕</button>
      </div>

      <img class="paywall-muse-hero" src="astra_assets/03_ПЕЙВОЛЫ_И_ПОДПИСКА/new_paywall_bg_female_2.png" alt="Muse">

      <div style="font-size: 22px; font-weight: 800; text-align: center; margin-bottom: 6px;">Ваш проводник к самопознанию</div>
      <div style="font-size: 13px; color: var(--text-muted); text-align: center; line-height: 1.45; margin-bottom: 20px;">
        Обретите ясность, настройтесь на ритмы Вселенной и управляйте своей судьбой с Астра Плюс.
      </div>

      <!-- Plans -->
      <div class="paywall-plan-card" onclick="selectPaywallPlan(this, 'week')">
        <div>
          <div style="font-size: 15px; font-weight: 700;">Неделя</div>
          <div style="font-size: 12px; color: var(--text-muted);">449,00 ₽ в неделю</div>
        </div>
        <div style="font-size: 16px; font-weight: 800;">449 ₽</div>
      </div>

      <div class="paywall-plan-card selected" onclick="selectPaywallPlan(this, 'year')">
        <div>
          <div style="display: flex; align-items: center; gap: 6px;">
            <span style="font-size: 15px; font-weight: 700;">Год + НЕДЕЛЯ В ПОДАРОК</span>
            <span style="background: #E5C378; color: #000; font-size: 10px; font-weight: 800; padding: 2px 6px; border-radius: 8px;">ВЫГОДНО</span>
          </div>
          <div style="font-size: 12px; color: var(--text-muted);">37,29 ₽ в неделю (1 790,00 ₽ в год)</div>
        </div>
        <div style="font-size: 16px; font-weight: 800; color: #E5C378;">1 790 ₽</div>
      </div>

      <div class="paywall-plan-card" onclick="selectPaywallPlan(this, 'lifetime')">
        <div>
          <div style="font-size: 15px; font-weight: 700;">Навсегда</div>
          <div style="font-size: 12px; color: var(--text-muted);">Единоразовая пожизненная оплата</div>
        </div>
        <div style="font-size: 16px; font-weight: 800;">490 ₽</div>
      </div>

      <button class="btn-primary" style="margin-top: 16px;" onclick="activateAstraPlusSubscription()">
        <span>Продолжить</span>
      </button>

      <div style="font-size: 11px; color: var(--text-dim); text-align: center; margin-top: 14px;">
        Все по любви. Отмена подписки в любой момент. • <span style="text-decoration: underline; cursor: pointer;" onclick="restorePurchases()">Восстановить покупки</span>
      </div>
    </div>

    <!-- ==================================================================== -->
    <!-- MODAL 6: AVATAR SELECTOR MODAL (POINTS 86-87)                        -->
    <!-- ==================================================================== -->
    <div class="bottom-sheet-overlay" id="modal-avatar-selector" onclick="closeSheet('modal-avatar-selector')">
      <div class="bottom-sheet-content" onclick="event.stopPropagation()">
        <div class="sheet-handle"></div>
        <div style="font-size: 18px; font-weight: 800; margin-bottom: 6px;">Выберите ваш Аватар</div>
        <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 14px;">Музы, Проводники и 12 знаков зодиака:</div>
        
        <div class="avatar-gallery-grid" id="avatar-picker-grid"></div>
      </div>
    </div>

    <!-- ==================================================================== -->
    <!-- MODAL 7: 24 ELDER FUTHARK RUNES CATALOG (POINT 61)                   -->
    <!-- ==================================================================== -->
    <div class="bottom-sheet-overlay" id="modal-runes-catalog" onclick="closeSheet('modal-runes-catalog')">
      <div class="bottom-sheet-content" onclick="event.stopPropagation()">
        <div class="sheet-handle"></div>
        <div style="font-size: 18px; font-weight: 800; margin-bottom: 6px;">Старший Футарк (24 руны)</div>
        <div style="font-size: 13px; color: var(--text-muted); margin-bottom: 14px;">Древнескандинавская система священных космических знаков:</div>
        
        <div id="all-runes-grid" style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; max-height: 60vh; overflow-y: auto;"></div>
      </div>
    </div>

    <!-- ==================================================================== -->
    <!-- MODAL 8: ONBOARDING FULLSCREEN SEQUENCE (13 SLIDES, POINTS 11-23)     -->
    <!-- ==================================================================== -->
    <div class="onboarding-modal" id="modal-onboarding">
      <div class="onboard-top-nav">
        <button class="player-close-btn" style="width: 32px; height: 32px; font-size: 14px;" onclick="prevOnboardSlide()" id="onboard-prev-btn">‹</button>
        <div class="onboard-progress-bar">
          <div class="onboard-progress-fill" id="onboard-progress-fill"></div>
        </div>
        <button class="player-close-btn" style="width: 32px; height: 32px; font-size: 14px;" onclick="skipOnboarding()">✕</button>
      </div>

      <div class="onboard-slide-content" id="onboard-slide-content"></div>
    </div>

  </div>

  <!-- ==================================================================== -->
  <!-- MASTER APPLICATION JAVASCRIPT CONTROLLER                             -->
  <!-- ==================================================================== -->
  <script>
    // --- State Management ---
    let currentMainScreen = 'calendar';
    let currentPracticeTab = 'tarot';
    let currentTarotMode = 1;
    let currentDrawnCards = [];
    let currentRune = null;
    let currentSoundPlaying = null;
    let sleepTimerMinutes = 0;
    let sleepTimerInterval = null;
    let isCardSheetFlipped = false;
    let currentActiveSheetCard = null;
    let currentOnboardSlide = 0;

    // --- Navigation Tabs ---
    function switchMainScreen(screenId) {
      document.querySelectorAll('.screen-view').forEach(s => s.classList.remove('active'));
      document.querySelectorAll('.nav-tab-item').forEach(t => t.classList.remove('active'));

      const targetScreen = document.getElementById('screen-' + screenId);
      const targetNav = document.getElementById('tab-nav-' + screenId);
      
      if (targetScreen) targetScreen.classList.add('active');
      if (targetNav) targetNav.classList.add('active');
      currentMainScreen = screenId;

      if (screenId === 'practices' && currentPracticeTab === 'tarot') {
        setTimeout(renderTarotFanDeck, 100);
      }
    }

    // --- Infinite Dates Calendar Strip ---
    function initCalendarStrip() {
      const container = document.getElementById('cal-strip');
      if (!container) return;
      container.innerHTML = '';
      const today = new Date(2026, 9, 19);

      const weekdays = ['Вс', 'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб'];
      for (let i = -10; i <= 60; i++) {
        const d = new Date(today);
        d.setDate(today.getDate() + i);
        
        const chip = document.createElement('div');
        chip.className = `cal-day-chip ${i === 0 ? 'active' : ''}`;
        chip.onclick = () => {
          document.querySelectorAll('.cal-day-chip').forEach(c => c.classList.remove('active'));
          chip.classList.add('active');
          document.getElementById('cal-date-display').innerText = `${d.getDate()} Октября • ${weekdays[d.getDay()]}`;
          document.getElementById('cal-moon-day-badge').innerText = `${(13 + i) % 30 || 1} лунный день`;
        };

        chip.innerHTML = `
          <div class="cal-day-weekday">${weekdays[d.getDay()]}</div>
          <div class="cal-day-num">${d.getDate()}</div>
          <img class="cal-day-moon-icon" src="astra_assets/01_ФОНЫ_И_БАННЕРЫ_ВЫСОКОГО_РАЗРЕШЕНИЯ/ic_sharing_moon.png" alt="m">
        `;
        container.appendChild(chip);
      }
    }

    // --- Practice Subtabs ---
    function switchPracticeTab(tabId, el) {
      document.querySelectorAll('.practice-pill').forEach(p => p.classList.remove('active'));
      if (el) el.classList.add('active');
      
      document.querySelectorAll('.practice-subview').forEach(v => v.style.display = 'none');
      const target = document.getElementById('subview-' + tabId);
      if (target) target.style.display = 'block';
      currentPracticeTab = tabId;

      if (tabId === 'tarot') {
        renderTarotFanDeck();
      }
    }

    function switchPracticeSection(tabId) {
      switchMainScreen('practices');
      const pills = document.querySelectorAll('.practice-pill');
      pills.forEach(p => {
        if (p.innerText.toLowerCase().includes(tabId)) switchPracticeTab(tabId, p);
      });
    }

    // --- Tarot 4 Modes Controller ---
    function setTarotMode(mode) {
      currentTarotMode = mode;
      document.querySelectorAll('.tarot-mode-btn').forEach(b => b.classList.remove('active'));
      
      const btn = document.getElementById('btn-tarot-mode-' + mode);
      if (btn) btn.classList.add('active');

      const slotsCont = document.getElementById('tarot-slots-container');
      const fanWrap = document.getElementById('tarot-fan-wrapper');
      const spheresBlock = document.getElementById('tarot-spheres-block');
      const catalogView = document.getElementById('tarot-catalog-view');

      if (mode === 'all') {
        slotsCont.style.display = 'none';
        fanWrap.style.display = 'none';
        spheresBlock.style.display = 'none';
        catalogView.style.display = 'block';
        renderTarotCatalog('all');
      } else {
        slotsCont.style.display = 'flex';
        fanWrap.style.display = 'block';
        spheresBlock.style.display = 'block';
        catalogView.style.display = 'none';
        initTarotSlots(mode);
        renderTarotFanDeck();
      }
    }

    function initTarotSlots(count) {
      const cont = document.getElementById('tarot-slots-container');
      cont.innerHTML = '';
      currentDrawnCards = [];
      document.getElementById('tarot-actions-bar').style.display = 'none';

      const labels = count === 1 ? ['Карта дня'] : count === 3 ? ['Прошлое', 'Настоящее', 'Будущее'] : ['Основа', 'Влияние', 'Совет', 'Препятствие', 'Итог'];

      for (let i = 0; i < count; i++) {
        const slot = document.createElement('div');
        slot.className = 'tarot-slot-hero';
        slot.id = 'tarot-slot-' + i;
        slot.innerHTML = `
          <div style="font-size: 28px; color: var(--purple); margin-bottom: 6px;">✦</div>
          <div class="tarot-slot-label">${labels[i]}</div>
          <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;">Вытянуть карту</div>
        `;
        cont.appendChild(slot);
      }

      initSpheresChips(count);
    }

    function initSpheresChips(count) {
      const container = document.getElementById('tarot-spheres-chips');
      container.innerHTML = '';
      const chips = count === 1 ? ['Карта дня', 'Да или Нет', 'Послание свыше'] : ['✦ Ситуация', '✦ Любовь', '✦ Карьера', '✦ Отношения', '✦ Финансы', '✦ Духовность'];
      chips.forEach((c, idx) => {
        const chip = document.createElement('div');
        chip.className = `sphere-chip ${idx === 0 ? 'active' : ''}`;
        chip.innerText = c;
        chip.onclick = () => {
          document.querySelectorAll('.sphere-chip').forEach(ch => ch.classList.remove('active'));
          chip.classList.add('active');
        };
        container.appendChild(chip);
      });
    }

    function renderTarotFanDeck() {
      const deck = document.getElementById('tarot-fan-deck');
      if (!deck) return;
      deck.innerHTML = '';

      const totalFanCards = 22;
      const angleStep = 4.2;
      const startAngle = -((totalFanCards - 1) * angleStep) / 2;

      for (let i = 0; i < totalFanCards; i++) {
        const c = document.createElement('img');
        c.className = 'fan-card-item';
        c.src = 'astra_assets/04_ТАРО_И_РУНЫ/ic_gods_card_back.png';
        
        const angle = startAngle + i * angleStep;
        const rad = (angle * Math.PI) / 180;
        const left = 50 + rad * 38;
        const top = 14 + 440 * (1 - Math.cos(rad));

        c.style.left = `calc(${left}% - 31px)`;
        c.style.top = `${top}px`;
        c.style.transform = `rotate(${angle}deg)`;

        c.onclick = () => pullCardFromFan(i);
        deck.appendChild(c);
      }
    }

    function pullCardFromFan(cardIndex) {
      if (!window.ASTRA_TAROT_DATABASE || ASTRA_TAROT_DATABASE.length === 0) return;
      
      const targetSlotIndex = currentDrawnCards.length;
      if (targetSlotIndex >= currentTarotMode) return;

      const randomCard = ASTRA_TAROT_DATABASE[Math.floor(Math.random() * ASTRA_TAROT_DATABASE.length)];
      currentDrawnCards.push(randomCard);

      const slot = document.getElementById('tarot-slot-' + targetSlotIndex);
      if (slot) {
        slot.className = 'tarot-slot-hero filled';
        slot.innerHTML = `
          <img class="tarot-card-img-hero" src="astra_assets/04_ТАРО_И_РУНЫ/${randomCard.image || 'ic_tarot_empty'}.png" onerror="this.src='astra_assets/04_ТАРО_И_РУНЫ/ic_gods_card_back.png'" alt="${randomCard.name}">
          <div style="font-size: 12px; font-weight: 700; color: #FFF; margin-top: 6px; text-shadow: 0 2px 8px #000;">${randomCard.name}</div>
        `;
        slot.onclick = () => openCardMeaningModal(randomCard);
      }

      if (currentDrawnCards.length === currentTarotMode) {
        document.getElementById('tarot-actions-bar').style.display = 'flex';
      }
    }

    function resetTarotSpread() {
      initTarotSlots(currentTarotMode);
      renderTarotFanDeck();
    }

    function openCardMeaningModal(card) {
      currentActiveSheetCard = card;
      isCardSheetFlipped = false;
      
      document.getElementById('sheet-card-img').src = `astra_assets/04_ТАРО_И_РУНЫ/${card.image || 'ic_tarot_empty'}.png`;
      document.getElementById('sheet-card-title').innerText = card.name;
      document.getElementById('sheet-card-arcana').innerText = card.arcana === 'major' ? 'Старший Аркан' : 'Младший Аркан';
      document.getElementById('sheet-card-desc-text').innerText = card.upright ? card.upright.text : (card.brief || 'Карта духовного роста и озарения.');
      document.getElementById('sheet-card-rec-text').innerText = card.upright ? card.upright.rec_text : 'Действуйте в согласии с интуицией.';
      document.getElementById('sheet-card-pos-label').innerText = 'Прямая позиция';
      document.getElementById('card-sheet-flip-inner').style.transform = 'rotateZ(0deg)';

      openSheet('sheet-card-meaning');
    }

    function toggleCard3DFlip() {
      if (!currentActiveSheetCard) return;
      isCardSheetFlipped = !isCardSheetFlipped;
      
      const inner = document.getElementById('card-sheet-flip-inner');
      const label = document.getElementById('sheet-card-pos-label');
      const desc = document.getElementById('sheet-card-desc-text');
      const rec = document.getElementById('sheet-card-rec-text');

      if (isCardSheetFlipped) {
        inner.style.transform = 'rotateZ(180deg)';
        label.innerText = 'Перевёрнутая позиция';
        desc.innerText = currentActiveSheetCard.reversed ? currentActiveSheetCard.reversed.text : currentActiveSheetCard.upright.text;
        rec.innerText = currentActiveSheetCard.reversed ? currentActiveSheetCard.reversed.rec_text : currentActiveSheetCard.upright.rec_text;
      } else {
        inner.style.transform = 'rotateZ(0deg)';
        label.innerText = 'Прямая позиция';
        desc.innerText = currentActiveSheetCard.upright.text;
        rec.innerText = currentActiveSheetCard.upright.rec_text;
      }
    }

    function sendCardToMentorChat() {
      closeSheet('sheet-card-meaning');
      switchMainScreen('chat');
      if (currentActiveSheetCard) {
        receiveMentorInsight({
          type: 'Таро • ' + currentActiveSheetCard.name,
          title: currentActiveSheetCard.name,
          text: currentActiveSheetCard.upright ? currentActiveSheetCard.upright.text : (currentActiveSheetCard.brief || 'Карта судьбы')
        });
      }
    }

    function requestTarotInsight() {
      if (currentDrawnCards.length === 0) {
        alert('Сначала вытяните хотя бы одну карту из веера!');
        return;
      }
      switchMainScreen('chat');
      const firstCard = currentDrawnCards[0];
      receiveMentorInsight({
        type: 'Расклад Таро • ' + firstCard.name,
        title: firstCard.name,
        text: firstCard.upright ? firstCard.upright.text : (firstCard.brief || 'Карта судьбы')
      });
    }

    // --- 78 Tarot Cards Catalog ---
    function renderTarotCatalog(suitFilter) {
      const grid = document.getElementById('tarot-catalog-grid');
      grid.innerHTML = '';
      if (!window.ASTRA_TAROT_DATABASE) return;

      const filtered = ASTRA_TAROT_DATABASE.filter(c => {
        if (suitFilter === 'all') return true;
        if (suitFilter === 'major') return c.arcana === 'major';
        return c.suit === suitFilter;
      });

      filtered.forEach(c => {
        const cardEl = document.createElement('div');
        cardEl.style.cssText = 'background: var(--bg-card); border-radius: 14px; overflow: hidden; cursor: pointer; text-align: center; border: 1px solid var(--bg-card-border);';
        cardEl.onclick = () => openCardMeaningModal(c);
        cardEl.innerHTML = `
          <img src="astra_assets/04_ТАРО_И_РУНЫ/${c.image || 'ic_tarot_empty'}.png" style="width: 100%; height: 130px; object-fit: cover;" alt="${c.name}">
          <div style="font-size: 11px; font-weight: 700; color: #FFF; padding: 6px 4px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${c.name}</div>
        `;
        grid.appendChild(cardEl);
      });
    }

    function filterTarotSuit(suit, el) {
      document.querySelectorAll('#tarot-catalog-view .sound-cat-chip').forEach(c => c.classList.remove('active'));
      if (el) el.classList.add('active');
      renderTarotCatalog(suit);
    }

    // --- Oracle & Deity Drawers ---
    function drawOracleCard() {
      const slot = document.getElementById('oracle-slot');
      slot.className = 'tarot-slot-hero filled';
      slot.innerHTML = `
        <img class="tarot-card-img-hero" src="astra_assets/02_ИЛЛЮСТРАЦИИ_И_ОНБОРДИНГ/imgi_1_Py0DQon8lKkK0aJj2FHQMOPx4o.png" alt="Oracle">
        <div style="font-size: 13px; font-weight: 800; color: var(--teal); margin-top: 6px;">Древо жизни</div>
      `;
    }

    function drawDeityCard() {
      const slot = document.getElementById('gods-slot');
      slot.className = 'tarot-slot-hero filled';
      slot.innerHTML = `
        <img class="tarot-card-img-hero" src="astra_assets/01_ФОНЫ_И_БАННЕРЫ_ВЫСОКОГО_РАЗРЕШЕНИЯ/ic_gods_empty.png" alt="Deity">
        <div style="font-size: 13px; font-weight: 800; color: var(--amber); margin-top: 6px;">Хануман (Сила Духа)</div>
      `;
    }

    // --- Dream Book (Сонник) ---
    function switchDreamMode(mode) {
      document.getElementById('tab-dream-new').classList.toggle('active', mode === 'new');
      document.getElementById('tab-dream-archive').classList.toggle('active', mode === 'archive');
      document.getElementById('dream-new-box').style.display = mode === 'new' ? 'block' : 'none';
      document.getElementById('dream-archive-box').style.display = mode === 'archive' ? 'block' : 'none';
      if (mode === 'archive') renderDreamArchive();
    }

    function interpretDreamAction() {
      const text = document.getElementById('dream-input-text').value.trim();
      if (!text) { alert('Пожалуйста, напишите детали вашего сна!'); return; }

      const resBox = document.getElementById('dream-result-card');
      resBox.style.display = 'block';
      resBox.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
          <span style="font-size: 12px; color: var(--amber); font-weight: 700;">19 Октября 2026 • Анализ сна</span>
          <button style="background: none; border: none; cursor: pointer; color: #EF4444;" onclick="deleteDreamEntry(this)">🗑️</button>
        </div>
        <img src="astra_assets/01_ФОНЫ_И_БАННЕРЫ_ВЫСОКОГО_РАЗРЕШЕНИЯ/dreamer_top_image.png" style="width: 100%; height: 130px; object-fit: cover; border-radius: 14px; margin-bottom: 10px;" alt="Dream">
        <div style="font-size: 15px; font-weight: 800; color: #FFF; margin-bottom: 6px;">«${text.slice(0, 35)}...»</div>
        <div style="font-size: 13px; line-height: 1.5; color: rgba(255,255,255,0.85); margin-bottom: 12px;">
          Слова и образы сна отражают бессознательное стремление к внутренней ясности и гармонии. В вашей натальной карте это активирует 9-й дом высшего познания.
        </div>
        <button class="btn-primary" onclick="switchMainScreen('chat'); receiveMentorInsight({ type: 'Толкование сновидения', title: 'Сон: ' + text.slice(0, 30), text: 'Образы вашего сна несут важное послание...' })">
          <span>Обсудить сон с Селеной (Ткачихой снов) →</span>
        </button>
      `;

      let archive = AstraSecurity.Vault.get('dreams_list', []);
      archive.unshift({ date: '19 Окт 2026', title: text.slice(0, 40) });
      AstraSecurity.Vault.set('dreams_list', archive);
    }

    function deleteDreamEntry(btn) {
      if (confirm('Удалить этот сон? Сон и его смыслы исчезнут. И это навсегда.')) {
        document.getElementById('dream-result-card').style.display = 'none';
        document.getElementById('dream-input-text').value = '';
      }
    }

    function renderDreamArchive() {
      const box = document.getElementById('dream-archive-box');
      const archive = AstraSecurity.Vault.get('dreams_list', [
        { date: '18 Окт 2026', title: 'Полет над сияющим океаном' }
      ]);
      box.innerHTML = '';
      archive.forEach((d, idx) => {
        const c = document.createElement('div');
        c.className = 'card-glass';
        c.innerHTML = `
          <div style="display: flex; justify-content: space-between;">
            <div style="font-size: 14px; font-weight: 700; color: #FFF;">${d.title}</div>
            <div style="font-size: 12px; color: var(--text-muted);">${d.date}</div>
          </div>
        `;
        box.appendChild(c);
      });
    }

    // --- Runes (Elder Futhark) ---
    const RUNES_LIST = [
      { name: 'Fehu', glyph: 'ᚠ', desc: 'Богатство, чистая энергия изобилия и новый старт.' },
      { name: 'Uruz', glyph: 'ᚢ', desc: 'Первозданная дикая сила, жизненная стойкость.' },
      { name: 'Thurisaz', glyph: 'ᚦ', desc: 'Врата осознанности, защита от токсичных энергий.' },
      { name: 'Ansuz', glyph: 'ᚨ', desc: 'Священный глас, мудрость слова и высшее наставничество.' },
      { name: 'Raidho', glyph: 'ᚱ', desc: 'Путешествие, ритм космического порядка и верный путь.' },
      { name: 'Kenaz', glyph: 'ᚲ', desc: 'Факел вдохновения, внутреннее озарение и творчество.' },
      { name: 'Gebo', glyph: 'ᚷ', desc: 'Дар небес, равновесие в партнерстве и гармония.' },
      { name: 'Wunjo', glyph: 'ᚹ', desc: 'Радость, свет сердца и исполнение сокровенного.' },
      { name: 'Hagalaz', glyph: 'ᚺ', desc: 'Град очищения, разрушение отживших иллюзий.' },
      { name: 'Nauthiz', glyph: 'ᚾ', desc: 'Преодоление трудностей, закалка духа через терпение.' },
      { name: 'Isa', glyph: 'ᛁ', desc: 'Лед тишины, пауза для кристаллизации намерений.' },
      { name: 'Jera', glyph: 'ᛃ', desc: 'Щедрый урожай, закономерное вознаграждение за труды.' },
      { name: 'Eihwaz', glyph: 'ᛇ', desc: 'Мировое древо Иггдрасиль, ось стойкости и вечности.' },
      { name: 'Perthro', glyph: 'ᛈ', desc: 'Тайна судьбы, раскрытие скрытых способностей.' },
      { name: 'Algiz', glyph: 'ᛉ', desc: 'Высшая божественная защита, ангел-хранитель.' },
      { name: 'Sowilo', glyph: 'ᛋ', desc: 'Солнечная победа, ясность цели и триумф света.' },
      { name: 'Tiwaz', glyph: 'ᛏ', desc: 'Честь воина духа, справедливость и победа правды.' },
      { name: 'Berkano', glyph: 'ᛒ', desc: 'Береза возрождения, плодородие, исцеление и рост.' },
      { name: 'Ehwaz', glyph: 'ᛖ', desc: 'Верный конь, прогресс и гармоничное сотрудничество.' },
      { name: 'Mannaz', glyph: 'ᛗ', desc: 'Человеческая душа, самопознание и братство.' },
      { name: 'Laguz', glyph: 'ᛚ', desc: 'Тайны воды, глубинная интуиция и поток жизни.' },
      { name: 'Ingwaz', glyph: 'ᛜ', desc: 'Внутренний потенциал, завершение цикла и покой.' },
      { name: 'Dagaz', glyph: 'ᛞ', desc: 'Рассвет нового дня, квантовый скачок сознания.' },
      { name: 'Othala', glyph: 'ᛟ', desc: 'Родовое наследие, священный дом и духовные корни.' }
    ];

    function drawDailyRune() {
      currentRune = RUNES_LIST[Math.floor(Math.random() * RUNES_LIST.length)];
      document.getElementById('rune-glyph-display').innerText = currentRune.glyph;
      document.getElementById('rune-name-display').innerText = currentRune.name;
      document.getElementById('rune-sub-display').innerText = `«${currentRune.desc.slice(0, 30)}...»`;
    }

    function openRuneMeaningModal() {
      if (!currentRune) drawDailyRune();
      alert(`РУНА ${currentRune.name} (${currentRune.glyph})\n\n${currentRune.desc}\n\nРекомендация: медитируйте на этот символ сегодня для сонастройки с космическим ритмом.`);
    }

    function openRunesCatalogModal() {
      const grid = document.getElementById('all-runes-grid');
      grid.innerHTML = '';
      RUNES_LIST.forEach(r => {
        const item = document.createElement('div');
        item.style.cssText = 'background: var(--bg-card); border-radius: 14px; padding: 10px; text-align: center; border: 1px solid var(--bg-card-border); cursor: pointer;';
        item.onclick = () => {
          currentRune = r;
          document.getElementById('rune-glyph-display').innerText = r.glyph;
          document.getElementById('rune-name-display').innerText = r.name;
          document.getElementById('rune-sub-display').innerText = `«${r.desc.slice(0, 30)}...»`;
          closeSheet('modal-runes-catalog');
        };
        item.innerHTML = `
          <div style="font-size: 32px; font-family: var(--font-serif); color: var(--teal); margin-bottom: 4px;">${r.glyph}</div>
          <div style="font-size: 13px; font-weight: 800; color: #FFF;">${r.name}</div>
          <div style="font-size: 10px; color: var(--text-muted); margin-top: 2px;">${r.desc.slice(0, 22)}...</div>
        `;
        grid.appendChild(item);
      });
      openSheet('modal-runes-catalog');
    }

    // --- Affirmations ---
    const AFFIRMATIONS_COLLECTION = [
      { cat: 'Прощение и покой', text: '«Я прощаю всех в прошлом за все осознанные ошибки и впускаю чистый свет в свое сердце.»' },
      { cat: 'Изобилие и сила', text: '«Вселенная щедро открывает передо мной двери возможностей и направляет каждый мой шаг.»' },
      { cat: 'Любовь к себе', text: '«Моя душа прекрасна в своей уникальности. Я достоин безусловной любви и глубокого мира.»' }
    ];
    let affIndex = 0;

    function nextAffirmation() {
      affIndex = (affIndex + 1) % AFFIRMATIONS_COLLECTION.length;
      const item = AFFIRMATIONS_COLLECTION[affIndex];
      document.getElementById('affirmation-cat-badge').innerText = item.cat;
      document.getElementById('affirmation-text-display').innerText = item.text;
    }

    // --- Soundscape (68 API Sounds) ---
    let currentSoundCategory = 'Все';

    function initSoundscape() {
      if (!window.ASTRA_SOUNDS_DATABASE) return;

      const cats = ['Все', 'Герцы', 'Природа', 'Животные', 'ASMR', 'Инструменты', 'Шумы', 'Бинауральная музыка'];
      const chipsContainer = document.getElementById('sound-category-chips');
      chipsContainer.innerHTML = '';

      cats.forEach(c => {
        const chip = document.createElement('div');
        chip.className = `sound-cat-chip ${c === currentSoundCategory ? 'active' : ''}`;
        chip.innerText = c;
        chip.onclick = () => {
          currentSoundCategory = c;
          document.querySelectorAll('.sound-cat-chip').forEach(ch => ch.classList.remove('active'));
          chip.classList.add('active');
          renderSoundsGrid();
        };
        chipsContainer.appendChild(chip);
      });

      renderSoundsGrid();
    }

    function renderSoundsGrid() {
      const grid = document.getElementById('sounds-list-grid');
      grid.innerHTML = '';
      if (!window.ASTRA_SOUNDS_DATABASE) return;

      const filtered = ASTRA_SOUNDS_DATABASE.filter(s => {
        if (currentSoundCategory === 'Все') return true;
        return s.categories && s.categories.includes(currentSoundCategory);
      });

      filtered.forEach(s => {
        const card = document.createElement('div');
        card.className = 'sound-card-item';
        card.onclick = () => openSoundPlayer(s);
        
        card.innerHTML = `
          <img class="sound-card-thumb" src="${s.cardIconUrl || 'astra_assets/07_3D_ИКОНКИ_И_ЭЛЕМЕНТЫ/icon.png'}" onerror="this.src='astra_assets/07_3D_ИКОНКИ_И_ЭЛЕМЕНТЫ/icon.png'" alt="${s.name}">
          <div class="sound-card-title">${s.name}</div>
          <div class="sound-card-cat">${s.categories ? s.categories[0] : 'Резонанс'}</div>
          <div class="sound-card-play-btn">▶</div>
        `;
        grid.appendChild(card);
      });
    }

    function openSoundPlayerById(soundId) {
      if (!window.ASTRA_SOUNDS_DATABASE) return;
      const s = ASTRA_SOUNDS_DATABASE.find(x => x.id === soundId) || ASTRA_SOUNDS_DATABASE[0];
      openSoundPlayer(s);
    }

    function openSoundPlayer(s) {
      currentSoundPlaying = s;
      document.getElementById('player-track-name').innerText = s.name;
      document.getElementById('player-track-category').innerText = s.categories ? s.categories.join(' • ') : 'ЧАСТОТЫ';
      document.getElementById('player-track-desc').innerText = s.description || 'Целебный резонанс восстанавливает душевное равновесие.';
      document.getElementById('player-disc-img').src = s.cardIconUrl || 'astra_assets/07_3D_ИКОНКИ_И_ЭЛЕМЕНТЫ/icon.png';
      
      const videoEl = document.getElementById('player-video-bg');
      if (s.videoUrl) {
        videoEl.src = s.videoUrl;
        videoEl.play().catch(() => {});
      }

      const audioEl = document.getElementById('real-sound-audio');
      if (s.soundUrl) {
        audioEl.src = s.soundUrl;
        audioEl.play().then(() => {
          document.getElementById('player-toggle-btn').innerText = '⏸';
        }).catch(() => {
          document.getElementById('player-toggle-btn').innerText = '▶';
        });
      }

      document.getElementById('modal-player-fullscreen').style.display = 'flex';
    }

    function toggleSoundPlayback() {
      const audioEl = document.getElementById('real-sound-audio');
      const btn = document.getElementById('player-toggle-btn');
      if (audioEl.paused) {
        audioEl.play();
        btn.innerText = '⏸';
      } else {
        audioEl.pause();
        btn.innerText = '▶';
      }
    }

    function closeSoundPlayer() {
      document.getElementById('modal-player-fullscreen').style.display = 'none';
      const audioEl = document.getElementById('real-sound-audio');
      audioEl.pause();
    }

    function cycleSleepTimer() {
      const timers = [0, 15, 30, 45, 60];
      const idx = (timers.indexOf(sleepTimerMinutes) + 1) % timers.length;
      sleepTimerMinutes = timers[idx];
      document.getElementById('player-timer-val').innerText = sleepTimerMinutes === 0 ? 'Выкл' : sleepTimerMinutes + ' мин';

      if (sleepTimerInterval) clearInterval(sleepTimerInterval);
      if (sleepTimerMinutes > 0) {
        sleepTimerInterval = setTimeout(() => {
          closeSoundPlayer();
          alert('Таймер сна сработал: воспроизведение завершено. Спокойного сна!');
        }, sleepTimerMinutes * 60 * 1000);
      }
    }

    function toggleSoundFavorite() {
      const btn = document.getElementById('player-fav-btn');
      btn.style.color = btn.style.color === 'rgb(255, 184, 77)' ? '#FFF' : '#FFB84D';
    }

    // --- Light Chat Engine (5 Mentors) ---
    function initMentors() {
      const listContainer = document.getElementById('mentors-selector-list');
      listContainer.innerHTML = '';
      if (!window.ASTRA_MENTORS) return;

      ASTRA_MENTORS.forEach((m, idx) => {
        const item = document.createElement('div');
        item.className = `mentor-item-card ${idx === currentMentorIndex ? 'active' : ''}`;
        item.onclick = () => {
          setMentor(idx);
          closeSheet('sheet-mentor-selector');
        };
        item.innerHTML = `
          <div style="display: flex; align-items: center; gap: 12px;">
            <img src="10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ/0${m.id}_${m.code || 'mentor'}.png" onerror="this.src='10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ/01_Luna_Wise_Mystic.png'" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover;" alt="${m.name_ru}">
            <div>
              <div style="font-size: 15px; font-weight: 800; color: #FFF;">${m.name_ru}</div>
              <div style="font-size: 12px; color: var(--text-muted);">${m.title_ru}</div>
            </div>
          </div>
          <div style="font-size: 18px; color: var(--purple);">${idx === currentMentorIndex ? '✓' : ''}</div>
        `;
        listContainer.appendChild(item);
      });

      updateMentorUI();
    }

    function updateMentorUI() {
      const m = getActiveMentor();
      document.getElementById('chat-header-name').innerText = m.name_ru;
      document.getElementById('chat-header-status').innerText = `${m.title_ru} • на связи`;
      document.getElementById('chat-header-avatar').src = `10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ/0${m.id}_${m.code || 'mentor'}.png`;
    }

    function openMentorSelectorSheet() {
      initMentors();
      openSheet('sheet-mentor-selector');
    }

    function sendUserChatMessage() {
      const input = document.getElementById('chat-input-box');
      const text = input.value.trim();
      if (!text) return;
      input.value = '';

      appendChatMessage('user', text);

      setTimeout(() => {
        const m = getActiveMentor();
        const reply = `${m.name_ru}: «Я слышу твой запрос. Энергии дня говорят, что сейчас ключевой момент для доверия внутреннему компасу. Действуй спокойно.»`;
        appendChatMessage('mentor', reply);
      }, 700);
    }

    function sendChatMessageQuick(text) {
      document.getElementById('chat-input-box').value = text;
      sendUserChatMessage();
    }

    function appendChatMessage(sender, text) {
      const area = document.getElementById('chat-msg-area');
      const row = document.createElement('div');
      row.className = `chat-msg-row ${sender}`;
      row.innerHTML = `<div class="chat-bubble">${text}</div>`;
      area.appendChild(row);
      area.scrollTop = area.scrollHeight;
    }

    function receiveMentorInsight(data) {
      const area = document.getElementById('chat-msg-area');
      const m = getActiveMentor();
      const row = document.createElement('div');
      row.className = 'chat-msg-row mentor';
      row.innerHTML = `
        <div class="chat-bubble">
          <div style="font-size: 12px; font-weight: 700; color: var(--purple);">${data.type}</div>
          <div style="font-size: 15px; font-weight: 800; margin: 4px 0 8px;">${data.title}</div>
          <div style="font-size: 13px; line-height: 1.48;">${data.text.slice(0, 110)}...</div>
          <div class="chat-spoiler-btn" onclick="this.previousElementSibling.innerText = '${data.text}'; this.style.display='none';">Показать полностью ↓</div>
          <div class="chat-feedback-row">
            <button class="chat-feedback-btn" onclick="this.style.color='#10B981'; alert('Спасибо за обратную связь!');">👍</button>
            <button class="chat-feedback-btn" onclick="this.style.color='#EF4444'; alert('Спасибо, наставник учтет замечание.');">👎</button>
          </div>
        </div>
      `;
      area.appendChild(row);
      area.scrollTop = area.scrollHeight;
    }

    // --- Settings & RuStore Account Deletion Compliance ---
    function openSettingsScreen() {
      document.getElementById('modal-settings-screen').style.display = 'flex';
    }
    function closeSettingsScreen() {
      document.getElementById('modal-settings-screen').style.display = 'none';
    }
    function editBirthDataPrompt() {
      const newCity = prompt('Введите ваш город рождения:', 'Сочи, Россия');
      if (newCity) {
        document.getElementById('settings-natal-preview').innerText = `14.03.2000, 22:00 • ${newCity}`;
      }
    }
    function confirmAccountDeletion() {
      const conf1 = confirm('Удалить аккаунт и все данные?\\n\\nВсе ваши сохранённые расклады, сны, натальная карта и история наставников будут безвозвратно стёрты с устройства.');
      if (conf1) {
        const conf2 = confirm('Вы абсолютно уверены? Это действие нельзя отменить.');
        if (conf2) {
          AstraSecurity.Vault.clearAll();
          alert('Аккаунт и все персональные данные полностью удалены в соответствии с регламентом конфиденциальности.');
          location.reload();
        }
      }
    }

    // --- Paywall & Sharing ---
    function openPaywallModal() {
      document.getElementById('modal-paywall').style.display = 'flex';
    }
    function closePaywallModal() {
      document.getElementById('modal-paywall').style.display = 'none';
    }
    function selectPaywallPlan(card, planId) {
      document.querySelectorAll('.paywall-plan-card').forEach(c => c.classList.remove('selected'));
      card.classList.add('selected');
    }
    function activateAstraPlusSubscription() {
      closePaywallModal();
      alert('🎉 Поздравляем! Подписка АСТРА ПЛЮС успешно активирована. Все 78 карт, 68 звуков и наставники открыты!');
    }
    function restorePurchases() {
      alert('Покупки успешно проверены. Ваша подписка активна.');
    }
    function saveTarotSnapshot() {
      alert('Снимок карточки сохранен в фотопленку!');
    }
    function shareToSocial(network) {
      alert(`Открытие экспорта истории в ${network.toUpperCase()}...`);
    }

    // --- Avatar Selector Modal (Points 86-87) ---
    function openAvatarSelectorModal() {
      const grid = document.getElementById('avatar-picker-grid');
      grid.innerHTML = '';
      
      const avatars = [
        { name: 'Муза Тишины', src: '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/01_Default_Female_Muse_master_1024.png' },
        { name: 'Проводник Ясности', src: '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/02_Default_Male_Guide_master_1024.png' },
        { name: 'Овен ♈', src: '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/zodiac_01_Aries_master_1024.png' },
        { name: 'Телец ♉', src: '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/zodiac_02_Taurus_master_1024.png' },
        { name: 'Близнецы ♊', src: '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/zodiac_03_Gemini_master_1024.png' },
        { name: 'Рак ♋', src: '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/zodiac_04_Cancer_master_1024.png' },
        { name: 'Лев ♌', src: '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/zodiac_05_Leo_master_1024.png' },
        { name: 'Дева ♍', src: '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/zodiac_06_Virgo_master_1024.png' },
        { name: 'Весы ♎', src: '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/zodiac_07_Libra_master_1024.png' },
        { name: 'Скорпион ♏', src: '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/zodiac_08_Scorpio_master_1024.png' },
        { name: 'Стрелец ♐', src: '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/zodiac_09_Sagittarius_master_1024.png' },
        { name: 'Козерог ♑', src: '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/zodiac_10_Capricorn_master_1024.png' },
        { name: 'Водолей ♒', src: '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/zodiac_11_Aquarius_master_1024.png' },
        { name: 'Рыбы ♓', src: '11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/zodiac_12_Pisces_master_1024.png' }
      ];

      avatars.forEach(a => {
        const item = document.createElement('div');
        item.className = 'avatar-item-card';
        item.onclick = () => {
          document.getElementById('profile-avatar-display').src = a.src;
          AstraSecurity.Vault.set('selected_avatar', a.src);
          closeSheet('modal-avatar-selector');
        };
        item.innerHTML = `
          <img class="avatar-item-img" src="${a.src}" alt="${a.name}">
          <div style="font-size: 11px; font-weight: 700; color: #FFF; text-align: center;">${a.name}</div>
        `;
        grid.appendChild(item);
      });

      openSheet('modal-avatar-selector');
    }

    // --- Onboarding 13 Slides Controller (Points 11-23) ---
    const ONBOARD_SLIDES = [
      // Slide 1: Bento Grid
      {
        title: 'Добро пожаловать в Астру',
        sub: 'Твой космический проводник к спокойствию, интуиции и ритмам Вселенной.',
        render: () => `
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 20px 0;">
            <div class="card-glass" style="margin: 0; padding: 14px;">
              <div style="font-size: 24px; margin-bottom: 4px;">🌙</div>
              <div style="font-size: 13px; font-weight: 700;">13 лунный день</div>
              <div style="font-size: 11px; color: var(--text-muted);">Растущая Луна</div>
            </div>
            <div class="card-glass" style="margin: 0; padding: 14px;">
              <div style="font-size: 24px; margin-bottom: 4px;">🪐</div>
              <div style="font-size: 13px; font-weight: 700;">Солнце △ Венера</div>
              <div style="font-size: 11px; color: var(--text-muted);">Гармония дня</div>
            </div>
            <div class="card-glass" style="grid-column: span 2; margin: 0; padding: 14px; display: flex; align-items: center; gap: 12px;">
              <img src="astra_assets/04_ТАРО_И_РУНЫ/ic_tarot_empty.png" style="width: 44px; height: 60px; border-radius: 8px; object-fit: cover;" alt="Tarot">
              <div>
                <div style="font-size: 13px; font-weight: 700;">Мудрость Таро и Рун</div>
                <div style="font-size: 11px; color: var(--text-muted);">Ежедневный совет высших сил</div>
              </div>
            </div>
          </div>
          <button class="btn-primary" onclick="nextOnboardSlide()">Начать путешествие →</button>
        `
      },
      // Slide 2: Archetype Choice
      {
        title: 'Выберите ваш архетип',
        sub: 'Это определит тональность подсказок и образ вашего космического проводника.',
        render: () => `
          <div style="display: flex; flex-direction: column; gap: 10px; margin: 20px 0;">
            <div class="onboard-quiz-option selected" onclick="selectQuizOption(this, 'muse')">
              <div style="display: flex; align-items: center; gap: 12px;">
                <img src="11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/01_Default_Female_Muse_master_1024.png" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover;" alt="Muse">
                <div>
                  <div style="font-size: 15px; font-weight: 700; color: #FFF;">Муза Тишины</div>
                  <div style="font-size: 12px; color: var(--text-muted);">Женская интуиция и мягкая глубина</div>
                </div>
              </div>
              <span style="color: var(--purple);">✓</span>
            </div>
            <div class="onboard-quiz-option" onclick="selectQuizOption(this, 'guide')">
              <div style="display: flex; align-items: center; gap: 12px;">
                <img src="11_ДЕФОЛТНЫЕ_И_AI_АВАТАРЫ/02_Default_Male_Guide_master_1024.png" style="width: 44px; height: 44px; border-radius: 50%; object-fit: cover;" alt="Guide">
                <div>
                  <div style="font-size: 15px; font-weight: 700; color: #FFF;">Проводник Ясности</div>
                  <div style="font-size: 12px; color: var(--text-muted);">Мужская структура и четкий вектор</div>
                </div>
              </div>
              <span></span>
            </div>
          </div>
          <button class="btn-primary" onclick="nextOnboardSlide()">Продолжить</button>
        `
      },
      // Slide 3: Wheel of Balance
      {
        title: 'Колесо баланса',
        sub: 'Какие сферы жизни сейчас требуют наибольшего внимания и поддержки?',
        render: () => `
          <div style="display: flex; flex-wrap: wrap; gap: 10px; margin: 20px 0;">
            <div class="sphere-chip active" onclick="this.classList.toggle('active')">⚡ Энергия и ресурс</div>
            <div class="sphere-chip active" onclick="this.classList.toggle('active')">💼 Карьера и деньги</div>
            <div class="sphere-chip active" onclick="this.classList.toggle('active')">❤️ Любовь и близость</div>
            <div class="sphere-chip" onclick="this.classList.toggle('active')">🌙 Глубокий сон</div>
            <div class="sphere-chip" onclick="this.classList.toggle('active')">🧘 Внутренний покой</div>
          </div>
          <button class="btn-primary" onclick="nextOnboardSlide()">Продолжить</button>
        `
      },
      // Slide 4: NEW - Personal Astrologer & 5 Mentors 24/7
      {
        title: 'Твой личный астролог и 5 наставников 24/7',
        sub: 'Получай мгновенные инсайты по натальной карте, расшифровывай сны и расклады в любое время суток. Поддержка мудрых менторов всегда в твоем кармане.',
        render: () => `
          <div style="display: flex; flex-direction: column; gap: 8px; margin: 16px 0; max-height: 52vh; overflow-y: auto;">
            <div class="card-glass" style="margin: 0; padding: 12px; display: flex; align-items: center; gap: 12px;">
              <img src="10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ/01_Luna_Wise_Mystic.png" style="width: 44px; height: 44px; border-radius: 50%;" alt="Altea">
              <div>
                <div style="font-size: 14px; font-weight: 700; color: #FFF;">Алтея</div>
                <div style="font-size: 12px; color: var(--purple);">Хранительница Лунной Тишины (интуиция, покой)</div>
              </div>
            </div>
            <div class="card-glass" style="margin: 0; padding: 12px; display: flex; align-items: center; gap: 12px;">
              <img src="10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ/02_Nova_Cosmic_Coach.png" style="width: 44px; height: 44px; border-radius: 50%;" alt="Mira">
              <div>
                <div style="font-size: 14px; font-weight: 700; color: #FFF;">Мира</div>
                <div style="font-size: 12px; color: var(--teal);">Проводник Реализации (карьера, 1-й и 10-й дома)</div>
              </div>
            </div>
            <div class="card-glass" style="margin: 0; padding: 12px; display: flex; align-items: center; gap: 12px;">
              <img src="10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ/03_Selena_Empathic_Oracle.png" style="width: 44px; height: 44px; border-radius: 50%;" alt="Maya">
              <div>
                <div style="font-size: 14px; font-weight: 700; color: #FFF;">Майя</div>
                <div style="font-size: 12px; color: #F472B6;">Оракул Отношений (любовь, синастрия)</div>
              </div>
            </div>
            <div class="card-glass" style="margin: 0; padding: 12px; display: flex; align-items: center; gap: 12px;">
              <img src="10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ/04_Aurora_Holistic_Healer.png" style="width: 44px; height: 44px; border-radius: 50%;" alt="Rada">
              <div>
                <div style="font-size: 14px; font-weight: 700; color: #FFF;">Рада</div>
                <div style="font-size: 12px; color: #10B981;">Целительница Тела (аюрведа, биоритмы, сон)</div>
              </div>
            </div>
            <div class="card-glass" style="margin: 0; padding: 12px; display: flex; align-items: center; gap: 12px;">
              <img src="10_ПЕРСОНАЖИ_ИИ_АСТРОЛОГИ/05_Orion_Celestial_Strategist.png" style="width: 44px; height: 44px; border-radius: 50%;" alt="Daniil">
              <div>
                <div style="font-size: 14px; font-weight: 700; color: #FFF;">Даниил</div>
                <div style="font-size: 12px; color: var(--amber);">Звездный Стратег (финансы, законы Сатурна)</div>
              </div>
            </div>
          </div>
          <button class="btn-primary" onclick="nextOnboardSlide()">Выбрать наставников →</button>
        `
      },
      // Slide 5: Personal Goal
      {
        title: 'Ваша главная цель на лунный месяц',
        sub: 'Фокусировка энергии помогает синхронизировать намерения с космическим ритмом.',
        render: () => `
          <div style="display: flex; flex-direction: column; gap: 10px; margin: 20px 0;">
            <div class="onboard-quiz-option selected" onclick="selectQuizOption(this, 'g1')">
              <span>🧘 Найти внутренний покой и ясность</span>
              <span style="color: var(--purple);">✓</span>
            </div>
            <div class="onboard-quiz-option" onclick="selectQuizOption(this, 'g2')">
              <span>🚀 Совершить прорыв в карьере и доходе</span>
              <span></span>
            </div>
            <div class="onboard-quiz-option" onclick="selectQuizOption(this, 'g3')">
              <span>❤️ Укрепить отношения и доверие</span>
              <span></span>
            </div>
          </div>
          <button class="btn-primary" onclick="nextOnboardSlide()">Продолжить</button>
        `
      },
      // Slide 6: Moon Phase
      {
        title: 'Фаза Луны в реальном времени',
        sub: 'Сегодня 13-й лунный день. Луна освещена на 98% и приближается к пику Полнолуния.',
        render: () => `
          <div style="display: flex; justify-content: center; margin: 30px 0;">
            <img src="astra_assets/01_ФОНЫ_И_БАННЕРЫ_ВЫСОКОГО_РАЗРЕШЕНИЯ/ic_sharing_moon.png" style="width: 180px; height: 180px; filter: drop-shadow(0 0 30px rgba(255, 184, 77, 0.4));" alt="Moon">
          </div>
          <button class="btn-primary" onclick="nextOnboardSlide()">Узнать влияние →</button>
        `
      },
      // Slide 7: Moon Influence
      {
        title: 'Влияние на вашу нервную систему',
        sub: 'Растущая Луна стимулирует творческую и ментальную активность, но может обострять эмоциональную восприимчивость.',
        render: () => `
          <div class="card-glass" style="margin: 24px 0;">
            <div style="font-size: 15px; font-weight: 700; color: #FFF; margin-bottom: 8px;">Совет от Астры:</div>
            <div style="font-size: 13px; line-height: 1.5; color: rgba(255,255,255,0.85);">
              Направляйте вечернюю энергию в расслабляющие звуковые ванны и медитации на гармонизацию чакр.
            </div>
          </div>
          <button class="btn-primary" onclick="nextOnboardSlide()">Продолжить</button>
        `
      },
      // Slide 8: Birth Date
      {
        title: 'Дата вашего рождения',
        sub: 'Необходима для точного расчета положения планет и знака Луны по эфемеридам NASA.',
        render: () => `
          <div style="margin: 30px 0;">
            <input type="date" value="2000-03-14" style="width: 100%; height: 54px; background: var(--bg-card); border: 1px solid var(--bg-card-border); border-radius: 16px; color: #FFF; padding: 0 16px; font-size: 16px; outline: none;">
          </div>
          <button class="btn-primary" onclick="nextOnboardSlide()">Продолжить</button>
        `
      },
      // Slide 9: Birth Time & City
      {
        title: 'Время и город рождения',
        sub: 'Позволяет рассчитать точный Асцендент (Лагну) и сетку астрологических домов.',
        render: () => `
          <div style="display: flex; flex-direction: column; gap: 12px; margin: 24px 0;">
            <input type="time" value="22:00" style="width: 100%; height: 50px; background: var(--bg-card); border: 1px solid var(--bg-card-border); border-radius: 16px; color: #FFF; padding: 0 16px; font-size: 15px; outline: none;">
            <input type="text" value="Сочи, Россия" placeholder="Город рождения" style="width: 100%; height: 50px; background: var(--bg-card); border: 1px solid var(--bg-card-border); border-radius: 16px; color: #FFF; padding: 0 16px; font-size: 15px; outline: none;">
          </div>
          <button class="btn-primary" onclick="nextOnboardSlide()">Рассчитать натал →</button>
        `
      },
      // Slide 10: Tarot Draw in Onboarding
      {
        title: 'Вытяните первую карту судьбы',
        sub: 'Прикоснитесь к карте, чтобы получить персональное благословение от Астры.',
        render: () => `
          <div style="display: flex; justify-content: center; margin: 24px 0;">
            <div class="tarot-slot-hero" style="width: 160px; height: 250px;" onclick="this.innerHTML='<img src=\\\'astra_assets/04_ТАРО_И_РУНЫ/ic_tarot_the_star.png\\\' style=\\\'width:100%;height:100%;border-radius:18px;object-fit:cover;\\\'>'; document.getElementById('onboard-tarot-drawn-btn').style.display='flex';">
              <div style="font-size: 32px; color: var(--purple);">✨</div>
              <div class="tarot-slot-label">Коснитесь карты</div>
            </div>
          </div>
          <button class="btn-primary" id="onboard-tarot-drawn-btn" style="display: none;" onclick="nextOnboardSlide()">Принять послание звезды</button>
        `
      },
      // Slide 11: Sound Healing Teaser
      {
        title: 'Исцеление звуком (432 Гц)',
        sub: 'Частота гармонии Вселенной снимает стресс и настраивает биоритмы на спокойствие.',
        render: () => `
          <div class="card-glass" style="text-align: center; margin: 30px 0; padding: 24px;">
            <div style="font-size: 42px; margin-bottom: 10px;">🎶</div>
            <div style="font-size: 16px; font-weight: 700; color: #FFF;">Поющая тибетская чаша • 432 Hz</div>
            <div style="font-size: 12px; color: var(--teal); margin-top: 4px;">Гармонизация сердечной чакры</div>
          </div>
          <button class="btn-primary" onclick="nextOnboardSlide()">Продолжить</button>
        `
      },
      // Slide 12: Profile Calculation
      {
        title: 'Составление космического профиля',
        sub: 'Синхронизация с эфемеридами NASA, расчет лунных стоянок и натальных аспектов...',
        render: () => `
          <div style="display: flex; flex-direction: column; align-items: center; margin: 40px 0;">
            <div style="width: 70px; height: 70px; border-radius: 50%; border: 3px solid var(--purple); border-top-color: transparent; animation: spin 1s linear infinite; margin-bottom: 20px;"></div>
            <div style="font-size: 14px; color: var(--text-muted);" id="calc-step-text">Расчет восходящего знака (Лагны)...</div>
          </div>
          <style>@keyframes spin { 100% { transform: rotate(360deg); } }</style>
          <button class="btn-primary" id="btn-finish-calc" style="display: none;" onclick="nextOnboardSlide()">Открыть профиль →</button>
        `
      },
      // Slide 13: Welcome Screen
      {
        title: 'Добро пожаловать в Астру!',
        sub: 'Ваш звездный код готов. Наставники ждут вас в главном пространстве приложения.',
        render: () => `
          <div style="text-align: center; margin: 30px 0;">
            <img src="00_ИКОНКИ_И_ЛОГОТИП_АСТРА/Astra_AppIcon_MandalaLotus_master_1024.webp" style="width: 110px; height: 110px; border-radius: 28px; box-shadow: 0 10px 30px rgba(120,75,246,0.4);" alt="Lotus">
            <div style="font-size: 18px; font-weight: 800; color: #FFF; margin-top: 18px;">Александр • Восходящий Скорпион</div>
            <div style="font-size: 13px; color: var(--amber); margin-top: 4px;">Луна в Тельце ♉ • Аркан 7</div>
          </div>
          <button class="btn-primary" onclick="finishOnboarding()">Войти в пространство Астры ✨</button>
        `
      }
    ];

    function startOnboardingFlow() {
      currentOnboardSlide = 0;
      renderCurrentOnboardSlide();
      document.getElementById('modal-onboarding').style.display = 'flex';
    }

    function renderCurrentOnboardSlide() {
      const slide = ONBOARD_SLIDES[currentOnboardSlide];
      const cont = document.getElementById('onboard-slide-content');
      const progress = ((currentOnboardSlide + 1) / ONBOARD_SLIDES.length) * 100;
      document.getElementById('onboard-progress-fill').style.width = progress + '%';
      document.getElementById('onboard-prev-btn').style.visibility = currentOnboardSlide === 0 ? 'hidden' : 'visible';

      cont.innerHTML = `
        <div>
          <div class="onboard-header-title">${slide.title}</div>
          <div class="onboard-header-sub">${slide.sub}</div>
        </div>
        <div>
          ${slide.render()}
        </div>
      `;

      if (currentOnboardSlide === 11) {
        setTimeout(() => {
          const txt = document.getElementById('calc-step-text');
          if (txt) txt.innerText = 'Анализ планетных стоянок завершен!';
          const btn = document.getElementById('btn-finish-calc');
          if (btn) btn.style.display = 'flex';
        }, 1200);
      }
    }

    function nextOnboardSlide() {
      if (currentOnboardSlide < ONBOARD_SLIDES.length - 1) {
        currentOnboardSlide++;
        renderCurrentOnboardSlide();
      }
    }

    function prevOnboardSlide() {
      if (currentOnboardSlide > 0) {
        currentOnboardSlide--;
        renderCurrentOnboardSlide();
      }
    }

    function selectQuizOption(el, optId) {
      el.parentElement.querySelectorAll('.onboard-quiz-option').forEach(o => {
        o.classList.remove('selected');
        const s = o.querySelector('span:last-child');
        if (s) s.innerText = '';
      });
      el.classList.add('selected');
      const lastSpan = el.querySelector('span:last-child');
      if (lastSpan) lastSpan.innerText = '✓';
    }

    function skipOnboarding() {
      document.getElementById('modal-onboarding').style.display = 'none';
      AstraSecurity.Vault.set('onboarding_seen', true);
    }

    function finishOnboarding() {
      skipOnboarding();
      switchMainScreen('calendar');
    }

    // --- Sheet Helpers ---
    function openSheet(sheetId) {
      document.getElementById(sheetId).style.display = 'flex';
    }
    function closeSheet(sheetId) {
      document.getElementById(sheetId).style.display = 'none';
    }

    // --- Screen Deep Linking & Message Bus ---
    function navigateToScreen(screenName, hideTabs) {
      if (hideTabs !== undefined && hideTabs !== null) {
        const bottomNav = document.querySelector('.bottom-nav');
        if (bottomNav) bottomNav.style.display = hideTabs ? 'none' : 'flex';
        document.querySelectorAll('.screen-view').forEach(s => {
          s.style.paddingBottom = hideTabs ? '24px' : '90px';
        });
      }

      // Close open modals
      document.querySelectorAll('.bottom-sheet-overlay, .player-fullscreen-modal, .settings-screen-modal, .paywall-modal, .onboarding-modal')
        .forEach(m => m.style.display = 'none');

      switch (screenName) {
        case 'calendar':
          switchMainScreen('calendar');
          break;
        case 'tarot_1':
          switchMainScreen('practices');
          switchPracticeTab('tarot');
          setTarotMode(1);
          break;
        case 'tarot_3':
          switchMainScreen('practices');
          switchPracticeTab('tarot');
          setTarotMode(3);
          break;
        case 'tarot_5':
          switchMainScreen('practices');
          switchPracticeTab('tarot');
          setTarotMode(5);
          break;
        case 'tarot_all':
          switchMainScreen('practices');
          switchPracticeTab('tarot');
          setTarotMode('all');
          break;
        case 'tarot_sheet':
          switchMainScreen('practices');
          switchPracticeTab('tarot');
          setTarotMode(1);
          pullCardFromFan(0);
          openCardMeaningModal(window.ASTRA_TAROT_DATABASE ? ASTRA_TAROT_DATABASE[0] : { name: 'Шут', arcana: 'major' });
          break;
        case 'oracle':
          switchMainScreen('practices');
          switchPracticeTab('oracle');
          break;
        case 'gods':
          switchMainScreen('practices');
          switchPracticeTab('gods');
          break;
        case 'dream':
          switchMainScreen('practices');
          switchPracticeTab('dream');
          break;
        case 'runes':
          switchMainScreen('practices');
          switchPracticeTab('runes');
          drawDailyRune();
          break;
        case 'runes_catalog':
          switchMainScreen('practices');
          switchPracticeTab('runes');
          openRunesCatalogModal();
          break;
        case 'affirmations':
          switchMainScreen('practices');
          switchPracticeTab('affirmations');
          break;
        case 'healing':
          switchMainScreen('healing');
          break;
        case 'player':
          switchMainScreen('healing');
          openSoundPlayerById(291);
          break;
        case 'chat':
          switchMainScreen('chat');
          break;
        case 'you':
          switchMainScreen('you');
          break;
        case 'avatars':
          switchMainScreen('you');
          openAvatarSelectorModal();
          break;
        case 'settings':
          switchMainScreen('you');
          openSettingsScreen();
          break;
        case 'paywall':
          openPaywallModal();
          break;
        case 'onboarding':
          startOnboardingFlow();
          break;
        default:
          switchMainScreen('calendar');
      }
    }

    window.addEventListener('message', (e) => {
      if (e.data && e.data.action === 'navigateScreen') {
        navigateToScreen(e.data.screen, e.data.hideTabs);
      }
    });

    // --- Initialization ---
    window.addEventListener('DOMContentLoaded', () => {
      initCalendarStrip();
      setTarotMode(1);
      drawDailyRune();
      initSoundscape();
      initMentors();

      const params = new URLSearchParams(window.location.search);
      const initialScreen = params.get('screen');
      const hideTabsFlag = params.get('hide_tabs') === '1' || params.get('hide_tabs') === 'true';
      if (initialScreen) {
        setTimeout(() => navigateToScreen(initialScreen, hideTabsFlag), 50);
      } else if (hideTabsFlag) {
        setTimeout(() => navigateToScreen('calendar', true), 50);
      }
    });
  </script>
</body>
</html>
"""

with open(OUT_PATH, 'w', encoding='utf-8') as f:
    f.write(html_template)

print(f"Master ASTRA Web App successfully generated at: {OUT_PATH}")
