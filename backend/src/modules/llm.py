
context_promt = lambda history, context, query_text: f"""
        Ты - техническая система поддержки для инспекционной машины МИК-1.
        Используя только предоставленный контекст, ответь на вопрос пользователя.

        История диалога:
        {history}

        Контекст:
        {context}

        Вопрос: {query_text}
        """

class RussianLLM:
    def __init__(
            self,
            cont_promt,
            credentials='MDE5YWViMmQtNDYzOC03OGRiLTk4OGEtNDdmNzkxOWVlNTFkOmVjMzRhN2Q4LWE4ZjQtNDUwNS1hNjk0LTk5OGFlNmNmYmU3NA==',
            verify_ssl_certs=False
            ):
        from langchain_gigachat.chat_models import GigaChat
        print("Инициализация LLM...")
        self.model = GigaChat(credentials=credentials, verify_ssl_certs=verify_ssl_certs)
        self.cont_promt = cont_promt
        print("Завершено!")

    def context_response(self, history, context, query_text):
        response = self.model.invoke(self.cont_promt(history, context, query_text))
        return response

    def no_contex_response(self, prompt):
        return self.model.invoke(promt)

    def docs_chunker(self, docs, docs_promt):
        chunked_docs = [self.model.no_context_response(docs_promt + doc).content.split('\n\n') for doc in docs]
        return chunked_docs


giga = RussianLLM(context_promt)