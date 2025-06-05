from tqdm import tqdm
import numpy as np 
from component.embedding import HFembedding
import os
import json
from typing import List




class Vectordatabase:

    def __init__(self,docs:List=[],path='RAG/ragdemo/tinyRAG/database') -> None:
        self.docs = docs
        self.path = path
    

    def get_vector(self,EmbeddingModel)->List[List[float]]:
        self.vectors = []
        for doc in tqdm(self.docs):
            self.vectors.append(EmbeddingModel.get_embedding(doc))
        return self.vectors
    

    def persist(self)->None:
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        with open(f"{self.path}/doecment.json", 'w', encoding='utf-8') as f:
            json.dump(self.docs, f, ensure_ascii=False)
        with open(f"{self.path}/vectors.json", 'w', encoding='utf-8') as f:
            json.dump(self.vectors, f)


    def load_vector(self)->None:
        with open(f"{self.path}/vectors.json", 'r', encoding='utf-8') as f:
            self.vectors = json.load(f)
        with open(f"{self.path}/doecment.json", 'r', encoding='utf-8') as f:
            self.document = json.load(f)
    

    def get_similarity(self, vector1: List[float], vector2: List[float],embedding_model) -> float:
        return embedding_model.compare_v(vector1, vector2)
    

    def query(self, query: str, EmbeddingModel, k: int = 1) -> List[str]:
        query_vector = EmbeddingModel.get_embedding(query)
        result = np.array([self.get_similarity(query_vector, vector,EmbeddingModel)
                          for vector in self.vectors])
        return np.array(self.document)[result.argsort()[-k:][::-1]].tolist()