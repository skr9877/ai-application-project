# AI 채팅 상담 서버

FastAPI 기반 AI 상담 채팅 서버입니다. 비즈니스 서버에 스크립트 한 줄만 추가하면 채팅 위젯이 활성화됩니다.

---

## 사용 모델

| 역할 | 모델 | 비고 |
|------|------|------|
| 언어 모델 (LLM) | [MLP-KTLim/llama-3-Korean-Bllossom-8B-gguf-Q4_K_M](https://huggingface.co/MLP-KTLim/llama-3-Korean-Bllossom-8B-gguf-Q4_K_M) | 한국어 특화 Llama3 8B, Q4_K_M 양자화 |
| 임베딩 모델 (RAG) | [jhgan/ko-sroberta-multitask](https://huggingface.co/jhgan/ko-sroberta-multitask) | 한국어 문장 임베딩 |
| 벡터 DB | ChromaDB | 로컬 퍼시스턴트 저장 |

---

## 프로젝트 구조

```
ai_application_project/
├── main.py                      # FastAPI 앱 진입점
├── ai/
│   ├── core/                    # 공유 핵심 모듈 (전처리/서빙 양쪽에서 사용)
│   │   └── rag.py               # 임베딩, 벡터 저장/검색
│   ├── preprocess/              # 문서 전처리 및 벡터화
│   │   └── vectorize_docs.py    # docs 벡터화 실행 스크립트
│   └── serve/                   # 모델 서빙 (채팅 답변 생성)
│       └── model.py             # LLM 로드 및 응답 생성
├── chatting/
│   ├── chat.py                  # WebSocket 세션 관리, 동시접속 제한(100명)
│   └── templates/
│       └── chat.html            # 채팅 UI
├── assets/
│   ├── models/                  # 모델 파일 (git 제외)
│   │   ├── llama-3-Korean-Bllossom-8B-Q4_K_M.gguf
│   │   └── ko-sroberta/
│   ├── chroma_db/               # 벡터 DB 저장소 (자동 생성, git 제외)
│   ├── docs/                    # RAG용 원본 문서 보관
│   └── prompts/
│       └── system_prompt.txt    # AI 시스템 프롬프트 (수정 가능)
└── requirements.txt
```

---

## 설치 및 실행

### 1. 사전 요구사항
- Python 3.10+
- CUDA 12.x (GPU 가속 사용 시)
- NVIDIA GPU (VRAM 8GB 이상 권장)

### 2. 모델 다운로드
```bash
# LLM 모델 (약 5GB)
hf download MLP-KTLim/llama-3-Korean-Bllossom-8B-gguf-Q4_K_M \
  llama-3-Korean-Bllossom-8B-Q4_K_M.gguf --local-dir ./assets/models

# 임베딩 모델
hf download jhgan/ko-sroberta-multitask --local-dir ./assets/models/ko-sroberta
```

### 3. 패키지 설치
```bash
python -m venv venv
./venv/Scripts/activate
pip install -r requirements.txt
```

### 4. 문서 벡터화
`assets/docs/` 에 `.txt` 또는 `.md` 파일을 넣고 실행:
```bash
python ai/preprocess/vectorize_docs.py
```

### 5. 서버 실행
```bash
uvicorn main:app --reload
```

---

## 사용 방법

### 채팅 접속
```
http://localhost:8000/chat
```

### 비즈니스 서버에서 채팅 연결
버튼에 아래 URL 연결:
```html
<button onclick="window.open('http://서버주소:8000/chat', 'chat', 'width=420,height=640')">
  상담하기
</button>
```

---

## 인프라

- IBM 서버 2대 + L4 로드밸런서
- 서버당 최대 동시 접속 100명

## 사용 이미지
<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/480706d6-683b-4800-ade2-3e2633a6e20d" />

