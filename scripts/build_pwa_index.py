import json

with open("data/questions.json", "r", encoding="utf-8") as f:
    questions_when = json.load(f)

with open("data/questions_why.json", "r", encoding="utf-8") as f:
    questions_why = json.load(f)

json_when_str = json.dumps(questions_when, ensure_ascii=False)
json_why_str = json.dumps(questions_why, ensure_ascii=False)

html_code = f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
  <meta name="theme-color" content="#2563eb">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="default">
  <meta name="apple-mobile-web-app-title" content="特教問答">
  <link rel="manifest" href="manifest.json">
  <link rel="icon" type="image/svg+xml" href="icon.svg">
  <link rel="apple-touch-icon" href="icon.svg">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; media-src 'self' data: blob:; img-src 'self' data:; connect-src 'self' data: blob:;">
  <meta name="referrer" content="no-referrer">
  <title>特教生活與因果認知問答（全200題雙單元）</title>
  <style>
    :root {{
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --border: #cbd5e1;
      --active-card: #eff6ff;
      --success: #10b981;
      --unit-why: #d97706;
      --unit-why-hover: #b45309;
      --unit-all: #7c3aed;
      --unit-all-hover: #6d28d9;
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-tap-highlight-color: transparent;
    }}

    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", "Microsoft JhengHei", sans-serif;
      background: var(--bg);
      color: var(--text-main);
      padding: 16px;
      padding-bottom: 140px;
    }}

    header {{
      max-width: 900px;
      margin: 0 auto 12px;
      text-align: center;
    }}

    h1 {{
      font-size: 1.5rem;
      color: #1e3a8a;
      margin-bottom: 4px;
      transition: color 0.2s ease;
    }}

    .subtitle {{
      font-size: 0.88rem;
      color: var(--text-muted);
      line-height: 1.4;
    }}

    /* 單元大切換 Switcher (三 Tab 切換) */
    .unit-switch-container {{
      max-width: 900px;
      margin: 0 auto 14px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 8px;
      background: #e2e8f0;
      padding: 6px;
      border-radius: 14px;
    }}

    .unit-btn {{
      border: none;
      border-radius: 10px;
      padding: 12px 14px;
      font-size: 0.98rem;
      font-weight: 700;
      cursor: pointer;
      background: transparent;
      color: #475569;
      transition: all 0.2s ease;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;
      text-align: center;
    }}

    .unit-btn .unit-desc {{
      font-size: 0.76rem;
      font-weight: normal;
      opacity: 0.88;
    }}

    .unit-btn.active.unit-when {{
      background: #2563eb;
      color: white;
      box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
    }}

    .unit-btn.active.unit-why {{
      background: #d97706;
      color: white;
      box-shadow: 0 4px 12px rgba(217, 119, 6, 0.25);
    }}

    .unit-btn.active.unit-all {{
      background: #7c3aed;
      color: white;
      box-shadow: 0 4px 12px rgba(124, 58, 237, 0.25);
    }}

    /* 離線快取狀態欄 */
    .cache-banner {{
      max-width: 900px;
      margin: 0 auto 14px;
      background: #f1f5f9;
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 10px 14px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
      font-size: 0.86rem;
    }}

    .cache-status {{
      display: flex;
      align-items: center;
      gap: 6px;
      color: #334155;
      font-weight: 500;
    }}

    .cache-actions {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
    }}

    .btn-xs {{
      padding: 5px 10px;
      font-size: 0.8rem;
      border-radius: 6px;
      border: 1px solid var(--border);
      background: white;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.15s ease;
    }}
    .btn-xs:hover {{
      background: #e2e8f0;
    }}

    .cache-progress-bar {{
      width: 100%;
      height: 4px;
      background: #e2e8f0;
      border-radius: 999px;
      overflow: hidden;
      margin-top: 6px;
      display: none;
    }}

    .cache-progress-fill {{
      height: 100%;
      width: 0%;
      background: var(--success);
      transition: width 0.2s ease;
    }}

    /* 頂部播放器 Dock */
    .player-dock {{
      position: sticky;
      top: 10px;
      z-index: 100;
      max-width: 900px;
      margin: 0 auto 16px;
      background: rgba(255, 255, 255, 0.98);
      backdrop-filter: blur(10px);
      border: 2px solid #93c5fd;
      border-radius: 16px;
      padding: 16px;
      box-shadow: 0 8px 24px rgba(37, 99, 235, 0.12);
      transition: all 0.2s ease;
    }}

    .player-dock.dock-why {{
      border-color: #fcd34d;
      box-shadow: 0 8px 24px rgba(217, 119, 6, 0.12);
    }}

    .player-dock.dock-all {{
      border-color: #c4b5fd;
      box-shadow: 0 8px 24px rgba(124, 58, 237, 0.12);
    }}

    .now-playing {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      font-weight: 700;
      color: #1e40af;
      font-size: 1.15rem;
    }}

    .dock-why .now-playing {{
      color: #b45309;
    }}

    .dock-all .now-playing {{
      color: #6d28d9;
    }}

    .controls-row {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;
      gap: 12px;
      margin-bottom: 10px;
    }}

    .btn {{
      border: none;
      border-radius: 9999px;
      padding: 10px 20px;
      font-size: 1rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      user-select: none;
    }}

    .btn-primary {{
      background: var(--primary);
      color: white;
      box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
    }}
    .btn-primary:hover {{
      background: var(--primary-hover);
    }}

    .dock-why .btn-primary {{
      background: var(--unit-why);
      box-shadow: 0 2px 8px rgba(217, 119, 6, 0.3);
    }}
    .dock-why .btn-primary:hover {{
      background: var(--unit-why-hover);
    }}

    .dock-all .btn-primary {{
      background: var(--unit-all);
      box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3);
    }}
    .dock-all .btn-primary:hover {{
      background: var(--unit-all-hover);
    }}

    .btn-outline {{
      background: white;
      border: 1.5px solid var(--border);
      color: var(--text-main);
    }}
    .btn-outline:hover {{
      background: #f1f5f9;
    }}

    .progress-bar-container {{
      width: 100%;
      height: 6px;
      background: #e2e8f0;
      border-radius: 999px;
      overflow: hidden;
      margin-bottom: 12px;
      cursor: pointer;
    }}

    .progress-bar-fill {{
      height: 100%;
      width: 0%;
      background: var(--primary);
      transition: width 0.1s linear;
    }}

    .dock-why .progress-bar-fill {{
      background: var(--unit-why);
    }}

    .dock-all .progress-bar-fill {{
      background: var(--unit-all);
    }}

    .toggle-group {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;
      gap: 16px;
      font-size: 0.88rem;
      color: var(--text-muted);
    }}

    .toggle-label {{
      display: flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      font-weight: 500;
    }}

    /* 大合輯專用快捷播放區 */
    .album-shortcuts {{
      max-width: 900px;
      margin: 0 auto 16px;
      background: #eff6ff;
      border: 1px dashed #60a5fa;
      border-radius: 12px;
      padding: 12px 14px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 8px;
    }}

    .album-shortcuts.shortcuts-why {{
      background: #fffbeb;
      border-color: #f59e0b;
    }}

    .album-shortcuts.shortcuts-all {{
      background: #f5f3ff;
      border-color: #a78bfa;
    }}

    .album-title {{
      font-size: 0.88rem;
      font-weight: 700;
      color: #1e40af;
      margin-right: 4px;
    }}

    .shortcuts-why .album-title {{
      color: #b45309;
    }}

    .shortcuts-all .album-title {{
      color: #6d28d9;
    }}

    .btn-sm {{
      padding: 6px 12px;
      font-size: 0.85rem;
      border-radius: 8px;
    }}

    /* 分類標籤頁 */
    .category-tabs {{
      max-width: 900px;
      margin: 0 auto 16px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }}

    .tab-btn {{
      padding: 8px 14px;
      border-radius: 10px;
      background: white;
      border: 1.5px solid var(--border);
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      color: var(--text-muted);
      transition: all 0.15s ease;
    }}
    .tab-btn.active {{
      background: #2563eb;
      color: white;
      border-color: #2563eb;
    }}

    .tabs-why .tab-btn.active {{
      background: #d97706;
      border-color: #d97706;
    }}

    .tabs-all .tab-btn.active {{
      background: #7c3aed;
      border-color: #7c3aed;
    }}

    /* 題目網格列表 */
    .question-list {{
      max-width: 900px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 14px;
    }}

    .q-card {{
      background: var(--card-bg);
      border: 1.5px solid var(--border);
      border-radius: 14px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      cursor: pointer;
      transition: all 0.15s ease;
      min-height: 120px;
    }}

    .q-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
      border-color: #60a5fa;
    }}

    .q-card.playing {{
      background: var(--active-card);
      border-color: #2563eb;
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.3);
    }}

    .list-why .q-card.playing {{
      background: #fffbeb;
      border-color: #d97706;
      box-shadow: 0 0 0 3px rgba(217, 119, 6, 0.3);
    }}

    .list-all .q-card.playing {{
      background: #f5f3ff;
      border-color: #7c3aed;
      box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.3);
    }}

    .q-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }}

    .badge {{
      font-size: 0.8rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      background: #e2e8f0;
      color: #334155;
    }}

    .badge-playing {{
      background: #2563eb;
      color: white;
    }}

    .list-why .badge-playing {{
      background: #d97706;
      color: white;
    }}

    .list-all .badge-playing {{
      background: #7c3aed;
      color: white;
    }}

    .q-title {{
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 10px;
      line-height: 1.4;
    }}

    .q-answer {{
      font-size: 1.05rem;
      color: #047857;
      font-weight: 700;
      background: #d1fae5;
      padding: 6px 10px;
      border-radius: 8px;
      align-self: flex-start;
    }}

    .hidden-answer {{
      filter: blur(8px);
      user-select: none;
      transition: filter 0.2s ease;
      background: #f1f5f9;
      color: #94a3b8;
    }}
    .hidden-answer:hover, .hidden-answer:active {{
      filter: blur(0);
      background: #d1fae5;
      color: #047857;
    }}
  </style>
