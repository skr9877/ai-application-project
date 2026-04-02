"""
assets/docs/ 폴더의 모든 텍스트 파일을 읽어서 ChromaDB에 벡터화합니다.
- [질문]/[답변] 블록이 있는 파일은 블록 단위로 청킹하여 저장
- 일반 텍스트 파일은 파일 단위로 저장
- 이미 벡터화된 항목은 스킵합니다.

실행 방법:
    python ai/vectorize_docs.py
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rag import vector_store

DOCS_DIR = Path("./assets/docs")
SUPPORTED_EXTENSIONS = {".txt", ".md"}


def parse_qa_chunks(text: str) -> list[str]:
    """카테고리/객체명 헤더를 각 Q&A 청크에 붙여서 분리.
    카테고리는 '>' 구분자로 계층화 가능 (예: [개발 > 백엔드])
    """
    chunks = []
    header_lines = []
    current_qa = []

    for line in text.splitlines():
        line = line.strip()
        if not line:
            if current_qa:
                qa_text = "\n".join(current_qa)
                if "[질문]" in qa_text and "[답변]" in qa_text:
                    header = "\n".join(header_lines)
                    chunks.append(f"{header}\n{qa_text}" if header else qa_text)
                current_qa = []
        elif line.startswith("카테고리") or line.startswith("객체명"):
            header_lines.append(line)
        else:
            current_qa.append(line)

    # 마지막 블록 처리
    if current_qa:
        qa_text = "\n".join(current_qa)
        if "[질문]" in qa_text and "[답변]" in qa_text:
            header = "\n".join(header_lines)
            chunks.append(f"{header}\n{qa_text}" if header else qa_text)

    return chunks


def index_all():
    files = [f for f in DOCS_DIR.iterdir() if f.suffix in SUPPORTED_EXTENSIONS]

    if not files:
        print("docs 폴더에 문서가 없습니다.")
        return

    added, skipped = 0, 0

    for file in files:
        text = file.read_text(encoding="utf-8").strip()
        if not text:
            print(f"[스킵] {file.name} - 내용 없음")
            skipped += 1
            continue

        chunks = parse_qa_chunks(text)
        if chunks:
            count = vector_store.add_chunks(file.name, chunks)
            if count > 0:
                print(f"[추가] {file.name} - {count}개 청크")
                added += count
            else:
                print(f"[스킵] {file.name} - 이미 벡터화됨")
                skipped += 1
        else:
            result = vector_store.add_file(file.name, text)
            if result:
                print(f"[추가] {file.name}")
                added += 1
            else:
                print(f"[스킵] {file.name} - 이미 벡터화됨")
                skipped += 1

    print(f"\n완료: {added}개 추가, {skipped}개 스킵 / 전체 문서 수: {vector_store.collection.count()}")


if __name__ == "__main__":
    index_all()
