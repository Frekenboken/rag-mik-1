from src.modules.rag_system import RAG

rag = RAG('src/static/questions/', 'src/static/docs/', 'src/vector_db/', '*.md')

#rag.rag_rating()