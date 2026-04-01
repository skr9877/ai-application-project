(function () {
  const scriptEl = document.currentScript;
  const serverUrl = scriptEl
    ? new URL(scriptEl.src).origin
    : window.location.origin;

  const CHAT_URL = `${serverUrl}/chat`;

  if (document.getElementById("ai-chat-widget-wrap")) return;

  const style = document.createElement("style");
  style.textContent = `
    #ai-chat-widget-btn {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: linear-gradient(135deg, #4f46e5, #7c3aed);
      color: white;
      font-size: 26px;
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(79,70,229,0.4);
      z-index: 9999;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.2s, opacity 0.2s;
    }
    #ai-chat-widget-btn:hover { transform: scale(1.08); }

    #ai-chat-widget-wrap {
      position: fixed;
      width: 420px;
      height: 640px;
      bottom: 90px;
      right: 24px;
      z-index: 9998;
      display: none;
      flex-direction: column;
      border-radius: 16px;
      box-shadow: 0 8px 40px rgba(0,0,0,0.22);
      overflow: hidden;
      user-select: none;
    }

    #ai-chat-widget-titlebar {
      background: linear-gradient(135deg, #4f46e5, #7c3aed);
      color: white;
      padding: 10px 14px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      cursor: grab;
      flex-shrink: 0;
    }

    #ai-chat-widget-titlebar:active { cursor: grabbing; }

    #ai-chat-widget-titlebar .title {
      font-size: 14px;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    #ai-chat-widget-close {
      background: rgba(255,255,255,0.2);
      border: none;
      color: white;
      width: 26px;
      height: 26px;
      border-radius: 50%;
      cursor: pointer;
      font-size: 14px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s;
    }
    #ai-chat-widget-close:hover { background: rgba(255,255,255,0.35); }

    #ai-chat-widget-iframe {
      flex: 1;
      border: none;
      width: 100%;
    }
  `;
  document.head.appendChild(style);

  // 플로팅 버튼
  const btn = document.createElement("button");
  btn.id = "ai-chat-widget-btn";
  btn.innerHTML = "💬";
  btn.title = "AI 상담";
  document.body.appendChild(btn);

  // 팝업 래퍼
  const wrap = document.createElement("div");
  wrap.id = "ai-chat-widget-wrap";

  // 타이틀바 (드래그 핸들)
  const titlebar = document.createElement("div");
  titlebar.id = "ai-chat-widget-titlebar";
  titlebar.innerHTML = `
    <div class="title">🤖 AI 상담원</div>
    <button id="ai-chat-widget-close">✕</button>
  `;
  wrap.appendChild(titlebar);

  // iframe
  const iframe = document.createElement("iframe");
  iframe.id = "ai-chat-widget-iframe";
  iframe.src = CHAT_URL;
  wrap.appendChild(iframe);

  document.body.appendChild(wrap);

  // 열기/닫기
  btn.addEventListener("click", () => {
    wrap.style.display = "flex";
    btn.style.display = "none";
  });

  document.getElementById("ai-chat-widget-close").addEventListener("click", () => {
    wrap.style.display = "none";
    btn.style.display = "flex";
  });

  // 드래그 이동
  let isDragging = false;
  let dragOffsetX = 0;
  let dragOffsetY = 0;

  titlebar.addEventListener("mousedown", (e) => {
    if (e.target.id === "ai-chat-widget-close") return;
    isDragging = true;
    const rect = wrap.getBoundingClientRect();
    dragOffsetX = e.clientX - rect.left;
    dragOffsetY = e.clientY - rect.top;
    wrap.style.transition = "none";
  });

  document.addEventListener("mousemove", (e) => {
    if (!isDragging) return;
    let x = e.clientX - dragOffsetX;
    let y = e.clientY - dragOffsetY;

    // 화면 밖으로 못 나가게
    x = Math.max(0, Math.min(window.innerWidth - wrap.offsetWidth, x));
    y = Math.max(0, Math.min(window.innerHeight - wrap.offsetHeight, y));

    wrap.style.right = "auto";
    wrap.style.bottom = "auto";
    wrap.style.left = x + "px";
    wrap.style.top = y + "px";
  });

  document.addEventListener("mouseup", () => {
    isDragging = false;
  });
})();
