from langchain_gigachat.chat_models import GigaChat


def context_prompt(history, context, query_text):
    return f"""
    Ты - техническая система поддержки для инспекционной машины МИК-1.
    Используя только предоставленный контекст, ответь на вопрос пользователя.

    История диалога:
    {history}

    Контекст:
    {context}

    Вопрос: {query_text}
    """

class LLM:
    def __init__(
            self,
            cont_prompt,
            credentials='MDE5YWViMmQtNDYzOC03OGRiLTk4OGEtNDdmNzkxOWVlNTFkOmVjMzRhN2Q4LWE4ZjQtNDUwNS1hNjk0LTk5OGFlNmNmYmU3NA==',
            verify_ssl_certs=False
            ):
        print("Инициализация LLM...")
        self.model = GigaChat(credentials=credentials, verify_ssl_certs=verify_ssl_certs)
        self.cont_prompt = cont_prompt
        print("Завершено!")

    def context_response(self, history, context, query_text):
        response = self.model.invoke(self.cont_prompt(history, context, query_text))
        return response

    def no_contex_response(self, prompt):
        return self.model.invoke(prompt)

    def docs_chunker(self, docs, docs_prompt):
        chunked_docs = [self.model.no_context_response(docs_prompt + doc).content.split('\n\n') for doc in docs]
        return chunked_docs
