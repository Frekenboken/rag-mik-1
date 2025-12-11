from src.modules.rag_system import RAG

rag = RAG('src/static/docs/', 'src/vector_db/', '*.md')
query = 'Какой вес стеклоизделия может контроллировать мик-1?'
rag.keyword_extraction_debug(query)
'''rag.semsearch_debug(query, k=5)
answer = rag.interaction(query, '')

print(f'user: {query}\nLLM: {answer}')
rag.keyword_extraction_debug(query)'''