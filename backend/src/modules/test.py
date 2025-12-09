from rag_system import RAG

rag = RAG('../static/docs/', 'vector_db', '*.md')

query = "Что такое МИК-1?"
print(rag.interaction(query, '').content)
