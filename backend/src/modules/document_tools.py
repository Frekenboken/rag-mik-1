from langchain_community.document_loaders import DirectoryLoader, TextLoader
import re
import numpy as np
from langchain_text_splitters import RecursiveCharacterTextSplitter


class DocumentsLoader:
    def __init__(self, loader: DirectoryLoader, text_loader: TextLoader, path, file_type):
        self.path = path
        self.global_pattern = file_type
        self.loader = loader(path=self.path, glob=self.global_pattern, loader_cls=text_loader)

    def process_docs(self):
        return self.loader.load()


class Chunker:
    def __init__(self):
        self.CHUNK_SIZE = 900
        self.chunk_overlap = np.round(self.CHUNK_SIZE * 0.30, 0)
        print(f"chunk_size: {self.CHUNK_SIZE}, chunk_overlap: {self.chunk_overlap}")

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.CHUNK_SIZE,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", "! ", "? "]
        )

    def standard_seperate(self, docs, chunk_size=900):
        chunk_overlap = np.round(chunk_size * 0.30, 0)
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", "! ", "? "]
        )
        print(f"chunk_size: {chunk_size}, chunk_overlap: {chunk_overlap}")
        chunked_docs = [splitter.split_text(str(doc.page_content)) for doc in docs]
        print(f"docs split into {[len(chunked_doc) for chunked_doc in chunked_docs]} chunks.")
        all_chunks = [chunk.lower() for chunked_doc in chunked_docs for chunk in chunked_doc]
        print(all_chunks[:10])
        chunks_with_index = [(chunk, i) for i, chunked_doc in enumerate(chunked_docs) for chunk in chunked_doc]
        print(chunks_with_index[:10])

        return [all_chunks, chunks_with_index]

    @staticmethod
    def advanced_separate(docs):
        chunks_with_meta = [
            (s_topic, s_ind, x_ind,
             doc.metadata['source'][doc.metadata['source'].rfind('/') + 1:doc.metadata['source'].rfind('.')])
            for doc in docs
            for x_ind, x_topic in enumerate(re.compile(r'(?!#)*##\s+').split(doc.page_content), 1)
            for s_ind, s_topic in enumerate(re.compile(r'(?!#)*###\s+').split(x_topic), 1)
        ]
        all_chunks = [i[0] for i in chunks_with_meta]
        return [all_chunks, chunks_with_meta]
