import os
import numpy as np
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import spacy
import pandas as pd

app = Flask(__name__)

# Initialize SentenceTransformer model
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Initialize spaCy for sentence splitting
nlp = spacy.load("en_core_web_sm")

# Load the DataFrame with data and embeddings
df = pd.read_parquet("data_with_embeddings.parquet")

# Helper function to process user query and return search results
def search(query, num_results=10):
    query_embedding = model.encode([query])[0]
    similarity_scores = np.dot(df["Embedding"].tolist(), query_embedding)
    sorted_indices = np.argsort(similarity_scores)[::-1]
    results = [{"text": df["Chunk"].iloc[idx], "filename": df["Filename"].iloc[idx]} for idx in sorted_indices[:num_results]]
    return results

@app.route('/search', methods=['GET'])
def search_endpoint():
    user_query = request.args.get('q', '')  # Get user query from query parameter
    print('query----> ')
    print(user_query)
    search_results = search(user_query)
    return jsonify(search_results)

if __name__ == '__main__':
    app.run(debug=True)
