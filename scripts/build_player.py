import json

with open("data/questions.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

json_str = json.dumps(questions, ensure_ascii=False, indent=2)

html_template = """<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>生活問答特教練習播放器（100題）</title>
  <style>
    :root {
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --text-main: #0f172a;
      --text-muted: #64748b;
      --border: #cbd5e1;
      --active-card: #eff6ff;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang TC", "Microsoft JhengHei", sans-serif;
      background: var(--bg);
      color: var(--text-main);
      padding: 16px;
      padding-bottom: 120px;
    }

    header {
      max-width: 900px;
      margin: 0 auto 16px;
      text-align: center;
    }

    h1 {
      font-size: 1.5rem;
      color: #1e3a8a;
      margin-bottom: 6px;
    }

    .subtitle {
      font-size: 0.9rem;
      color: var(--text-muted);
    }

    /* 頂部播放器 Dock */
    .player-dock {
      position: sticky;
      top: 10px;
      z-index: 100;
      max-width: 900px;
      margin: 0 auto 16px;
      background: rgba(255, 255, 255, 0.98);
      backdrop-filter: blur(10px);
      border: 2px solid #93c5fd;
      border-radius: 16px;
      padding: 16px 20px;
      box-shadow: 0 8px 24px rgba(37, 99, 235, 0.15);
    }

    .now-playing {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      font-weight: 700;
      color: #1e40af;
      font-size: 1.15rem;
    }

    .status-msg {
      font-size: 0.85rem;
      color: #dc2626;
      font-weight: 500;
      margin-top: 4px;
    }

    .controls-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;
      gap: 12px;
      margin-bottom: 10px;
    }

    .btn {
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
    }

    .btn-primary {
      background: var(--primary);
      color: white;
      box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
    }
    .btn-primary:hover {
      background: var(--primary-hover);
    }

    .btn-outline {
      background: white;
      border: 1.5px solid var(--border);
      color: var(--text-main);
    }
    .btn-outline:hover {
      background: #f1f5f9;
    }

    .progress-bar-container {
      width: 100%;
      height: 6px;
      background: #e2e8f0;
      border-radius: 999px;
      overflow: hidden;
      margin-bottom: 12px;
      cursor: pointer;
    }

    .progress-bar-fill {
      height: 100%;
      width: 0%;
      background: var(--primary);
      transition: width 0.1s linear;
    }

    .toggle-group {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: center;
      gap: 16px;
      font-size: 0.9rem;
      color: var(--text-muted);
    }

    .toggle-label {
      display: flex;
      align-items: center;
      gap: 6px;
      cursor: pointer;
      font-weight: 500;
    }

    /* 大合輯專用快捷播放區 */
    .album-shortcuts {
      max-width: 900px;
      margin: 0 auto 16px;
      background: #eff6ff;
      border: 1px dashed #60a5fa;
      border-radius: 12px;
      padding: 12px 16px;
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
    }

    .album-title {
      font-size: 0.9rem;
      font-weight: 700;
      color: #1e40af;
      margin-right: 6px;
    }

    .btn-sm {
      padding: 6px 12px;
      font-size: 0.85rem;
      border-radius: 8px;
    }

    /* 分類標籤頁 */
    .category-tabs {
      max-width: 900px;
      margin: 0 auto 16px;
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .tab-btn {
      padding: 8px 14px;
      border-radius: 10px;
      background: white;
      border: 1.5px solid var(--border);
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      color: var(--text-muted);
      transition: all 0.15s ease;
    }
    .tab-btn.active {
      background: #2563eb;
      color: white;
      border-color: #2563eb;
    }

    /* 題目網格列表 */
    .question-list {
      max-width: 900px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 14px;
    }

    .q-card {
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
    }

    .q-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
      border-color: #60a5fa;
    }

    .q-card.playing {
      background: var(--active-card);
      border-color: #2563eb;
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.3);
    }

    .q-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
    }

    .badge {
      font-size: 0.8rem;
      font-weight: 800;
      padding: 3px 8px;
      border-radius: 6px;
      background: #e2e8f0;
      color: #334155;
    }

    .badge-playing {
      background: #2563eb;
      color: white;
    }

    .q-title {
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-main);
      margin-bottom: 10px;
      line-height: 1.4;
    }

    .q-answer {
      font-size: 1.05rem;
      color: #047857;
      font-weight: 700;
      background: #d1fae5;
      padding: 6px 10px;
      border-radius: 8px;
      align-self: flex-start;
    }

    .hidden-answer {
      filter: blur(8px);
      user-select: none;
      transition: filter 0.2s ease;
      background: #f1f5f9;
      color: #94a3b8;
    }
    .hidden-answer:hover, .hidden-answer:active {
      filter: blur(0);
      background: #d1fae5;
      color: #047857;
    }
  </style>
</head>
<body>

  <header>
    <h1>生活問答特教教材（100題）</h1>
    <p class="subtitle">臺灣國語自然女聲（語速 90% | 問後停頓 3 秒 | 題間間隔 3 秒）</p>
  </header>

  <!-- 頂部播放器 Dock -->
  <div class="player-dock">
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
    </div>

    <div class="toggle-group">
      <label class="toggle-label">
        <input type="checkbox" id="autoPlayNext" checked> 自動連續播放（題間停3秒）
      </label>
      <label class="toggle-label">
        <input type="checkbox" id="loopSingle"> 單題循環重複聽
      </label>
      <label class="toggle-label">
        <input type="checkbox" id="hideAnswer"> 隱藏答案（測驗模式，碰一下看答案）
      </label>
    </div>
    <div id="statusMsg" class="status-msg"></div>
  </div>

  <!-- 合輯快捷播放 -->
  <div class="album-shortcuts">
    <span class="album-title">🚌 復康巴士一鍵合輯：</span>
    <button class="btn btn-outline btn-sm" id="btnAlbumFull">▶ 100題完整大合輯</button>
    <button class="btn btn-outline btn-sm" id="btnAlbum1">1. 生理需求</button>
    <button class="btn btn-outline btn-sm" id="btnAlbum2">2. 生活作息</button>
    <button class="btn btn-outline btn-sm" id="btnAlbum3">3. 穿著天氣</button>
    <button class="btn btn-outline btn-sm" id="btnAlbum4">4. 學校學習</button>
    <button class="btn btn-outline btn-sm" id="btnAlbum5">5. 外出安全</button>
    <button class="btn btn-outline btn-sm" id="btnAlbum6">6. 季節事件</button>
  </div>

  <!-- 分類篩選 Tab -->
  <div class="category-tabs" id="tabs">
    <button class="tab-btn active" data-cat="all">全部 100 題</button>
    <button class="tab-btn" data-cat="第一類：身體需求與生理反應">1. 生理需求 (1-20)</button>
    <button class="tab-btn" data-cat="第二類：生活作息">2. 生活作息 (21-40)</button>
    <button class="tab-btn" data-cat="第三類：穿著與天氣">3. 穿著天氣 (41-55)</button>
    <button class="tab-btn" data-cat="第四類：學校與學習">4. 學校學習 (56-70)</button>
    <button class="tab-btn" data-cat="第五類：外出與安全">5. 外出安全 (71-85)</button>
    <button class="tab-btn" data-cat="第六類：季節、節日與事件">6. 季節事件 (86-100)</button>
  </div>

  <!-- 題目列表 -->
  <div class="question-list" id="qList"></div>

  <audio id="audioElement" preload="auto"></audio>

  <script>
    // 直接內嵌 100 題題庫，避免直接以 file:// 開啟時受瀏覽器 CORS 限制影響！
    const questionsData = __QUESTIONS_DATA__;

    let currentIndex = 0;
    let isPlaying = false;
    let isAlbumMode = false;
    let currentFilter = "all";

    const audio = document.getElementById("audioElement");
    const playBtn = document.getElementById("playBtn");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const playingTitle = document.getElementById("playingTitle");
    const playingTime = document.getElementById("playingTime");
    const progressFill = document.getElementById("progressFill");
    const progressContainer = document.getElementById("progressContainer");
    const autoPlayNext = document.getElementById("autoPlayNext");
    const loopSingle = document.getElementById("loopSingle");
    const hideAnswer = document.getElementById("hideAnswer");
    const statusMsg = document.getElementById("statusMsg");
    const qList = document.getElementById("qList");

    function formatTime(seconds) {
      if (isNaN(seconds) || seconds < 0) return "00:00";
      const m = Math.floor(seconds / 60);
      const s = Math.floor(seconds % 60);
      return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
    }

    function getAudioPath(item) {
      const cleanQ = item.question.replace("？", "").replace("?", "").trim();
      const idStr = String(item.id).padStart(3, "0");
      return encodeURI(`../output/singles/第${idStr}題_${cleanQ}.mp3`);
    }

    function renderList() {
      qList.innerHTML = "";
      const isHidden = hideAnswer.checked;

      questionsData.forEach((item, index) => {
        if (currentFilter !== "all" && item.category !== currentFilter) {
          return;
        }

        const card = document.createElement("div");
        card.className = `q-card ${!isAlbumMode && index === currentIndex && isPlaying ? "playing" : ""}`;
        card.id = `card-${index}`;
        card.onclick = () => playQuestion(index);

        card.innerHTML = `
          <div>
            <div class="q-header">
              <span class="badge ${!isAlbumMode && index === currentIndex && isPlaying ? "badge-playing" : ""}">第 ${item.id} 題</span>
              <span style="font-size: 0.75rem; color: #64748b; font-weight: 500;">${item.category.split("：")[1] || item.category}</span>
            </div>
            <div class="q-title">${item.question}</div>
          </div>
          <div class="q-answer ${isHidden ? 'hidden-answer' : ''}">${item.answer}</div>
        `;
        qList.appendChild(card);
      });
    }

    function playQuestion(index) {
      if (index < 0 || index >= questionsData.length) return;
      isAlbumMode = false;
      currentIndex = index;
      const item = questionsData[index];
      const audioSrc = getAudioPath(item);

      statusMsg.innerText = "";
      audio.src = audioSrc;
      audio.load();
      
      const playPromise = audio.play();
      if (playPromise !== undefined) {
        playPromise.then(() => {
          isPlaying = true;
          updateUI();
        }).catch(err => {
          console.error("播放失敗:", err);
          statusMsg.innerText = "瀏覽器限制自動發音，請點擊上方「播放」按鈕。";
        });
      }
      updateUI();
    }

    function playAlbum(albumPath, albumName) {
      isAlbumMode = true;
      statusMsg.innerText = "";
      audio.src = encodeURI(albumPath);
      audio.load();
      playingTitle.innerText = `🎧 正在播放：${albumName}`;
      
      const playPromise = audio.play();
      if (playPromise !== undefined) {
        playPromise.then(() => {
          isPlaying = true;
          playBtn.innerText = "⏸ 暫停";
        }).catch(err => {
          console.error("合輯播放失敗:", err);
        });
      }
      document.querySelectorAll(".q-card").forEach(c => c.classList.remove("playing"));
    }

    // 綁定合輯按鈕事件
    document.getElementById("btnAlbumFull").onclick = () => playAlbum("../output/full_100_compilation.mp3", "100題完整大合輯 (19分鐘)");
    document.getElementById("btnAlbum1").onclick = () => playAlbum("../output/categories/01_第一類_身體需求與生理反應(1-20題).mp3", "第一類：身體需求 (1-20題)");
    document.getElementById("btnAlbum2").onclick = () => playAlbum("../output/categories/02_第二類_生活作息(21-40題).mp3", "第二類：生活作息 (21-40題)");
    document.getElementById("btnAlbum3").onclick = () => playAlbum("../output/categories/03_第三類_穿著與天氣(41-55題).mp3", "第三類：穿著天氣 (41-55題)");
    document.getElementById("btnAlbum4").onclick = () => playAlbum("../output/categories/04_第四類_學校與學習(56-70題).mp3", "第四類：學校學習 (56-70題)");
    document.getElementById("btnAlbum5").onclick = () => playAlbum("../output/categories/05_第五類_外出與安全(71-85題).mp3", "第五類：外出安全 (71-85題)");
    document.getElementById("btnAlbum6").onclick = () => playAlbum("../output/categories/06_第六類_季節節日與事件(86-100題).mp3", "第六類：季節事件 (86-100題)");

    function updateUI() {
      if (!isAlbumMode) {
        const item = questionsData[currentIndex];
        if (item) {
          playingTitle.innerText = `第 ${item.id} 題：${item.question}`;
        }
      }
      playBtn.innerText = isPlaying ? "⏸ 暫停" : "▶ 播放";

      document.querySelectorAll(".q-card").forEach(c => c.classList.remove("playing"));
      if (!isAlbumMode) {
        const activeCard = document.getElementById(`card-${currentIndex}`);
        if (activeCard) {
          activeCard.classList.add("playing");
        }
      }
    }

    playBtn.onclick = () => {
      if (!audio.src) {
        playQuestion(0);
        return;
      }
      if (audio.paused) {
        audio.play().then(() => {
          isPlaying = true;
          updateUI();
        });
      } else {
        audio.pause();
        isPlaying = false;
        updateUI();
      }
    };

    prevBtn.onclick = () => {
      if (currentIndex > 0) playQuestion(currentIndex - 1);
    };

    nextBtn.onclick = () => {
      if (currentIndex < questionsData.length - 1) playQuestion(currentIndex + 1);
    };

    audio.ontimeupdate = () => {
      if (!isNaN(audio.duration) && audio.duration > 0) {
        const percent = (audio.currentTime / audio.duration) * 100;
        progressFill.style.width = percent + "%";
        playingTime.innerText = `${formatTime(audio.currentTime)} / ${formatTime(audio.duration)}`;
      }
    };

    progressContainer.onclick = (e) => {
      if (!isNaN(audio.duration) && audio.duration > 0) {
        const rect = progressContainer.getBoundingClientRect();
        const clickX = e.clientX - rect.left;
        const ratio = Math.max(0, Math.min(1, clickX / rect.width));
        audio.currentTime = ratio * audio.duration;
      }
    };

    audio.onerror = (e) => {
      console.error("Audio error:", e);
      statusMsg.innerText = "音訊載入失敗，請確認檔案是否存在。";
    };

    audio.onended = () => {
      if (isAlbumMode) {
        isPlaying = false;
        updateUI();
        return;
      }

      if (loopSingle.checked) {
        audio.currentTime = 0;
        audio.play();
        return;
      }

      if (autoPlayNext.checked) {
        playingTitle.innerText = `準備下一題...（間隔 3 秒）`;
        setTimeout(() => {
          if (currentIndex < questionsData.length - 1) {
            playQuestion(currentIndex + 1);
          } else {
            isPlaying = false;
            updateUI();
          }
        }, 3000);
      } else {
        isPlaying = false;
        updateUI();
      }
    };

    hideAnswer.onchange = () => renderList();

    // Tab 切換
    document.getElementById("tabs").onclick = (e) => {
      if (e.target.classList.contains("tab-btn")) {
        document.querySelectorAll(".tab-btn").forEach(b => b.classList.remove("active"));
        e.target.classList.add("active");
        currentFilter = e.target.getAttribute("data-cat");
        renderList();
      }
    };

    // 初始載入渲染
    renderList();
  </script>
</body>
</html>
"""

html_out = html_template.replace("__QUESTIONS_DATA__", json_str)
with open("web_player/index.html", "w", encoding="utf-8") as f:
    f.write(html_out)

print("web_player/index.html built successfully!")
