
import re
import string
from natasha import MorphVocab
from langchain_community.retrievers import BM25Retriever

from src.modules.rerank import Rerank
from src.modules.text_embedder import TextEmbedder
from difflib import SequenceMatcher
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag

import nltk

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger_rus')


class SemanticSearch:
    def __init__(self, vectorstore, chunks, rerank: Rerank, embedding: TextEmbedder):
        self.dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
        self.sparse_retriever = BM25Retriever.from_documents(chunks, k=10, preprocess_func=lambda x: x.lower())
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
         return [self.chunks[idx] for similarity, idx in relevance]

    def new_search_debuging(self, query, k=3, dense_weight=0.5, sparse_weight=0.5):
        dense_docs = self.dense_retriever.invoke(query.lower())[:k]
        dense_doc_ids = [doc.metadata['id'] for doc in dense_docs]
        print("\nCompare IDs:")
        print("dense IDs: ", dense_doc_ids)
        sparse_docs = self.sparse_retriever.invoke(query.lower())[:k]
        sparse_doc_ids = [doc.metadata['id'] for doc in sparse_docs]
        print("sparse IDs: ", sparse_doc_ids)

        # Combine the document IDs and remove duplicates
        all_doc_ids = list(set(dense_doc_ids + sparse_doc_ids))

        # Create dictionaries to store the reciprocal ranks
        dense_reciprocal_ranks = {doc_id: 0.0 for doc_id in all_doc_ids}
        sparse_reciprocal_ranks = {doc_id: 0.0 for doc_id in all_doc_ids}

        # Step 2: Calculate the reciprocal rank for each document in dense and sparse search results.
        for i, doc_id in enumerate(dense_doc_ids):
            dense_reciprocal_ranks[doc_id] = 1.0 / (i + 1)

        for i, doc_id in enumerate(sparse_doc_ids):
            sparse_reciprocal_ranks[doc_id] = 1.0 / (i + 1)

        # Step 3: Sum the reciprocal ranks for each document.
        combined_reciprocal_ranks = {doc_id: 0.0 for doc_id in all_doc_ids}
        for doc_id in all_doc_ids:
            combined_reciprocal_ranks[doc_id] = dense_weight * dense_reciprocal_ranks[doc_id] + sparse_weight * \
                                                sparse_reciprocal_ranks[doc_id]

        # Step 4: Sort the documents based on their combined reciprocal rank scores.
        sorted_doc_ids = sorted(all_doc_ids, key=lambda doc_id: combined_reciprocal_ranks[doc_id], reverse=True)

        # Step 5: Retrieve the documents based on the sorted document IDs.
        sorted_docs = []
        all_docs = dense_docs + sparse_docs
        for doc_id in sorted_doc_ids:
            matching_docs = [doc for doc in all_docs if doc.metadata['id'] == doc_id]
            if matching_docs:
                doc = matching_docs[0]
                doc.metadata['score'] = combined_reciprocal_ranks[doc_id]
                doc.metadata['rank'] = sorted_doc_ids.index(doc_id) + 1
                if len(matching_docs) > 1:
                    doc.metadata['retriever'] = 'both'
                elif doc in dense_docs:
                    doc.metadata['retriever'] = 'dense'
                else:
                    doc.metadata['retriever'] = 'sparse'
                sorted_docs.append(doc)

        # Step 7: Return the final ranked and sorted list, truncated by the top-k parameter
        print(f"🔍 Запрос: '{query}'\n")
        for num, i in enumerate(sorted_docs[:k]):
            print(f'{num+1}. {i.metadata}')
            print(i.page_content)
            print("=" * 80)

    def new_search(self, query, k=3, dense_weight=0.5, sparse_weight=0.5):
        dense_docs = self.dense_retriever.invoke(query.lower())[:k]
        dense_doc_ids = [doc.metadata['id'] for doc in dense_docs]
        sparse_docs = self.sparse_retriever.invoke(query.lower())[:k]
        sparse_doc_ids = [doc.metadata['id'] for doc in sparse_docs]

        # Combine the document IDs and remove duplicates
        all_doc_ids = list(set(dense_doc_ids + sparse_doc_ids))

        # Create dictionaries to store the reciprocal ranks
        dense_reciprocal_ranks = {doc_id: 0.0 for doc_id in all_doc_ids}
        sparse_reciprocal_ranks = {doc_id: 0.0 for doc_id in all_doc_ids}

        # Step 2: Calculate the reciprocal rank for each document in dense and sparse search results.
        for i, doc_id in enumerate(dense_doc_ids):
            dense_reciprocal_ranks[doc_id] = 1.0 / (i + 1)

        for i, doc_id in enumerate(sparse_doc_ids):
            sparse_reciprocal_ranks[doc_id] = 1.0 / (i + 1)

        # Step 3: Sum the reciprocal ranks for each document.
        combined_reciprocal_ranks = {doc_id: 0.0 for doc_id in all_doc_ids}
        for doc_id in all_doc_ids:
            combined_reciprocal_ranks[doc_id] = dense_weight * dense_reciprocal_ranks[doc_id] + sparse_weight * \
                                                sparse_reciprocal_ranks[doc_id]

        # Step 4: Sort the documents based on their combined reciprocal rank scores.
        sorted_doc_ids = sorted(all_doc_ids, key=lambda doc_id: combined_reciprocal_ranks[doc_id], reverse=True)

        # Step 5: Retrieve the documents based on the sorted document IDs.
        sorted_docs = []
        all_docs = dense_docs + sparse_docs
        for doc_id in sorted_doc_ids:
            matching_docs = [doc for doc in all_docs if doc.metadata['id'] == doc_id]
            if matching_docs:
                doc = matching_docs[0]
                doc.metadata['score'] = combined_reciprocal_ranks[doc_id]
                doc.metadata['rank'] = sorted_doc_ids.index(doc_id) + 1
                if len(matching_docs) > 1:
                    doc.metadata['retriever'] = 'both'
                elif doc in dense_docs:
                    doc.metadata['retriever'] = 'dense'
                else:
                    doc.metadata['retriever'] = 'sparse'
                sorted_docs.append(doc)
        return sorted_docs[:k]


    def extract_keywords(self, text):

        cleaned_text = ''.join(char for char in text if char not in string.punctuation)

        words = word_tokenize(cleaned_text)

        stop_words = set(stopwords.words('russian'))

        filtered_words = [word for word in words if word.lower() not in stop_words]

        lemmatized_words = [self.morph.parse(word)[0].normal_form for word in filtered_words]

        tagged_lemmatized_words = pos_tag(lemmatized_words, lang='rus')

        return [i[0] for i in filter(lambda x: x[1] in ('S', 'NONLEX', 'INTJ'), tagged_lemmatized_words)]


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
            keywords_found = sum(1 for kw in keywords if kw in self.extract_keywords(answer)) / len(keywords)
        else:
            keywords_found = 1.0

        # Комбинированная оценка
        final_score = (numbers_match * 0.45 + text_similarity * 0.325 + keywords_found * 0.225)

        return final_score

