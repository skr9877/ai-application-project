from abc import ABC, abstractmethod
from sentence_transformers import SentenceTransformer
import chromadb

# ── 임베딩 인터페이스 (나중에 모델 교체 시 이것만 수정) ──────────────
class BaseEmbedder(ABC):
    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        pass


class KoSRobertaEmbedder(BaseEmbedder):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model = SentenceTransformer("./assets/models/ko-sroberta")
        return cls._instance

    def embed(self, texts: list[str]) -> list[list[float]]:
        return self.model.encode(texts, convert_to_numpy=True).tolist()


# ── 벡터 스토어 ────────────────────────────────────────────────────
class VectorStore:
    def __init__(self, embedder: BaseEmbedder, collection_name: str = "documents"):
        self.embedder = embedder
        self.client = chromadb.PersistentClient(path="./assets/chroma_db")
        self.collection = self.client.get_or_create_collection(collection_name)

    def add_file(self, filename: str, text: str) -> bool:
        # 파일명을 ID로 사용 — 이미 있으면 스킵
        existing = self.collection.get(ids=[filename])
        if existing["ids"]:
            return False
        embedding = self.embedder.embed([text])
        self.collection.add(documents=[text], embeddings=embedding, ids=[filename])
        return True

    def search(self, query: str, top_k: int = 3, threshold: float = 0.5) -> list[str]:
        if self.collection.count() == 0:
            return []
        embedding = self.embedder.embed([query])
        results = self.collection.query(query_embeddings=embedding, n_results=min(top_k, self.collection.count()), include=["documents", "distances"])
        docs, distances = results["documents"][0], results["distances"][0]
        return [doc for doc, dist in zip(docs, distances) if dist <= threshold]


# ── 싱글톤 인스턴스 ───────────────────────────────────────────────
_embedder = KoSRobertaEmbedder()
vector_store = VectorStore(_embedder)


def get_context(query: str, top_k: int = 3) -> str:
    docs = vector_store.search(query, top_k)
    if not docs:
        return ""
    return "\n\n".join(f"[참고 문서]\n{doc}" for doc in docs)
