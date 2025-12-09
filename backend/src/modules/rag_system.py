from src.modules.llm import RussianLLM
from src.modules.rerank import Rerank
from src.modules.text_embedder import TextEmbedder
from src.modules.semantic_search import SemanticSearch
from src.modules.document_tools import DocumentsLoader, Chunker


class RAG:
    def __init__(
            self,
            rerank: Rerank,
            llm: RussianLLM,
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
        pass