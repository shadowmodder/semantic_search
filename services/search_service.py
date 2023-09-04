# services/search_service.py

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from models.data_access import DataAccess

class SearchService:
    def __init__(self):
        self.data_access = DataAccess()

    def search(self, query, num_results=10):
        query_embedding = self.data_access.model.encode([query])[0]
        similarity_scores = np.dot(self.data_access.df["Embedding"].tolist(), query_embedding)
        sorted_indices = np.argsort(similarity_scores)[::-1]
        results = []
        for idx in sorted_indices[:num_results]:
            result = {
                "text": self.data_access.df["Chunk"].iloc[idx],
                "filename": self.data_access.df["Filename"].iloc[idx],
                "context": self.data_access.df["Context"].iloc[idx]  # Include context
            }
            results.append(result)
        
        return results
        # results = [{"text": self.data_access.df["Chunk"].iloc[idx], "filename": self.data_access.df["Filename"].iloc[idx]} for idx in sorted_indices[:num_results]]
        # return results
