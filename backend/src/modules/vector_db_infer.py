import chromadb
import pickle
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from text_embedder import TextEmbedder
from langchain_community.vectorstores import Chroma

#with open('src/static/docs/' + '../' + 'all_chunks.bin', 'rb') as all_chunks: all_chunks = pickle.load(all_chunks)
#'src/static/docs/'
print('starting')
with open('../../src/static/chunks_with_meta.bin', 'rb') as chunks_with_meta: chunks_with_meta = pickle.load(chunks_with_meta)
chunks_with_meta = [Document(page_content=chunk, metadata={"id": f'{doc} Раздел {j}.{i}'}) for chunk, i, j, doc in chunks_with_meta]

chroma_client = chromadb.Client()
print('chroma client loaded')
embedding_function = TextEmbedder()
print('embedding model loaded')
try:
    vectorstore = Chroma(
        persist_directory='../../src/vector_db/',
        embedding_function=embedding_function
    )
except FileNotFoundError:
    print('creating db...')
    vectorstore = Chroma.from_documents(
        documents=chunks_with_meta,
        embedding=embedding_function,
        collection_name='vect_db',
        client=chroma_client,
        persist_directory='../../src/vector_db/'
    )
print('vector db initialised')
# Create dense retriever
dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
# Create sparse retriever
sparse_retriever = BM25Retriever.from_documents(chunks_with_meta, k=10)
print('retrievers loaded')
# Custom hybrid search function (as opposed to using LangChain EnsembleRetriever)
def hybrid_search(query, k=10, dense_weight=0.5, sparse_weight=0.5):
    # Step 1: Retrieve the top-k documents from both dense search and sparse search.
    dense_docs = dense_retriever.invoke(query)[:k]
    dense_doc_ids = [doc.metadata['id'] for doc in dense_docs]
    print("\nCompare IDs:")
    print("dense IDs: ", dense_doc_ids)
    sparse_docs = sparse_retriever.invoke(query)[:k]
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
        combined_reciprocal_ranks[doc_id] = dense_weight * dense_reciprocal_ranks[doc_id] + sparse_weight * sparse_reciprocal_ranks[doc_id]

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
    return sorted_docs[:k]


print('search initialised')
print('_'*80)
while True:
    try:
        t = hybrid_search(input())
        for i in t:
            print(i.page_content)
            print(i.metadata)
        print('_'*80)
    except KeyboardInterrupt:
        print('programm ended')


'''chroma_client = chromadb.Client()

vector_db = chroma_client.create_collection(name='zov')

for chunk, i, j, doc in chunks_with_meta:
    vector_db.add(
        ids=[f'{doc} Раздел {j}.{i}'],
        documents=[chunk]
    )

while True:
    try:
        print(vector_db.query(
            query_texts=[input()]
        ))
    except KeyboardInterrupt:
        print('programm ended')'''