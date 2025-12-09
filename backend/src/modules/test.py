from src.modules.llm import giga

query = 'Что такое MIK-1?'
context = semsearch.search(query)[0]
response = giga.context_response([], context, query)
print(f'user: {query}\nLLM: {response}')