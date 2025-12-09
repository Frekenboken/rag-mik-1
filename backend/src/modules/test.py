from rag_system import RAG


rag = RAG('backend/src/static/docs', 'backend/src/vector_db', '*.md')

query = input('user: \n')
print(rag.interaction(query, ''))





