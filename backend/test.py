from src.modules.rag_system import rag

query = 'Какой максимальный вес стеклоизделия может контроллировать мик-1?'

rag.semsearch_debug(query, k=5)
answer = rag.interaction(query, '')

print(f'user: {query}\nLLM: {answer}')
rag.keyword_extraction_debug(answer)