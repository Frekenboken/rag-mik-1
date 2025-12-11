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


class RAG:
    def __init__(
            self,
            docs_path,
            vdb_path,
            file_type
    ):
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
            print('Документы найдены!')
        except:
            print('Обработанные документы не найдены\nОбработка документов...')
            self.docs = self.documents_loader.process_docs()
            self.all_chunks, self.chunks_with_meta = self.chunker.advanced_separate(self.docs)
            with open(docs_path + '../' + 'docs.bin', 'wb') as docs:
                pickle.dump(self.docs, docs)
            with open(docs_path + '../' + 'all_chunks.bin', 'wb') as all_chunks:
                pickle.dump(self.all_chunks, all_chunks)
            with open(docs_path + '../' + 'chunks_with_meta.bin', 'wb') as chunks_with_meta:
                pickle.dump(self.chunks_with_meta, chunks_with_meta)
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

    def interaction(self, query, history, k=3):
        context = self.semantic_search.search(query, k=k)
        response = self.llm.context_response(history, ''.join([chunk[0] for chunk in context]), query)
        return response.content + ('\n\nИсточники: ' + ', '.join(
            [f'{source}, Раздел {x_topic}.{s_topic}' for chunk, s_topic, x_topic, source in
             context]) if context != [] else '')

    def semsearch_debug(self, query, k):
        self.semantic_search.search_debuging(query, k=k)

    def rag_rating(self):
        pass
