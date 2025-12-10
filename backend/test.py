from src.modules.rag_system import rag

query = "в каком температурном диапазоне может работать мик-1?"

rag.semsearch_debug(query, k=5)
answer = rag.interaction(query, '', k=5)
print(f'user: {query}\nLLM: {answer}')
