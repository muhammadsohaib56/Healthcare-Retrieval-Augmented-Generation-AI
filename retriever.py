import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class Retriever:
    def __init__(self, documents_path="documents.json"):
        # Load documents
        with open(documents_path, "r", encoding="utf-8") as f:
            self.documents = json.load(f)
        
        # Check if documents are valid
        if not self.documents or not any(doc.get("text") for doc in self.documents):
            raise ValueError("No valid documents found in documents.json. Please run preprocess.py.")
        
        # Load embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        
        # Create embeddings and index
        self.texts = [doc["text"] for doc in self.documents if doc.get("text")]
        if not self.texts:
            raise ValueError("No text data to embed. Check your dataset.")
        self.embeddings = self.model.encode(self.texts, show_progress_bar=True)
        self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
        self.index.add(np.array(self.embeddings))

    def retrieve(self, query, top_k=3):
        # Encode the query
        query_embedding = self.model.encode([query])
        
        # Search the index
        distances, indices = self.index.search(np.array(query_embedding), top_k)
        
        # Return top-k relevant documents
        results = [self.documents[i] for i in indices[0] if i < len(self.documents)]
        return results

if __name__ == "__main__":
    # Test the retriever
    try:
        retriever = Retriever()
        query = "What treatment was given for hypertension?"
        results = retriever.retrieve(query)
        for i, doc in enumerate(results):
            print(f"Result {i+1}: {doc['id']}\n{doc['text'][:200]}...\n")
    except Exception as e:
        print(f"Error: {e}")