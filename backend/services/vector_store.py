# 벡터 DB 인터페이스
class VectorStore:
    def search(self, vector: list[float], top_k: int = 5) -> list[dict]:
        pass
