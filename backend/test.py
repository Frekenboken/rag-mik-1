from src.modules.rag_system import rag

query = "Какой максимальный вес стеклоизделия может контроллировать MIK-1?"

rag.semsearch_debug(query, k=5)
#answer = rag.interaction(query, '', k=5)
#print(f'user: {query}\nLLM: {answer[0].content}\nИсточники: {'; '.join(answer[1])}')
