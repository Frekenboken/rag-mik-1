from transformers import AutoModelForSequenceClassification

class Rerank:
    def __init__(self, model_name='jinaai/jina-reranker-v2-base-multilingual'):
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name, torch_dtype="auto", trust_remote_code=True)
        self.model.to('cpu')
        self.model.eval()

    def reranking_and_format(self, chunk_indices, query_text, all_chunks):
        scores = self.model.compute_score([[query_text, all_chunks[i]] for i in chunk_indices], max_length=1024)
        return sorted(zip(scores, chunk_indices), key=lambda x: x[0], reverse=True)