import os
import spacy
import pandas as pd
from docx import Document
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer

class DataAccess:
    def __init__(self, data_directory="Sample_Docs"):
        self.data_directory = data_directory
        self.model = SentenceTransformer("paraphrase-MiniLM-L6-v2")
        self.nlp = spacy.load("en_core_web_sm")
        self.df = self.load_data()
        self.parquet_filename = "res/data/data_chunks.parquet"
        if not os.path.exists(self.parquet_filename):
            self.save_parquet(self.df)

    def load_data(self):
        chunks = []
        filenames = []
        embeddings = []
        context = []  # list to store additional context

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
                    document_chunks = list(self.nlp(doc_text).sents)  # Convert to a list

                    for chunk in document_chunks:
                        chunk_index = document_chunks.index(chunk)
                        start_index = max(0, chunk_index - 1)
                        end_index = min(len(document_chunks), chunk_index + 2)
                        context_chunk = document_chunks[start_index:end_index]
                        context_text = " ".join([str(sent) for sent in context_chunk])

                        chunks.append(chunk.text)
                        context.append(context_text)  # Store additional context
                        filenames.append(filename)
                        embeddings.append(self.model.encode([chunk.text])[0])

                else:
                    continue

        data = {"Chunk": chunks, "Context": context, "Filename": filenames, "Embedding": embeddings}
        df = pd.DataFrame(data)

        return df

    def save_parquet(self, dframe):
        # Save DataFrame as Parquet file
        dframe.to_parquet(self.parquet_filename, index=False)
        print(f"Data saved as {self.parquet_filename}")

    def get_all_embeddings(self):
        try:
            # Load the Parquet file into a DataFrame
            df = pd.read_parquet(self.parquet_filename)

            # Assuming the DataFrame has an "Embedding" column
            if "Embedding" in df.columns:
                return df["Embedding"].tolist()
            else:
                return []
        except Exception as e:
            print(f"Error loading embeddings: {str(e)}")
            return []

    def get_all_filenames(self):
        try:
            # Load the Parquet file into a DataFrame
            df = pd.read_parquet(self.parquet_filename)

            # Assuming the DataFrame has a "Filename" column
            if "Filename" in df.columns:
                return df["Filename"].tolist()
            else:
                return []
        except Exception as e:
            print(f"Error loading filenames: {str(e)}")
            return []
        
    def get_all_contexts(self):
        try:
            # Load the Parquet file into a DataFrame
            df = pd.read_parquet(self.parquet_filename)

            # Assuming the DataFrame has an "Contexts" column
            if "Context" in df.columns:
                return df["Context"].tolist()
            else:
                return []
        except Exception as e:
            print(f"Error loading contexts: {str(e)}")
            return []