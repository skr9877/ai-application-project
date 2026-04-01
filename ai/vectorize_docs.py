"""
assets/docs/ 폴더의 모든 텍스트 파일을 읽어서 ChromaDB에 벡터화합니다.
이미 벡터화된 파일은 스킵합니다.

실행 방법:
    python ai/vectorize_docs.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from pathlib import Path
from rag import vector_store

DOCS_DIR = Path("./assets/docs")
SUPPORTED_EXTENSIONS = {".txt", ".md"}


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
