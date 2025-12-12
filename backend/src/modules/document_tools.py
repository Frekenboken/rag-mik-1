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
        self.chunk_size = 300
        self.chunk_overlap = np.round(self.chunk_size * 0.3, 0)
        print(f"chunk_size: {self.chunk_size}, chunk_overlap: {self.chunk_overlap}")

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", "! ", "? "]
        )

    def standard_seperate(self, docs):
        print(f"chunk_size: {self.chunk_size}, chunk_overlap: {self.chunk_overlap}")
        chunked_docs = [self.splitter.split_text(str(doc.page_content)) for doc in docs]
        print(f"docs split into {[len(chunked_doc) for chunked_doc in chunked_docs]} chunks.")
        all_chunks = [chunk.lower() for chunked_doc in chunked_docs for chunk in chunked_doc]
        print(all_chunks[:10])
        chunks_with_index = [(chunk, i) for i, chunked_doc in enumerate(chunked_docs) for chunk in chunked_doc]
        print(chunks_with_index[:10])

        return [all_chunks, chunks_with_index]

    @staticmethod
    def advanced_separate(docs):
        chunks_with_meta = [
            (podglava, index_podglava, index_glava,
             doc.metadata['source'][doc.metadata['source'].rfind('\\') + 1:doc.metadata['source'].rfind('.')])
            for doc in docs
            for index_glava, glava in enumerate(re.split(r'\n##\s', doc.page_content), 1)
            for index_podglava, podglava in enumerate(re.split(r'\n###\s', glava), 1)
            if podglava.strip() and not re.match(r'\*\*[\w\s]*\*\*\n', podglava)
        ]

        all_chunks = [i[0] for i in chunks_with_meta[1:]]
        return [all_chunks, chunks_with_meta]

    def advanced_separate_on_chunks(self, docs):
        podglavas_with_meta = [
            (podglava, index_podglava, index_glava,
             doc.metadata['source'][doc.metadata['source'].rfind('\\') + 1:doc.metadata['source'].rfind('.')])
            for doc in docs
            for index_glava, glava in enumerate(re.split(r'\n##\s', doc.page_content), 1)
            for index_podglava, podglava in enumerate(re.split(r'\n###\s', glava), 1)
            if podglava.strip() and not re.match(r'\*\*[\w\s]*\*\*\n$', podglava)
        ][1:]

        all_chunks = [
            chunk
            for podglava, i, j, name in podglavas_with_meta
            for chunk in self.splitter.split_text(podglava)
        ]

        podglavas_with_meta_for_index = [
            (podglava, i, j, name)
            for podglava, i, j, name in podglavas_with_meta
            for chunk in self.splitter.split_text(podglava)]

        return [all_chunks, podglavas_with_meta_for_index]

    def questions_process(self, questionss):
        processed_questions = []
        ind = 1
        for questions in questionss:
            for blocks in re.split(r'\n##\s', questions.page_content[questions.page_content.find('##'):questions.page_content.rfind('\n## ')]):
                for question in enumerate(re.split(r'\n###\s', blocks)):
                    if question[0] == 0:
                        c = re.search(r'.*:', question[1])
                        category = question[1][c.end()+1:question[1].rfind('\n')]
                        continue
                    q = re.search(r'\*\*Q:\*\*\s', question[1])
                    a = re.search(r'\*\*A:\*\*\s', question[1])
                    i = re.search(r'\*\*Источник:\*\*\s', question[1])
                    quest = question[1][q.end():a.start()-1]
                    answer = question[1][a.end():i.start()-1]
                    processed_questions.append((ind, category, quest, answer))
                    ind+=1
        print(f'{ind-1} вопросов загружено')
        return processed_questions