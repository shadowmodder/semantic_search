# models/data_access.py

import os
import spacy
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
import numpy as np

class DataAccess:
    def __init__(self, data_directory="Sample_Docs"):
        self.data_directory = data_directory
        self.model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        self.nlp = spacy.load("en_core_web_sm")
        self.df = self.load_data()

    def load_data(self):
        chunks = []
        filenames = []
        embeddings = []

        for subfolder in ["pdf", "txt", "word"]:
            subfolder_path = os.path.join(self.data_directory, subfolder)
            for filename in os.listdir(subfolder_path):
                filepath = os.path.join(subfolder_path, filename)

                if filepath.endswith(".pdf"):
                    pdf = PdfReader(filepath)
                    pdf_text = " ".join(page.extract_text() for page in pdf.pages)
                    document_chunks = self.nlp(pdf_text)
                elif filepath.endswith(".txt"):
                    with open(filepath, "r", encoding="utf-8") as f:
                        document_text = f.read()
                    document_chunks = self.nlp(document_text)
                elif filepath.endswith(".docx"):
                    doc = Document(filepath)
                    doc_text = " ".join(para.text for para in doc.paragraphs)
                    document_chunks = self.nlp(doc_text)
                else:
                    continue

                for chunk in document_chunks.sents:
                    chunks.append(chunk.text)
                    filenames.append(filename)
                    embeddings.append(self.model.encode([chunk.text])[0])

        data = {"Chunk": chunks, "Filename": filenames, "Embedding": embeddings}
        df = pd.DataFrame(data)

        return df

    def get_all_embeddings(self):
        return self.df["Embedding"].tolist()

    def get_all_filenames(self):
        return self.df["Filename"].tolist()
    
    def check_database_health():
        # ToDo Add logic to check the database connectivity
        # Return True if the connection is successful, else return False
        try:
            # Check the database connection here
            return True
        except Exception as e:
            return False

