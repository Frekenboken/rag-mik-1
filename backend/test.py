from src.modules.rag_system import RAG

rag = RAG('src/static/questions/', 'src/static/docs/', 'src/vector_db/', '*.md')

input('press enter')

rag.rag_rating()
#rag.semsearch_debug(query, k=5)
#answer = rag.interaction(query, '', k=10)

#print(f'user: {query}\nLLM: {answer}')
#rag.keyword_extraction_debug(answer)