import os
import numpy as np
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer
import spacy
from chunks_to_parquet import get_all_embeddings, get_all_filenames


app = Flask(__name__)

# Initialize SentenceTransformer model
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Initialize spaCy for sentence splitting
nlp = spacy.load("en_core_web_sm")

# Path to the directory containing content subfolders
content_directory = "Sample_Docs"

# Process and load embeddings and metadata (replace with your actual data)
embeddings = get_all_embeddings
metadata = get_all_filenames  # Replace with your filenames

# Helper function to process user query and return search results
def search(query, num_results=10):
    query_embedding = model.encode([query])[0]
    similarity_scores = np.dot(embeddings, query_embedding)
    sorted_indices = np.argsort(similarity_scores)[::-1]
    results = [{"text": metadata[idx], "filename": metadata[idx]} for idx in sorted_indices[:num_results]]
    return results

@app.route('/search', methods=['GET'])
def search_endpoint():
    user_query = request.args.get('q', '')  # Get user query from query parameter
    search_results = search(user_query)
    return jsonify(search_results)

if __name__ == '__main__':
    app.run(debug=True)
