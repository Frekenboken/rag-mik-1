from langchain_gigachat.chat_models import GigaChat

from src.core.config import settings

def context_prompt(history, context, query_text):
    return f"""
    Ты — автоматизированная справочная система для инспекционной машины МИК-1.
    Твоя задача — извлекать факты из контекста и выдавать их пользователю в максимально сжатом виде.

    СТРОГИЕ ПРАВИЛА:
    1. ИСПОЛЬЗУЙ ТОЛЬКО КОНТЕКСТ. Если информации нет в контексте — отвечай одной фразой: "В базе данных нет информации по этому вопросу."
    2. МАКСИМАЛЬНАЯ КРАТКОСТЬ. Запрещены вводные слова ("Согласно документу...", "Ответ на ваш вопрос...", "Здравствуйте").
    3. ФОРМАТ ОТВЕТА. Если ответ — число или параметр, пиши только значение. Если ответ — инструкция, пиши нумерованный список в повелительном наклонении (Сделай, Включи, Проверь).
    4. СТИЛЬ. Официально-деловой, безэмоциональный. Обращение на "Вы".
    5. ЗАПРЕЩЕНО давать советы или информацию, которой нет в тексте.

    История диалога:
    {history}

    Контекст:
    {context}

    Вопрос пользователя: {query_text}

    Примеры правильных ответов (следуй этому стилю):
    Q: Какая максимальная высота изделия?
    A: 410 мм

    Q: Как включить машину?
    A: 1. Повернуть главный рубильник. 2. Нажать кнопку "Пуск".

    Q: Какая потребляемая мощность?
    A: 3.5 кВт
    """

class LLM:
    def __init__(
            self,
            cont_prompt,
            credentials=settings.GIGACHAT_API_TOKEN,
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

