(function () {
  // 채팅 서버 URL 자동 감지 (script src 기준)
  const scriptEl = document.currentScript;
  const serverUrl = scriptEl
    ? new URL(scriptEl.src).origin
    : window.location.origin;

  const CHAT_URL = `${serverUrl}/chat`;

  // 중복 삽입 방지
  if (document.getElementById("ai-chat-widget")) return;

  const style = document.createElement("style");
  style.textContent = `
    #ai-chat-widget-btn {
      position: fixed;
      bottom: 24px;
      right: 24px;
      width: 56px;
      height: 56px;
      border-radius: 50%;
      background: #4f46e5;
      color: white;
      font-size: 26px;
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 16px rgba(0,0,0,0.2);
      z-index: 9999;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: background 0.2s;
    }
    #ai-chat-widget-btn:hover { background: #4338ca; }

    #ai-chat-widget {
      position: fixed;
      bottom: 90px;
      right: 24px;
      width: 420px;
      height: 620px;
      border: none;
      border-radius: 16px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.18);
      z-index: 9998;
      display: none;
      transition: opacity 0.2s;
    }

    @media (max-width: 480px) {
      #ai-chat-widget {
        width: 100vw;
        height: 100vh;
        bottom: 0;
        right: 0;
        border-radius: 0;
      }
    }
  `;
  document.head.appendChild(style);

  // 채팅 버튼
  const btn = document.createElement("button");
  btn.id = "ai-chat-widget-btn";
  btn.innerHTML = "💬";
  btn.title = "AI 상담";
  document.body.appendChild(btn);

  // 채팅 iframe
  const iframe = document.createElement("iframe");
  iframe.id = "ai-chat-widget";
  iframe.src = CHAT_URL;
  iframe.allow = "microphone";
  document.body.appendChild(iframe);

  // 버튼 클릭 토글
  let isOpen = false;
  btn.addEventListener("click", () => {
    isOpen = !isOpen;
    iframe.style.display = isOpen ? "block" : "none";
    btn.innerHTML = isOpen ? "✕" : "💬";
  });
})();
