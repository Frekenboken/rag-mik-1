from rag_system import RAG

rag = RAG('../static/docs/', 'vector_db', '*.md')

query = "Что такое МИК-1?"
answer = rag.interaction(query, '').content
print(f'user: {query}\nLLM: {}')
