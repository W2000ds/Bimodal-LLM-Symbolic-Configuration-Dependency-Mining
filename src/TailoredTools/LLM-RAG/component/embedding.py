import numpy as np
from transformers import AutoModel
from numpy.linalg import norm
# from langchain_community.embeddings import OpenAIEmbeddings
from zhipuai import ZhipuAI
from langchain_community.embeddings import HuggingFaceEmbeddings
import os
from typing import List
import requests
import json

#Embedding
class HFembedding:


    def __init__(self, path:str=''):
        self.path = path
        self.embedding=HuggingFaceEmbeddings(model_name=path)


    def get_embedding(self,content:str=''):
        return self.embedding.embed_query(content)


    def compare(self, text1: str, text2: str):
        embed1=self.embedding.embed_query(text1) 
        embed2=self.embedding.embed_query(text2)
        return np.dot(embed1, embed2) / (np.linalg.norm(embed1) * np.linalg.norm(embed2))

    def compare_v(cls, vector1: List[float], vector2: List[float]) -> float:
        dot_product = np.dot(vector1, vector2)
        magnitude = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        if not magnitude:
            return 0
        return dot_product / magnitude


# class OpenAIembedding:
    
#     def __init__(self, path:str=''):
#         self.path = path
#         self.embedding=OpenAIEmbeddings()
    
#     def get_embedding(self,content:str=''):
#         content = content.replace("\n", " ")
#         return self.embedding.embed_query(content)
    
#     def compare(self, text1: str, text2: str):
#         embed1=self.embedding.embed_query(text1) 
#         embed2=self.embedding.embed_query(text2)
#         return np.dot(embed1, embed2) / (np.linalg.norm(embed1) * np.linalg.norm(embed2))
    
#     def compare_v(cls, vector1: List[float], vector2: List[float]) -> float:
#         dot_product = np.dot(vector1, vector2)
#         magnitude = np.linalg.norm(vector1) * np.linalg.norm(vector2)
#         if not magnitude:
#             return 0
#         return dot_product / magnitude



class Zhipuembedding:

    def __init__(self, path:str=''):
        client = ZhipuAI(api_key='your api key') 
        self.embedding_model=client


    def get_embedding(self,content:str=''):
        response =self.embedding_model.embeddings.create(
            model="embedding-2", 
            input=content 
        )
        return response.data[0].embedding

    def compare_v(cls, vector1: List[float], vector2: List[float]) -> float:
        dot_product = np.dot(vector1, vector2)
        magnitude = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        if not magnitude:
            return 0
        return dot_product / magnitude
    
    def compare(self, text1: str, text2: str):
        embed1=self.embedding_model.embeddings.create(
            model="embedding-2", 
            input=text1 
        ).data[0].embedding

        embed2=self.embedding_model.embeddings.create(
            model="embedding-2", 
            input=text2 
        ).data[0].embedding

        return np.dot(embed1, embed2) / (np.linalg.norm(embed1) * np.linalg.norm(embed2))
    

class BGEembedding:
    def __init__(self, access_token: str = 'bce-v3/ALTAK-QPvXIo9W6nTQ47ZfrJIng/2288e2afb050b87ec93c682a2ffb92f72a293873'):
        """
        """
        self.access_token = access_token

    def get_embedding(self, content: str = '') -> List[float]:
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/bge_large_en"
        payload = json.dumps({
        "input": [
            "test"
        ]
    }, ensure_ascii=False)
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.access_token}'
        }
        response = requests.post(url, headers=headers, data=payload.encode("utf-8"))
        data = response.json()
        if "data" not in data:
            raise RuntimeError(f"BGE API Error: {data}")
        return data["data"][0]["embedding"]

    @staticmethod
    def compare_v(vector1: List[float], vector2: List[float]) -> float:
        dot_product = np.dot(vector1, vector2)
        magnitude = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        if not magnitude:
            return 0
        return dot_product / magnitude

    def compare(self, text1: str, text2: str) -> float:
        embed1 = self.get_embedding(text1)
        embed2 = self.get_embedding(text2)
        return np.dot(embed1, embed2) / (np.linalg.norm(embed1) * np.linalg.norm(embed2))

# class Jinaembedding:

#     def __init__(self, path:str='jinaai/jina-embeddings-v2-base-zh'):
#         self.path = path
#         self.embedding_model=AutoModel.from_pretrained('jinaai/jina-embeddings-v2-base-zh', trust_remote_code=True) 
    
#     def get_embedding(self,content:str=''):
#         return self.embedding_model.encode([content])[0]
    
#     def compare(self, text1: str, text2: str):
        
#         cos_sim = lambda a,b: (a @ b.T) / (norm(a)*norm(b))
#         embeddings = self.embedding_model.encode([text1, text2])
#         return cos_sim(embeddings[0], embeddings[1])

#     def compare_v(cls, vector1: List[float], vector2: List[float]) -> float:
#         dot_product = np.dot(vector1, vector2)
#         magnitude = np.linalg.norm(vector1) * np.linalg.norm(vector2)
#         if not magnitude:
#             return 0
# #         return dot_product / magnitude
# def main():
        
#     url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/embeddings/bge_large_en"
    
#     payload = json.dumps({
#         "input": [
#             "test"
#         ]
#     }, ensure_ascii=False)
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': 'Bearer bce-v3/ALTAK-QPvXIo9W6nTQ47ZfrJIng/2288e2afb050b87ec93c682a2ffb92f72a293873'
#     }
    
#     response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    
#     print(response.text)
    

# if __name__ == '__main__':
#     main()