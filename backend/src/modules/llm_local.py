from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TextStreamer
import torch

def context_prompt(history, context, query_text):
    return f"""
    Ты — автоматизированная справочная система для инспекционной машины МИК-1.
    Твоя задача — извлекать факты из контекста и выдавать их пользователю в максимально сжатом виде.

    СТРОГИЕ ПРАВИЛА:
    1. ИСПОЛЬЗУЙ ТОЛЬКО КОНТЕКСТ. Если информации нет в контексте — отвечай одной фразой: "В базе данных нет информации по этому вопросу."
    2. МАКСИМАЛЬНАЯ КРАТКОСТЬ. Запрещены вводные слова ("Согласно документу...", "Ответ на ваш вопрос...", "Здравствуйте").
    3. ФОРМАТ ОТВЕТА. Если ответ — число или параметр, пиши только значение. Если ответ — инструкция, пиши нумерованный список в повелительном наклонении (Сделайте, Включите, Проверьте).
    4. СТИЛЬ. Официально-деловой, безэмоциональный. Обращение на "Вы".
    5. ЗАПРЕЩЕНО давать советы или информацию, которой нет в тексте.

    История диалога:
    {history}

    Контекст:
    {context}

    Примеры правильных ответов (следуй этому стилю):
    Q: Какая максимальная высота изделия?
    A: 410 мм

    Q: Как включить машину?
    A: 1. Повернуть главный рубильник. 2. Нажать кнопку "Пуск".

    Q: Что означает ошибка E003?
    A: Критическая ошибка - сбой инициализации камер. Требуется проверка подключения камер и перезапуск системы

    Q: Какие типы стекла по цвету поддерживает система?
    A: БС (бесцветное), ПС (полубелое), ЗС-1 (зеленое с хромом), ЗС-2 (зеленое с железом), КС (коричневое), а также синее и красное различных оттенков
    
    
    Q: {query_text}
    """


class LLM:
    def __init__(
            self,
            device_map="cuda",
            model_id="Qwen/Qwen2.5-1.5B-Instruct"
    ):
        print("Инициализация LLM...")
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,  # или bfloat16 если карта RTX 30xx/40xx
            bnb_4bit_quant_type="nf4"
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            quantization_config=bnb_config,
            device_map=device_map
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        print(f"Модель загружена на устройство: {self.model.device}")

    def debug(self, prompt):
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        messages = [
            {"role": "user", "content": prompt}
        ]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)

        # --- Передача **inputs (включая attention_mask) ---
        self.model.generate(
            **inputs,
            streamer=self.streamer,
            max_new_tokens=512,
            pad_token_id=self.tokenizer.pad_token_id
        )

    def inference(self, query, context, history):
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        messages = [
            {"role": "user", "content": context_prompt(history, context, query)}
        ]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.tokenizer(text, return_tensors="pt").to(self.model.device)

        # --- Передача **inputs (включая attention_mask) ---
        generated_ids = self.model.generate(
            **inputs,
            max_new_tokens=1000,
            pad_token_id=self.tokenizer.pad_token_id  # Явно указываем, когда остановиться
        )

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response[response.find('assistant\nA: ')+len('assistant\nA: '):]
