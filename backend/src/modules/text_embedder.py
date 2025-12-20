from transformers import AutoTokenizer, AutoModel
import torch
import os

class TextEmbedder:
    def __init__(self, model_name='intfloat/multilingual-e5-large', device='cpu'):
        self.device = device
        if self.device == 'cpu':
            os.environ['OMP_NUM_THREADS'] = str(os.cpu_count() or 4)
            os.environ['MKL_NUM_THREADS'] = str(os.cpu_count() or 4)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()
        if self.device == 'cpu':
            torch.set_num_threads(os.cpu_count() or 4)

    def get_embeddings(self, texts):
        with torch.no_grad():
            inputs = self.tokenizer(texts, padding=True, truncation=True,
                                  max_length=512, return_tensors='pt')

            outputs = self.model(**inputs)

            embeddings = outputs.last_hidden_state[:, 0, :]
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

            return embeddings.numpy().astype('float32')

    def embed_documents(self, texts):
        batch_size = 8  # <-- Если снова будет ошибка памяти, уменьши до 4 или 2
        all_embeddings = []

        # Цикл обработки по кусочкам (батчам)
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i: i + batch_size]

            # 1. Токенизация батча
            inputs = self.tokenizer(batch_texts, return_tensors="pt", padding=True, truncation=True, max_length=512)

            # 2. Перенос на GPU
            if self.device == 'cuda':
                inputs = {key: value.to(self.device) for key, value in inputs.items()}

            # 3. Прогон через модель без сохранения градиентов (экономит память)
            with torch.no_grad():
                outputs = self.model(**inputs)

            # 4. Получение эмбеддингов (среднее по токенам)
            # Внимание: для некоторых моделей лучше использовать inputs['attention_mask'] для правильного усреднения
            # Но для простоты пока оставим так, или используем CLS токен outputs.last_hidden_state[:, 0, :]
            embeddings = outputs.last_hidden_state.mean(dim=1)

            # 5. Переносим на CPU и добавляем в общий список
            all_embeddings.extend(embeddings.cpu().tolist())

            # 6. Очищаем кэш GPU (опционально, но полезно при малом объеме памяти)
            del inputs, outputs, embeddings
            if self.device == 'cuda':
                torch.cuda.empty_cache()

        return all_embeddings

    def embed_query(self, text):
        with torch.no_grad():
            # 1. Токенизация
            inputs = self.tokenizer(text, padding=True, truncation=True,
                                    max_length=512, return_tensors='pt')

            # 2. Перенос входных данных на GPU
            if self.device == 'cuda':
                inputs = {key: value.to(self.device) for key, value in inputs.items()}

            # 3. Прогон через модель
            outputs = self.model(**inputs)

            # 4. Получение эмбеддинга
            # Внимание: Убедись, что метод здесь (CLS token или Mean Pooling)
            # совпадает с тем, что в embed_documents.
            # В твоем примере сейчас стоит CLS (первый токен):
            embeddings = outputs.last_hidden_state[:, 0, :]

            # 5. Нормализация (хорошо для поиска по косинусному сходству)
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

            # 6. !!! ИСПРАВЛЕНИЕ: Переносим на CPU перед конвертацией в список
            # .numpy() не работает с GPU-тензорами напрямую
            return embeddings.cpu().tolist()[0]