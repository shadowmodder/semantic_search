import os
import spacy
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np

# Initialize spaCy model for sentence splitting
nlp = spacy.load("en_core_web_sm")

# Initialize SentenceTransformer model for embeddings
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

# Directory containing subfolders with documents
main_directory = "Sample_Docs"

# Initialize lists to store data
chunks = []
filenames = []
embeddings = []

# Traverse through subfolders
for subfolder in ["pdf", "txt", "word"]:
    subfolder_path = os.path.join(main_directory, subfolder)
    for filename in os.listdir(subfolder_path):
        filepath = os.path.join(subfolder_path, filename)
        
        # Process PDF files
        if filepath.endswith(".pdf"):
            pdf = PdfReader(filepath)
            pdf_text = " ".join(page.extract_text() for page in pdf.pages)
            document_chunks = nlp(pdf_text)
            
        # Process text files
        elif filepath.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                document_text = f.read()
            document_chunks = nlp(document_text)
            
        # Process Word files
        elif filepath.endswith(".docx"):
            doc = Document(filepath)
            doc_text = " ".join(para.text for para in doc.paragraphs)
            document_chunks = nlp(doc_text)
            
        # Process other file types (if needed)
        else:
            continue
        
        # Generate text chunks and store metadata and embeddings
        for chunk in document_chunks.sents:
            chunks.append(chunk.text)
            filenames.append(filename)
            embeddings.append(model.encode([chunk.text])[0])

# Create a DataFrame to store data
data = {
    "Chunk": chunks,
    "Filename": filenames,
    "Embedding": embeddings
}
df = pd.DataFrame(data)

# Save DataFrame as Parquet file
parquet_filename = "data_with_embeddings.parquet"
df.to_parquet(parquet_filename, index=False)

print(f"Data with embeddings saved as {parquet_filename}")

# Function to return all embeddings
def get_all_embeddings():
    return df["Embedding"].tolist()

# Function to return all filenames
def get_all_filenames():
    return df["Filename"].tolist()
