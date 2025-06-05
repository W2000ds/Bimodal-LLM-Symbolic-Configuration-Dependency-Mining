from component.embedding import Zhipuembedding, BGEembedding
from component.data_chunker import ReadFile
from component.databases import Vectordatabase
from component.llms import Openai_model



if __name__ == '__main__':

    api_key = "Your api key"
    base_url = "https://api.deepseek.com"

    softwarelist = ["cinder","glance"]

    for software in softwarelist:

        vecdatapath = f'./database/{software}'

        filter = ReadFile(f'./data/{software}')
        docs = filter.get_all_chunk_content(200, 150)

        embedding_model = Zhipuembedding()
        database = Vectordatabase(docs, vecdatapath)

        Vectors = database.get_vector(embedding_model)
        database.persist()



