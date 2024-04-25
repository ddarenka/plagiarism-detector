from sentence_transformers import SentenceTransformer, util
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class SemanticRetrieval:
    def __init__(self, model_name='paraphrase-multilingual-MiniLM-L12-v2'):
        self.model = SentenceTransformer(model_name)

    def encode_text(self, text):
        return self.model.encode(text, convert_to_tensor=True)

    def find_similar(self, query_embedding, corpus_embeddings, top_k=5):
        similarities = util.pytorch_cos_sim(query_embedding, corpus_embeddings)
        top_results = np.argpartition(-similarities[0], range(top_k))[:top_k]
        return top_results.tolist()

class TFIDFRetrieval(SemanticRetrieval):
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def encode_text(self, texts):
        # This method now fits the TF-IDF model to the texts and transforms them
        return self.vectorizer.fit_transform(texts)

    def find_similar(self, query_embedding, corpus_embeddings, top_k=5):
        # Compute cosine similarities between the query and corpus embeddings
        cosine_similarities = linear_kernel(query_embedding, corpus_embeddings).flatten()
        # Get indices of top_k documents
        top_k_indices = cosine_similarities.argsort()[-top_k:][::-1]
        return top_k_indices
    
# Example usage:
# pip install sentence-transformers
# 1. Initialize the semantic retrieval system
semantic_retrieval = SemanticRetrieval()

# 2. Suppose you have a list of texts (corpus) and a query text
corpus = ["This is a sample sentence", "Another example text", "More data to test"]
query = "Sample text for testing"

# 3. Encode the corpus and the query to get their embeddings
corpus_embeddings = semantic_retrieval.encode_text(corpus)
query_embedding = semantic_retrieval.encode_text(query)

# 4. Find the most similar texts in the corpus to the query
top_k_indices = semantic_retrieval.find_similar(query_embedding, corpus_embeddings, top_k=2)
print("Top K similar texts in the corpus:", [corpus[index] for index in top_k_indices])