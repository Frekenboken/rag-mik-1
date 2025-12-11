import faiss
import re
import string
from natasha import MorphVocab

from src.modules.rerank import Rerank
from src.modules.text_embedder import TextEmbedder
from difflib import SequenceMatcher
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag

import nltk
# Скачайте все необходимые данные
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger_rus')

# Для русского языка также может понадобиться
# nltk.download('rslp')  # для стемминга


class SemanticSearch:
    def __init__(self, vector_db: faiss.swigfaiss_avx2.IndexFlatIP, chunks, rerank: Rerank, embedding: TextEmbedder):
        self.vector_db = vector_db
        self.chunks = chunks
        self.rerank = rerank
        self.embedding = embedding
        self.morph = MorphVocab()

    def search_debuging(self, query_text, k=3):
        relevance = self.rerank.reranking_and_format(
            self.vector_db.search(self.embedding.get_embeddings([query_text.lower()]), k)[1][0],
            query_text.lower(),
            self.chunks
            )
        print(f"🔍 Запрос: '{query_text}'\n")
        for i, (similarity, idx) in enumerate(relevance):
            print(f"{i+1}.")
            print(f"{self.chunks[idx][0]}")
            print(f"   📊 Сходство: {similarity:.4f}\n")
            print("=" * 80)

    def search(self, query_text, k=3):
         relevance = self.rerank.reranking_and_format(
            self.vector_db.search(self.embedding.get_embeddings([query_text.lower()]), k)[1][0],
            query_text.lower(),
            self.chunks
            )
         # return [self.chunks[idx] for similarity, idx in filter(lambda x: x[0] > 0.17, relevance)]
         return [self.chunks[idx] for similarity, idx in relevance if similarity > 0.17]

    def extract_keywords(self, text):

        # Удаляем знаки препинания с помощью string.punctuation
        cleaned_text = ''.join(char for char in text if char not in string.punctuation)

        # Токенизация слов
        words = word_tokenize(cleaned_text)

        # Загрузить список стоп-слов NLTK
        stop_words = set(stopwords.words('russian'))

        # Отфильтровать стоп-слова
        filtered_words = [word for word in words if word.lower() not in stop_words]

        # Лемматизируем каждое слово
        lemmatized_words = [self.morph.parse(word)[0].normal_form for word in filtered_words]

        tagged_lemmatized_words = pos_tag(lemmatized_words, lang='rus')

        return [i[0] for i in filter(lambda x: x[1] == 'S', tagged_lemmatized_words)]
        #return tagged_lemmatized_words

    def calculate_similarity(self, answer: str, expected: str) -> float:
        """
        Расчет схожести ответа с эталонным
        """
        # Нормализация текста
        answer = answer.lower().strip()
        expected = expected.lower().strip()

        # Извлечение чисел для сравнения
        numbers_answer = set(re.findall(r'\d+(?:\.\d+)?', answer))
        numbers_expected = set(re.findall(r'\d+(?:\.\d+)?', expected))

        # Если есть числа, проверяем их совпадение
        if numbers_expected:
            numbers_match = len(numbers_answer & numbers_expected) / len(numbers_expected)
        else:
            numbers_match = 1.0

        # Текстовое сходство
        text_similarity = SequenceMatcher(None, answer, expected).ratio()

        # Проверка ключевых слов
        keywords = self.extract_keywords(expected)
        if keywords:
            keywords_found = sum(1 for kw in keywords if kw in answer) / len(keywords)
        else:
            keywords_found = 1.0

        # Комбинированная оценка
        final_score = (numbers_match * 0.4 + text_similarity * 0.3 + keywords_found * 0.3)

        return final_score