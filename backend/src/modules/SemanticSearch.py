import faiss
import Rerank
import TextEmbedder

class SemanticSearch:
    def __init__(self, vector_db: faiss.swigfaiss_avx2.IndexFlatIP, chunks, rerank: Rerank(), embedding: TextEmbedder()):
        self.vector_db = vector_db
        self.chunks = chunks
        self.rerank = Rerank
        self.embedding = embedding

    def search_debuging(self, query_text, k=3):
        relevance = rerank.reranking_and_format(
            self.vector_db.search(self.embedding.get_embeddings([query_text.lower()]), k)[1][0],
            query_text.lower(),
            self.chunks
            )
        print(f"🔍 Запрос: '{query_text}'\n")
        for i, (similarity, idx) in enumerate(relevance):
            print(f"{i+1}.")
            print(f"{self.chunks[idx]}")
            print(f"   📊 Сходство: {similarity:.4f}\n")
            print("=" * 80)

    def search(self, query_text, k=3):
         relevance = rerank.reranking_and_format(
            self.vector_db.search(self.embedding.get_embeddings([query_text.lower()]), k)[1][0],
            query_text.lower(),
            self.chunks
            )
         return [self.chunks[idx] for similarity, idx in relevance]