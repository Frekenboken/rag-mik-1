from backend.src.modules.LLM import *
from backend.src.modules.Rerank import *
from backend.src.modules.TextEmbedder import *
from backend.src.modules.SemanticSearch import *
from backend.src.modules.DocumentTools import *


class RAG:
    def __init__(
            self,
            rerank: Rerank,
            llm: LLM,
            embedder: TextEmbedder,
            semantic_search: SemanticSearch,
            chunker: Chunker,
            documents_loader: DocumentsLoader,
            path
    ):
        self.path = path
        print('initialising RAG system...')
        self.rerank = rerank()
        self.llm = llm()
        self.embedder = embedder()
        self.semantic_search = semantic_search()
        self.chunker = chunker()
        self.documents_loader = documents_loader()
        print('RAG system initialised')

    def documents_load(self):
