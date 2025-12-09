from transformers import AutoTokenizer, AutoModel
import torch
import numpy

class TextEmbedder:
    def __init__(self, model_name='intfloat/multilingual-e5-large'):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()

    def get_embeddings(self, texts):
        with torch.no_grad():
            inputs = self.tokenizer(texts, padding=True, truncation=True,
                                  max_length=128, return_tensors='pt')
            outputs = self.model(**inputs)

            embeddings = outputs.last_hidden_state[:, 0, :]
            embeddings = torch.nn.functional.normalize(embeddings, p=2, dim=1)

            return embeddings.numpy().astype('float32')