</head>
<body>

  <header>
    <h1 id="mainTitle">特教生活與因果認知教材（全200題）</h1>
    <p class="subtitle" id="mainSubtitle">臺灣國語自然女聲（語速 90% | 問後停頓 3 秒 | 題間間隔 3 秒）</p>
  </header>

  <!-- 單元大切換 Switcher (三 Tab 切換) -->
  <div class="unit-switch-container">
    <button class="unit-btn active unit-when" id="btnSwitchWhen" onclick="switchUnit('when')">
      <span>📘 單元一：生活問答</span>
      <span class="unit-desc">100題（什麼時候）| 停頓3秒</span>
    </button>
    <button class="unit-btn unit-why" id="btnSwitchWhy" onclick="switchUnit('why')">
      <span>📙 單元二：因果認知</span>
      <span class="unit-desc">100題（為什麼）| 停頓5秒</span>
    </button>
    <button class="unit-btn unit-all" id="btnSwitchAll" onclick="switchUnit('all')">
      <span>🎲 全部雙單元綜合</span>
      <span class="unit-desc">全200題 | 跨單元隨機大混播</span>
    </button>
  </div>

  <!-- 離線快取管理欄 -->
  <div class="cache-banner">
    <div class="cache-status" id="cacheStatusText">
      <span>💾 離線模式：</span>
      <span id="cacheLabel" style="color: #2563eb;">點擊右側按鈕可預載音檔，沒網路也能播放</span>
    </div>
    <div class="cache-actions">
      <button class="btn-xs" id="btnDownloadCurrent" style="background: #2563eb; color: white; border-color: #2563eb;">📥 下載當前單元</button>
      <button class="btn-xs" id="btnDownloadAll" style="background: #7c3aed; color: white; border-color: #7c3aed;">📥 下載全部 200 題 (30MB)</button>
      <button class="btn-xs" id="btnClearCache">🔄 清理快取</button>
    </div>
    <div class="cache-progress-bar" id="cacheProgressBar">
      <div class="cache-progress-fill" id="cacheProgressFill"></div>
    </div>
  </div>

  <!-- 頂部播放器 Dock -->
  <div class="player-dock" id="playerDock">
    <div class="now-playing">
      <span id="playingTitle">點選下方任一題目即可發音</span>
      <span id="playingTime" style="font-size: 0.88rem; font-weight: normal; color: var(--text-muted);">00:00 / 00:00</span>
    </div>

    <!-- 進度條 -->
    <div class="progress-bar-container" id="progressContainer">
      <div class="progress-bar-fill" id="progressFill"></div>
    </div>

    <div class="controls-row">
      <button class="btn btn-outline" id="prevBtn">⏮ 上一題</button>
      <button class="btn btn-primary" id="playBtn">▶ 播放</button>
      <button class="btn btn-outline" id="nextBtn">下一題 ⏭</button>
      <button class="btn btn-outline" id="randomBtn" style="border-color: #8b5cf6; color: #6d28d9; background: #f5f3ff;">🎲 隨機抽一題</button>
    </div>

    <div class="toggle-group">
      <label class="toggle-label">
        <input type="checkbox" id="autoPlayNext" checked> <span id="autoPlayLabel">自動連續播放（題間隔3秒）</span>
      </label>
      <label class="toggle-label">
        <input type="checkbox" id="shuffleMode"> 隨機播放模式
      </label>
      <label class="toggle-label">
        <input type="checkbox" id="loopSingle"> 單題循環重複聽
      </label>
      <label class="toggle-label">
        <input type="checkbox" id="hideAnswer"> 隱藏答案（測驗模式）
      </label>
    </div>
  </div>

  <!-- 合輯快捷播放 -->
  <div class="album-shortcuts" id="albumContainer">
    <!-- 動態注入合輯按鈕 -->
  </div>

  <!-- 分類篩選 Tab -->
  <div class="category-tabs" id="tabs">
    <!-- 動態注入分類標籤 -->
  </div>

  <!-- 題目列表 -->
  <div class="question-list" id="qList"></div>

  <audio id="audioElement" preload="auto"></audio>

  <script>
    // 註冊 PWA Service Worker 並自動偵測更新（免手動清除快取）
    if ('serviceWorker' in navigator) {{
      navigator.serviceWorker.register('./sw.js').then(reg => {{
        console.log('Service Worker 註冊成功:', reg.scope);
        reg.update();
        
        reg.onupdatefound = () => {{
          const installingWorker = reg.installing;
          installingWorker.onstatechange = () => {{
            if (installingWorker.state === 'installed' && navigator.serviceWorker.controller) {{
              console.log('偵測到新版本，自動刷新升級！');
              window.location.reload();
            }}
          }};
        }};
      }}).catch(err => console.log('Service Worker 註冊略過:', err));

      let refreshing = false;
      navigator.serviceWorker.addEventListener('controllerchange', () => {{
        if (!refreshing) {{
          refreshing = true;
          window.location.reload();
        }}
      }});
    }}

    const rawWhen = {json_when_str};
    const rawWhy = {json_why_str};

    const dataWhen = rawWhen.map(item => ({{ ...item, unit: 'when', unitName: '生活' }}));
    const dataWhy = rawWhy.map(item => ({{ ...item, unit: 'why', unitName: '因果' }}));
    const dataAll = [...dataWhen, ...dataWhy];

    const config = {{
      when: {{
        title: "生活問答特教教材（100題）",
        subtitle: "臺灣國語自然女聲（語速 90% | 問後停頓 3 秒 | 題間間隔 3 秒）",
        autoDelay: 3000,
        autoLabel: "自動連續播放（題間隔3秒）",
        audioDir: "./output/singles/",
        fullAlbum: "./output/full_100_compilation.mp3",
        fullAlbumName: "生活問答100題完整大合輯 (19分鐘)",
        categories: [
          {{ key: "第一類：身體需求與生理反應", label: "1. 生理需求 (1-20)", album: "./output/categories/01_第一類_身體需求與生理反應(1-20題).mp3", albumName: "第一類：身體需求" }},
          {{ key: "第二類：生活作息", label: "2. 生活作息 (21-40)", album: "./output/categories/02_第二類_生活作息(21-40題).mp3", albumName: "第二類：生活作息" }},
          {{ key: "第三類：穿著與天氣", label: "3. 穿著天氣 (41-55)", album: "./output/categories/03_第三類_穿著與天氣(41-55題).mp3", albumName: "第三類：穿著天氣" }},
          {{ key: "第四類：學校與學習", label: "4. 學校學習 (56-70)", album: "./output/categories/04_第四類_學校與學習(56-70題).mp3", albumName: "第四類：學校學習" }},
          {{ key: "第五類：外出與安全", label: "5. 外出安全 (71-85)", album: "./output/categories/05_第五類_外出與安全(71-85題).mp3", albumName: "第五類：外出安全" }},
          {{ key: "第六類：季節、節日與事件", label: "6. 季節事件 (86-100)", album: "./output/categories/06_第六類_季節節日與事件(86-100題).mp3", albumName: "第六類：季節事件" }}
        ]
      }},
      why: {{
        title: "因果認知特教教材（100題）",
        subtitle: "臺灣國語自然女聲（語速 90% | 問後停頓 5 秒 | 題間間隔 2 秒）",
        autoDelay: 2000,
        autoLabel: "自動連續播放（題間隔2秒）",
        audioDir: "./output/singles_why/",
        fullAlbum: "./output/why_100_compilation.mp3",
        fullAlbumName: "為什麼因果認知100題完整大合輯 (21分鐘)",
        categories: [
          {{ key: "第一類：身體需求與日常生活", label: "1. 身體日常 (1-20)", album: "./output/categories_why/01_第一類_身體需求與日常生活(1-20題).mp3", albumName: "第一類：身體日常" }},
          {{ key: "第二類：天氣、穿著與環境", label: "2. 天氣環境 (21-40)", album: "./output/categories_why/02_第二類_天氣穿著與環境(21-40題).mp3", albumName: "第二類：天氣環境" }},
          {{ key: "第三類：學校與外出安全", label: "3. 學校安全 (41-60)", album: "./output/categories_why/03_第三類_學校與外出安全(41-60題).mp3", albumName: "第三類：學校安全" }},
          {{ key: "第四類：情緒與人際互動", label: "4. 情緒人際 (61-80)", album: "./output/categories_why/04_第四類_情緒與人際互動(61-80題).mp3", albumName: "第四類：情緒人際" }},
          {{ key: "第五類：生活情境與因果推理", label: "5. 生活因果 (81-100)", album: "./output/categories_why/05_第五類_生活情境與因果推理(81-100題).mp3", albumName: "第五類：生活因果" }}
        ]
      }},
      all: {{
        title: "特教雙單元綜合（全 200 題大混播）",
        subtitle: "臺灣國語自然女聲（生活問答 100 題 + 因果認知 100 題 | 跨單元隨機大抽題）",
        autoDelay: 2500,
        autoLabel: "自動連續播放（題間隔2.5秒）",
        fullAlbum: "./output/full_100_compilation.mp3",
        fullAlbumName: "生活問答完整大合輯",
        categories: [
          {{ key: "all", label: "🎲 全部 200 題混播" }},
          {{ key: "when", label: "📘 生活問答 (100題)" }},
          {{ key: "why", label: "📙 因果認知 (100題)" }}
        ]
      }}
    }};

    let currentUnit = "when";
    let questionsData = dataWhen;
    let currentIndex = 0;
    let isPlaying = false;
    let isAlbumMode = false;
    let currentFilter = "all";

    const CACHE_NAME = 'autism-tts-v2.1.0';

    const audio = document.getElementById("audioElement");
    const playBtn = document.getElementById("playBtn");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const playingTitle = document.getElementById("playingTitle");
    const playingTime = document.getElementById("playingTime");
    const progressFill = document.getElementById("progressFill");
    const progressContainer = document.getElementById("progressContainer");
    const autoPlayNext = document.getElementById("autoPlayNext");
    const autoPlayLabel = document.getElementById("autoPlayLabel");
    const shuffleMode = document.getElementById("shuffleMode");
    const loopSingle = document.getElementById("loopSingle");
    const hideAnswer = document.getElementById("hideAnswer");
    const randomBtn = document.getElementById("randomBtn");
    const qList = document.getElementById("qList");
    const albumContainer = document.getElementById("albumContainer");
    const tabsContainer = document.getElementById("tabs");
    const playerDock = document.getElementById("playerDock");

    const cacheLabel = document.getElementById("cacheLabel");
    const btnDownloadCurrent = document.getElementById("btnDownloadCurrent");
    const btnDownloadAll = document.getElementById("btnDownloadAll");
    const btnClearCache = document.getElementById("btnClearCache");
    const cacheProgressBar = document.getElementById("cacheProgressBar");
    const cacheProgressFill = document.getElementById("cacheProgressFill");

    function escapeHtml(str) {{
      if (!str) return "";
      return String(str)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/\\x27/g, "&#039;");
    }}

    function formatTime(seconds) {{
      if (isNaN(seconds) || seconds < 0) return "00:00";
      const m = Math.floor(seconds / 60);
      const s = Math.floor(seconds % 60);
      return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
    }}

    function getAudioPath(item) {{
      const cleanQ = item.question.replace("？", "").replace("?", "").replace("/", "_").trim();
      const idStr = String(item.id).padStart(3, "0");
      const dir = item.unit === "why" ? config.why.audioDir : config.when.audioDir;
      return encodeURI(`${{dir}}第${{idStr}}題_${{cleanQ}}.mp3`);
    }}

    function switchUnit(unitKey) {{
      currentUnit = unitKey;
      if (unitKey === "when") {{
        questionsData = dataWhen;
      }} else if (unitKey === "why") {{
        questionsData = dataWhy;
      }} else {{
        questionsData = dataAll;
        shuffleMode.checked = true; // 切換到全 200 題綜合時預設開啟隨機播放！
      }}

      currentIndex = 0;
      isAlbumMode = false;
      currentFilter = "all";
      audio.pause();
      isPlaying = false;
      playBtn.innerText = "▶ 播放";
      progressFill.style.width = "0%";
      playingTime.innerText = "00:00 / 00:00";
      playingTitle.innerText = "點選下方任一題目即可發音";

      // 更新按鈕外觀
      const btnWhen = document.getElementById("btnSwitchWhen");
      const btnWhy = document.getElementById("btnSwitchWhy");
      const btnAll = document.getElementById("btnSwitchAll");

      btnWhen.classList.remove("active");
      btnWhy.classList.remove("active");
      btnAll.classList.remove("active");

      playerDock.classList.remove("dock-why", "dock-all");
      albumContainer.classList.remove("shortcuts-why", "shortcuts-all");
      tabsContainer.classList.remove("tabs-why", "tabs-all");
      qList.classList.remove("list-why", "list-all");

      if (unitKey === "when") {{
        btnWhen.classList.add("active");
        btnDownloadCurrent.style.background = "#2563eb";
        btnDownloadCurrent.style.borderColor = "#2563eb";
        btnDownloadCurrent.innerText = "📥 下載生活問答 (15MB)";
      }} else if (unitKey === "why") {{
        btnWhy.classList.add("active");
        playerDock.classList.add("dock-why");
        albumContainer.classList.add("shortcuts-why");
        tabsContainer.classList.add("tabs-why");
        qList.classList.add("list-why");
        btnDownloadCurrent.style.background = "#d97706";
        btnDownloadCurrent.style.borderColor = "#d97706";
        btnDownloadCurrent.innerText = "📥 下載因果認知 (15MB)";
      }} else {{
        btnAll.classList.add("active");
        playerDock.classList.add("dock-all");
        albumContainer.classList.add("shortcuts-all");
        tabsContainer.classList.add("tabs-all");
        qList.classList.add("list-all");
        btnDownloadCurrent.style.background = "#7c3aed";
        btnDownloadCurrent.style.borderColor = "#7c3aed";
        btnDownloadCurrent.innerText = "📥 下載全200題 (30MB)";
      }}

      // 更新文案
      document.getElementById("mainTitle").innerText = config[unitKey].title;
      document.getElementById("mainSubtitle").innerText = config[unitKey].subtitle;
      autoPlayLabel.innerText = config[unitKey].autoLabel;

      renderShortcutsAndTabs();
      renderList();
      checkExistingCache();
    }}

    function renderShortcutsAndTabs() {{
      const unitCfg = config[currentUnit];
      
      // 合輯快捷鍵
      if (currentUnit === "all") {{
        albumContainer.innerHTML = `
          <span class="album-title">🚌 復康巴士一鍵合輯：</span>
          <button class="btn btn-outline btn-sm" id="btnAlbumFullWhen">▶ 生活問答大合輯 (19分)</button>
          <button class="btn btn-outline btn-sm" id="btnAlbumFullWhy">▶ 因果認知大合輯 (21分)</button>
        `;
        document.getElementById("btnAlbumFullWhen").onclick = () => playAlbum(config.when.fullAlbum, config.when.fullAlbumName);
        document.getElementById("btnAlbumFullWhy").onclick = () => playAlbum(config.why.fullAlbum, config.why.fullAlbumName);
      }} else {{
        albumContainer.innerHTML = `
          <span class="album-title">🚌 復康巴士一鍵合輯：</span>
          <button class="btn btn-outline btn-sm" id="btnAlbumFull">▶ 100題完整大合輯</button>
        `;
        unitCfg.categories.forEach((cat, idx) => {{
          const b = document.createElement("button");
          b.className = "btn btn-outline btn-sm";
          b.innerText = `${{idx + 1}}. ${{cat.albumName.split("：")[1] || cat.albumName}}`;
          b.onclick = () => playAlbum(cat.album, cat.albumName);
          albumContainer.appendChild(b);
        }});
        document.getElementById("btnAlbumFull").onclick = () => playAlbum(unitCfg.fullAlbum, unitCfg.fullAlbumName);
      }}

      // 分類標籤
      tabsContainer.innerHTML = "";
      if (currentUnit === "all") {{
        unitCfg.categories.forEach((cat, idx) => {{
          const tb = document.createElement("button");
          tb.className = `tab-btn ${{idx === 0 ? "active" : ""}}`;
          tb.setAttribute("data-cat", cat.key);
          tb.innerText = cat.label;
          tabsContainer.appendChild(tb);
        }});
      }} else {{
        tabsContainer.innerHTML = `<button class="tab-btn active" data-cat="all">全部 100 題</button>`;
        unitCfg.categories.forEach(cat => {{
          const tb = document.createElement("button");
          tb.className = "tab-btn";
          tb.setAttribute("data-cat", cat.key);
          tb.innerText = cat.label;
          tabsContainer.appendChild(tb);
        }});
      }}
    }}

    function renderList() {{
      qList.innerHTML = "";
      const isHidden = hideAnswer.checked;

      questionsData.forEach((item, index) => {{
        if (currentUnit === "all") {{
          if (currentFilter === "when" && item.unit !== "when") return;
          if (currentFilter === "why" && item.unit !== "why") return;
        }} else {{
          if (currentFilter !== "all" && item.category !== currentFilter) return;
        }}

        const card = document.createElement("div");
        card.className = `q-card ${{!isAlbumMode && index === currentIndex && isPlaying ? "playing" : ""}}`;
        card.id = `card-${{index}}`;
        card.onclick = () => playQuestion(index);

        const badgeText = currentUnit === "all" ? `【${{item.unitName}}】第 ${{item.id}} 題` : `第 ${{item.id}} 題`;

        card.innerHTML = `
          <div>
            <div class="q-header">
              <span class="badge ${{!isAlbumMode && index === currentIndex && isPlaying ? "badge-playing" : ""}}">${{badgeText}}</span>
              <span style="font-size: 0.75rem; color: #64748b; font-weight: 500;">${{item.category.split("：")[1] || item.category}}</span>
            </div>
            <div class="q-title">${{escapeHtml(item.question)}}</div>
          </div>
          <div class="q-answer ${{isHidden ? 'hidden-answer' : ''}}">${{escapeHtml(item.answer)}}</div>
        `;
        qList.appendChild(card);
      }});
    }}

    function playQuestion(index) {{
      if (index < 0 || index >= questionsData.length) return;
      isAlbumMode = false;
      currentIndex = index;
      const item = questionsData[index];
      const audioSrc = getAudioPath(item);

      audio.src = audioSrc;
      audio.load();
      
      const playPromise = audio.play();
      if (playPromise !== undefined) {{
        playPromise.then(() => {{
          isPlaying = true;
          updateUI();
        }}).catch(err => console.error("播放錯誤:", err));
      }}
      updateUI();
    }}

    function playAlbum(albumPath, albumName) {{
      isAlbumMode = true;
      audio.src = encodeURI(albumPath);
      audio.load();
      playingTitle.innerText = `🎧 正在播放：${{albumName}}`;
      
      const playPromise = audio.play();
      if (playPromise !== undefined) {{
        playPromise.then(() => {{
          isPlaying = true;
          playBtn.innerText = "⏸ 暫停";
        }}).catch(err => console.error("合輯播放錯誤:", err));
      }}
      document.querySelectorAll(".q-card").forEach(c => c.classList.remove("playing"));
    }}

    function updateUI() {{
      if (!isAlbumMode) {{
        const item = questionsData[currentIndex];
        if (item) {{
          const tag = currentUnit === "all" ? `【${{item.unitName}}】` : "";
          playingTitle.innerText = `${{tag}}第 ${{item.id}} 題：${{escapeHtml(item.question)}}`;
        }}
      }}
      playBtn.innerText = isPlaying ? "⏸ 暫停" : "▶ 播放";

      document.querySelectorAll(".q-card").forEach(c => c.classList.remove("playing"));
      if (!isAlbumMode) {{
        const activeCard = document.getElementById(`card-${{currentIndex}}`);
        if (activeCard) {{
          activeCard.classList.add("playing");
        }}
      }}
    }}

    playBtn.onclick = () => {{
      if (!audio.src) {{
        playQuestion(0);
        return;
      }}
      if (audio.paused) {{
        audio.play().then(() => {{
          isPlaying = true;
          updateUI();
        }});
      }} else {{
        audio.pause();
        isPlaying = false;
        updateUI();
      }}
    }};

    function getFilteredIndices() {{
      const indices = [];
      questionsData.forEach((item, index) => {{
        if (currentUnit === "all") {{
          if (currentFilter === "when" && item.unit !== "when") return;
          if (currentFilter === "why" && item.unit !== "why") return;
          indices.push(index);
        }} else {{
          if (currentFilter === "all" || item.category === currentFilter) {{
            indices.push(index);
          }}
        }}
      }});
      return indices;
    }}

    function getNextRandomIndex() {{
      const list = getFilteredIndices();
      if (list.length === 0) return 0;
      if (list.length === 1) return list[0];
      let nextIdx = list[Math.floor(Math.random() * list.length)];
      while (nextIdx === currentIndex && list.length > 1) {{
        nextIdx = list[Math.floor(Math.random() * list.length)];
      }}
      return nextIdx;
    }}

    randomBtn.onclick = () => {{
      const idx = getNextRandomIndex();
      playQuestion(idx);
    }};

    prevBtn.onclick = () => {{
      const list = getFilteredIndices();
      const pos = list.indexOf(currentIndex);
      if (pos > 0) {{
        playQuestion(list[pos - 1]);
      }} else if (currentIndex > 0) {{
        playQuestion(currentIndex - 1);
      }}
    }};

    nextBtn.onclick = () => {{
      if (shuffleMode.checked) {{
        playQuestion(getNextRandomIndex());
        return;
      }}
      const list = getFilteredIndices();
      const pos = list.indexOf(currentIndex);
      if (pos >= 0 && pos < list.length - 1) {{
        playQuestion(list[pos + 1]);
      }} else if (currentIndex < questionsData.length - 1) {{
        playQuestion(currentIndex + 1);
      }}
    }};

    audio.ontimeupdate = () => {{
      if (!isNaN(audio.duration) && audio.duration > 0) {{
        const percent = (audio.currentTime / audio.duration) * 100;
        progressFill.style.width = percent + "%";
        playingTime.innerText = `${{formatTime(audio.currentTime)}} / ${{formatTime(audio.duration)}}`;
      }}
    }};

    progressContainer.onclick = (e) => {{
      if (!isNaN(audio.duration) && audio.duration > 0) {{
        const rect = progressContainer.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const ratio = Math.max(0, Math.min(1, clickX / rect.width));
        audio.currentTime = ratio * audio.duration;
      }}
    }};

    audio.onended = () => {{
      if (isAlbumMode) {{
        isPlaying = false;
        updateUI();
        return;
      }}

      if (loopSingle.checked) {{
        audio.currentTime = 0;
        audio.play();
        return;
      }}

      if (autoPlayNext.checked) {{
        const delay = (currentUnit === "all" && questionsData[currentIndex]) 
          ? (questionsData[currentIndex].unit === "why" ? 2000 : 3000) 
          : config[currentUnit].autoDelay;
        const delaySec = delay / 1000;
        playingTitle.innerText = `準備下一題...（間隔 ${{delaySec}} 秒）`;
        setTimeout(() => {{
          if (shuffleMode.checked) {{
            playQuestion(getNextRandomIndex());
          }} else {{
            const list = getFilteredIndices();
            const pos = list.indexOf(currentIndex);
            if (pos >= 0 && pos < list.length - 1) {{
              playQuestion(list[pos + 1]);
            }} else if (currentIndex < questionsData.length - 1) {{
              playQuestion(currentIndex + 1);
            }} else {{
              isPlaying = false;
              updateUI();
            }}
          }}
        }}, delay);
      }} else {{
        isPlaying = false;
        updateUI();
      }}
    }};

    hideAnswer.onchange = () => renderList();

    // Tab 切換
    tabsContainer.onclick = (e) => {{
      if (e.target.classList.contains("tab-btn")) {{
        document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
        e.target.classList.add("active");
        currentFilter = e.target.getAttribute("data-cat");
        renderList();
      }}
    }};

    // 下載特定音檔清單輔助函數
    async function downloadAudioBatch(audioList, labelPrefix) {{
      if (!('caches' in window)) {{
        alert('您的瀏覽器不支援離線快取功能');
        return;
      }}
      if (!navigator.onLine) {{
        alert(`⚠️ 目前處於離線狀態（例如開啟了飛航模式）！\\n\\n請先連上 Wi-Fi 或行動網路，才能下載音檔到手機內喔！\\n下載完成後，就可以關閉網路離線使用了。`);
        cacheLabel.innerText = '⚠️ 請先連線網路，才能將音檔下載到手機中';
        cacheLabel.style.color = '#dc2626';
        return;
      }}

      btnDownloadCurrent.disabled = true;
      btnDownloadAll.disabled = true;
      cacheProgressBar.style.display = 'block';
      cacheLabel.innerText = `${{labelPrefix}} 下載中，請勿關閉網頁...`;
      cacheLabel.style.color = '#2563eb';

      const cache = await caches.open(CACHE_NAME);
      let successCount = 0;
      let failCount = 0;
      const total = audioList.length;

      for (let i = 0; i < total; i++) {{
        const url = audioList[i];
        try {{
          const response = await fetch(url);
          if (response.ok) {{
            await cache.put(url, response);
            successCount++;
          }} else {{
            failCount++;
          }}
        }} catch (err) {{
          failCount++;
          console.warn('下載失敗:', url, err);
        }}

        const done = i + 1;
        const pct = Math.round((done / total) * 100);
        cacheProgressFill.style.width = pct + '%';
        cacheLabel.innerText = `${{labelPrefix}} (${{done}}/${{total}} - ${{pct}}%)`;
      }}

      btnDownloadCurrent.disabled = false;
      btnDownloadAll.disabled = false;

      if (failCount === 0 && successCount === total) {{
        cacheLabel.innerText = `✅ 教材已全數離線儲存！即使無網路也能隨時播放。`;
        cacheLabel.style.color = '#059669';
      }} else {{
        cacheLabel.innerText = `⚠️ 下載未完全（成功 ${{successCount}} 題，失敗 ${{failCount}} 題），請在網路良好時重試。`;
        cacheLabel.style.color = '#dc2626';
      }}
      checkExistingCache();
    }}

    // 下載當前單元
    btnDownloadCurrent.onclick = () => {{
      const list = questionsData.map(item => getAudioPath(item));
      const title = currentUnit === 'when' ? '生活問答' : (currentUnit === 'why' ? '因果認知' : '全部雙單元');
      downloadAudioBatch(list, `正在下載【${{title}}】`);
    }};

    // 下載雙單元全部 200 題
    btnDownloadAll.onclick = () => {{
      const list = dataAll.map(item => getAudioPath(item));
      downloadAudioBatch(list, '正在下載雙單元全套 200 題');
    }};

    // 清理快取
    btnClearCache.onclick = async () => {{
      if (confirm('確定要清理離線快取嗎？清理後若沒有網路將無法播放。')) {{
        if ('caches' in window) {{
          const keys = await caches.keys();
          for (const key of keys) {{
            await caches.delete(key);
          }}
          cacheLabel.innerText = '已清除快取，需重新連線或下載。';
          cacheLabel.style.color = '#dc2626';
          cacheProgressBar.style.display = 'none';
          cacheProgressFill.style.width = '0%';
        }}
      }}
    }};

    // 檢查快取狀態
    async function checkExistingCache() {{
      if ('caches' in window) {{
        const cache = await caches.open(CACHE_NAME);
        const keys = await cache.keys();
        const urls = keys.map(k => k.url);
        const audioCount = urls.filter(u => u.includes('.mp3')).length;
        if (audioCount >= 200) {{
          cacheLabel.innerText = `✅ 雙單元 200 題已全數快取就緒（無網路隨時播放）`;
          cacheLabel.style.color = '#059669';
        }} else if (audioCount >= 100) {{
          cacheLabel.innerText = `✅ 已離線快取 ${{audioCount}} 題（無網路可播放已存項目）`;
          cacheLabel.style.color = '#059669';
        }} else if (audioCount > 0) {{
          cacheLabel.innerText = `⚠️ 目前已離線快取 ${{audioCount}} 題，建議連線補齊`;
          cacheLabel.style.color = '#d97706';
        }}
      }}
    }}

    // 初始化預設為生活問答單元
    switchUnit("when");
  </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_code)

print("Root index.html (PWA) with 3 unit tabs built successfully!")
