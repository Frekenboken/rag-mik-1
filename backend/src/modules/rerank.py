import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import os


class Rerank:
    def __init__(self, model_name='jinaai/jina-reranker-v2-base-multilingual'):
        # Устанавливаем переменные окружения для оптимизации CPU
        os.environ['OMP_NUM_THREADS'] = str(os.cpu_count() or 4)
        os.environ['MKL_NUM_THREADS'] = str(os.cpu_count() or 4)

        self.device = 'cpu'

        # Для CPU используем float32
        self.model = AutoModelForSequenceClassification.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            trust_remote_code=True
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

        # Оптимизация torch для CPU
        torch.set_num_threads(os.cpu_count() or 4)

    def reranking_and_format(self, chunk_indices, query_text, all_chunks, batch_size=8):
        # Для CPU используем меньший размер батча
        pairs = [[query_text, all_chunks[i][0].lower()] for i in chunk_indices]

        scores = []

        for i in range(0, len(pairs), batch_size):
            batch_pairs = pairs[i:i + batch_size]

            features = self.tokenizer(
                batch_pairs,
                padding=True,
                truncation=True,
                return_tensors="pt",
                max_length=512  # Еще меньше для скорости
            )

            with torch.no_grad():
                outputs = self.model(**features)
                batch_scores = outputs.logits.squeeze(dim=1)
                scores.extend(batch_scores.tolist())

        return sorted(zip(scores, chunk_indices), key=lambda x: x[0], reverse=True)