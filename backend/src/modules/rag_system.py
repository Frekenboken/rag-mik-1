from src.modules.llm import LLM, context_prompt
from src.modules.rerank import Rerank
from src.modules.text_embedder import TextEmbedder
from src.modules.semantic_search import SemanticSearch
from src.modules.document_tools import DocumentsLoader, Chunker
from src.modules.rag_exeptions import DimensionMismatch, ModuleLoadingFailure
from langchain_community.document_loaders import DirectoryLoader, TextLoader
import faiss
import pickle
import numpy as np
import time
import json


class RAG:
    def __init__(
            self,
            question_path,
            docs_path,
            vdb_path,
            file_type
    ):
        self.question_path = question_path
        self.docs_path = docs_path
        self.vdb_path = vdb_path
        self.file_type = file_type
        print('Инициализация RAG системы...')
        try:
            self.rerank = Rerank()
        except:
            raise ModuleLoadingFailure(Rerank)
        try:
            self.llm = LLM(context_prompt)
        except:
            raise ModuleLoadingFailure(LLM)
        try:
            self.embedder = TextEmbedder()
        except:
            raise ModuleLoadingFailure(TextEmbedder)
        try:
            self.chunker = Chunker()
        except:
            raise ModuleLoadingFailure(Chunker)
        try:
            self.documents_loader = DocumentsLoader(DirectoryLoader, TextLoader, docs_path, file_type)
            self.questions_loader = DocumentsLoader(DirectoryLoader, TextLoader, question_path, file_type)
        except:
            raise ModuleLoadingFailure(DocumentsLoader)

        print('Поиск обработанных документов...')
        try:
            with open(docs_path + '../' + 'docs.bin', 'rb') as docs:
                self.docs = pickle.load(docs)
            with open(docs_path + '../' + 'all_chunks.bin', 'rb') as all_chunks:
                self.all_chunks = pickle.load(all_chunks)
            with open(docs_path + '../' + 'chunks_with_meta.bin', 'rb') as chunks_with_meta:
                self.chunks_with_meta = pickle.load(chunks_with_meta)
            with open(question_path + '../' + 'processed_questions.bin', 'rb') as processed_questions:
                self.processed_questions = pickle.load(processed_questions)
            print('Документы найдены!')
        except FileNotFoundError:
            print('Обработанные документы не найдены\nОбработка документов...')
            self.docs = self.documents_loader.process_docs()
            self.questions = self.questions_loader.process_docs()
            self.all_chunks, self.chunks_with_meta = self.chunker.advanced_separate_on_chunks(self.docs)
            self.processed_questions = self.chunker.questions_process(self.questions)
            with open(docs_path + '../' + 'docs.bin', 'wb') as docs:
                pickle.dump(self.docs, docs)
            with open(docs_path + '../' + 'all_chunks.bin', 'wb') as all_chunks:
                pickle.dump(self.all_chunks, all_chunks)
            with open(docs_path + '../' + 'chunks_with_meta.bin', 'wb') as chunks_with_meta:
                pickle.dump(self.chunks_with_meta, chunks_with_meta)
            with open(question_path + '../' + 'questions.bin', 'wb') as questions:
                pickle.dump(self.questions, questions)
            print('Завершено!')

        print("Поиск эмбеддингов...")
        try:
            embeddings = np.load(self.vdb_path + 'embeddings.npy')
            print("Эмбеддинги найдены!")
        except:
            print("Эмбеддинги не найдены\nСоздание эмбеддингов...")
            embeddings = self.embedder.get_embeddings(self.all_chunks)
            np.save(self.vdb_path + 'embeddings.npy', embeddings, allow_pickle=False, fix_imports=False)
            print("Завершено!")

        dimension = embeddings.shape[1]

        print("Поиск индекса...")
        try:
            self.index = faiss.read_index(self.vdb_path + "index.index")
            print("Индекс найден!")
        except:
            print("Индекс не найден\nСоздаем индекс...")
            self.index = faiss.IndexFlatIP(dimension)
            self.index.add(embeddings)
            faiss.write_index(self.index, self.vdb_path + "index.index")
            print("Завершено!")

        if self.index.d == dimension:
            print(f"Размерность индекса и эмбеддингов: {dimension}")
        else:
            raise DimensionMismatch(dimension, self.index.d)

        try:
            self.semantic_search = SemanticSearch(self.index, self.chunks_with_meta, self.rerank, self.embedder)
        except:
            raise ModuleLoadingFailure(SemanticSearch)
        print('RAG система инициализированна')

    def interaction(self, query, history, k=3, d=2):
        context = set(self.semantic_search.search(query, k=k)[:d])
        response = self.llm.context_response(history, ''.join([chunk[0] for chunk in context]), query)
        return response.content + ('\n\nИсточники: ' + ', '.join(
            [f'{source}, Раздел {x_topic}.{s_topic}' for chunk, s_topic, x_topic, source in
             context]) if context != [] else '')

    def semsearch_debug(self, query, k):
        self.semantic_search.search_debuging(query, k=k)

    def keyword_extraction_debug(self, query):
        print(self.semantic_search.extract_keywords(query))

    def one_ans_rate(self, quest):
        query = quest[2]
        category = quest[1]
        ind = quest[0]
        expected_answer = quest[3]
        start_time = time.time()
        actual_answer = self.interaction(query, '')
        response_time = time.time() - start_time
        # Расчет схожести
        similarity = self.semantic_search.calculate_similarity(
            actual_answer,
            expected_answer
        )

        # Определение баллов
        if similarity >= 0.8:
            score = 0.8  # Полностью правильный
            status = "✅ Правильно"
        elif similarity >= 0.5:
            score = 0.4  # Частично правильный
            status = "⚠️ Частично"
        else:
            score = 0  # Неправильный
            status = "❌ Неправильно"

        # Проверка источников
        has_sources = 'Источники' in actual_answer

        return {
            'question_id': ind,
            'category': category,
            'question': query,
            'expected_answer': expected_answer,
            'received_answer': actual_answer,
            'similarity': similarity,
            'score': score,
            'status': status,
            'has_sources': has_sources,
            'confidence': 100,
            'response_time': response_time,
            'error': 'everytime'
        }, actual_answer

    def rag_rating(self):
        results = []
        print("\n" + "=" * 60)
        print("🚀 ЗАПУСК ОЦЕНКИ RAG-СИСТЕМЫ МИК-1")
        print("=" * 60 + "\n")

        total_score = 0
        category_scores = {}

        # Тестирование каждого вопроса
        for i, test_q in enumerate(self.processed_questions, 1):
            query = test_q[2]
            category = test_q[1]
            print(f"📝 Тест {i}/{len(self.processed_questions)}: {query[:50]}...")

            result, res = self.one_ans_rate(test_q)
            print(f"Ответ: {res[:100]}")

            results.append(result)
            total_score += result['score']

            if category not in category_scores:
                category_scores[category] = {'total': 0, 'earned': 0, 'count': 0}
            category_scores[category]['total'] += 0.8
            category_scores[category]['earned'] += result['score']
            category_scores[category]['count'] += 1

            print(f"   {result['status']} | Схожесть: {result['similarity']:.2%} | Баллы: {result['score']}")

            # Небольшая задержка между запросами
            time.sleep(0.5)

        max_possible = len(self.processed_questions) * 0.8

        # Расчет процентов по категориям
        category_percentages = {}
        for cat, scores in category_scores.items():
            percentage = (scores['earned'] / scores['total']) * 100 if scores['total'] > 0 else 0
            category_percentages[cat] = {
                'percentage': percentage,
                'earned': scores['earned'],
                'total': scores['total'],
                'count': scores['count']
            }

            # Дополнительные метрики
            correct_answers = sum(1 for r in results if r['score'] == 0.8)
            partial_answers = sum(1 for r in results if r['score'] == 0.4)
            wrong_answers = sum(1 for r in results if r['score'] == 0)

            avg_confidence = sum(r['confidence'] for r in results) / len(results) if results else 0
            avg_response_time = sum(r['response_time'] for r in results) / len(results) if results else 0

            final_results = {
                'total_score': total_score,
                'max_possible': max_possible,
                'percentage': (total_score / max_possible * 100) if max_possible > 0 else 0,
                'questions_tested': len(self.processed_questions),
                'correct_answers': correct_answers,
                'partial_answers': partial_answers,
                'wrong_answers': wrong_answers,
                'category_scores': category_percentages,
                'avg_confidence': avg_confidence,
                'avg_response_time': avg_response_time,
                'detailed_results': results
            }
            print("\n" + "=" * 60)
            print("📊 ОТЧЕТ ОБ ОЦЕНКЕ RAG-СИСТЕМЫ")
            print("=" * 60 + "\n")

            # Основные метрики
            print("🎯 ИТОГОВЫЕ БАЛЛЫ:")
            print(f"   Набрано баллов: {final_results['total_score']:.1f} / {final_results['max_possible']:.1f}")
            print(f"   Процент: {final_results['percentage']:.1f}%")
            print(f"   Оценка: ", end='')
            if final_results['percentage'] >= 90:
                print("🏆 Отлично (A)")
            elif final_results['percentage'] >= 80:
                print("👍 Хорошо (B)")
            elif final_results['percentage'] >= 70:
                print("✔️ Удовлетворительно (C)")
            elif final_results['percentage'] >= 60:
                print("⚠️ Достаточно (D)")
            else:
                print("❌ Неудовлетворительно (F)")
            print()

            # Статистика ответов
            print("📈 СТАТИСТИКА ОТВЕТОВ:")
            print(
                f"   ✅ Правильных: {final_results['correct_answers']} ({final_results['correct_answers'] / final_results['questions_tested'] * 100:.1f}%)")
            print(
                f"   ⚠️ Частичных: {final_results['partial_answers']} ({final_results['partial_answers'] / final_results['questions_tested'] * 100:.1f}%)")
            print(
                f"   ❌ Неправильных: {final_results['wrong_answers']} ({final_results['wrong_answers'] / final_results['questions_tested'] * 100:.1f}%)")
            print()

            # По категориям
            print("📂 ПО КАТЕГОРИЯМ:")
            for cat, scores in final_results['category_scores'].items():
                print(f"   {cat}: {scores['percentage']:.1f}% ({scores['earned']:.1f}/{scores['total']:.1f} баллов)")
            print()
            # Производительность
            print("⚡ ПРОИЗВОДИТЕЛЬНОСТЬ:")
            print(f"   Средняя уверенность: {final_results['avg_confidence']:.2%}")
            print(f"   Среднее время ответа: {final_results['avg_response_time']:.2f} сек")
            print()

            # Критерии оценки по ТЗ
            print("✅ СООТВЕТСТВИЕ КРИТЕРИЯМ:")
            criteria_met = []
            criteria_not_met = []

            # Проверка критериев
            if final_results['category_scores'][list(final_results['category_scores'].keys())[0]]['percentage'] >= 90:
                criteria_met.append("✓ Простые вопросы ≥ 90%")
            else:
                criteria_not_met.append("✗ Простые вопросы < 90%")

            if final_results['category_scores'][final_results['category_scores'].keys()[0]]['percentage'] >= 80:
                criteria_met.append("✓ Средние вопросы ≥ 80%")
            else:
                criteria_not_met.append("✗ Средние вопросы < 80%")

            if final_results['category_scores'][final_results['category_scores'].keys()[0]]['percentage'] >= 60:
                criteria_met.append("✓ Сложные вопросы ≥ 60%")
            else:
                criteria_not_met.append("✗ Сложные вопросы < 60%")

            if final_results['percentage'] >= 75:
                criteria_met.append("✓ Общая точность ≥ 75%")
            else:
                criteria_not_met.append("✗ Общая точность < 75%")

            for criterion in criteria_met:
                print(f"   {criterion}")
            for criterion in criteria_not_met:
                print(f"   {criterion}")

            print("\n" + "=" * 60)

        compact_results = {k: v for k, v in final_results.items() if k != 'detailed_results'}

        with open('src/rag_evaluation/evaluation_results.json', 'w', encoding='utf-8') as f:
            json.dump(compact_results, f, ensure_ascii=False, indent=2)

        print(f"\n💾 Результаты сохранены в evaluation_results.json")

        # Сохранение детального отчета
        with open('src/rag_evaluation/evaluation_detailed.txt', 'w', encoding='utf-8') as f:
            f.write("ДЕТАЛЬНЫЙ ОТЧЕТ ОЦЕНКИ RAG-СИСТЕМЫ МИК-1\n")
            f.write("=" * 60 + "\n\n")

            for result in final_results['detailed_results']:
                f.write(f"Вопрос {result['question_id']}: {result['question']}\n")
                f.write(f"Ожидаемый ответ: {result['expected_answer']}\n")
                f.write(f"Полученный ответ: {result['received_answer']}\n")
                f.write(f"Статус: {result['status']} | Схожесть: {result['similarity']:.2%}\n")
                f.write("-" * 60 + "\n\n")

        print(f"📄 Детальный отчет сохранен в evaluation_detailed.txt")
