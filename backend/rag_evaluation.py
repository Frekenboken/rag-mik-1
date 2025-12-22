from src.modules.rag_system import RAG

rag = RAG('src/static/questions/', 'src/static/docs/', 'src/vector_db/', '*.md')

'''query = input('user: ')
while query != 'стоп':
    #rag.semsearch_debug(query, k=5)
    print('llm:', rag.interaction(query, ''))
    query = input('user: ')'''
rag.llm_debug()
#rag.rag_rating()