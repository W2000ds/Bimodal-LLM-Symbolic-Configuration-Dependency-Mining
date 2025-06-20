from openai import OpenAI
import requests

def dpseek_chat(question):

    client = OpenAI(api_key="your api-key", base_url="https://api.deepseek.com")
    
    system_message = {"role": "system", "content": "You are an experienced software engineering expert"}
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            system_message,
            {"role": "user", "content": question}
        ],
        stream=False
    )
    
    responsetext = response.choices[0].message.content
    return responsetext

def doubao_chat(question):
    client = OpenAI(base_url="https://ark.cn-beijing.volces.com/api/v3",api_key="your api-key")

    system_message = {"role": "system", "content": "You are an experienced software engineering expert"}
    
    response = client.chat.completions.create(
        model="doubao-1-5-pro-32k-250115",
        messages=[
            system_message,
            {"role": "user", "content": question}
        ],
        stream=False
    )
    
    responsetext = response.choices[0].message.content
    return responsetext


def qwen_chat(question):
    client = OpenAI(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",api_key="your api-key")

    system_message = {"role": "system", "content": "You are an experienced software engineering expert"}
    
    response = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            system_message,
            {"role": "user", "content": question}
        ],
        stream=False,
        extra_body={"enable_thinking": False}
    )
    
    responsetext = response.choices[0].message.content
    return responsetext

def dpseek_qwen_chat(question):
    client = OpenAI(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",api_key="your api-key")

    system_message = {"role": "system", "content": "You are an experienced software engineering expert"}
    
    response = client.chat.completions.create(
        model="deepseek-v3",
        messages=[
            system_message,
            {"role": "user", "content": question}
        ],
        stream=False,
        extra_body={"enable_thinking": False}
    )

    responsetext = response.choices[0].message.content
    return responsetext
    

if __name__ == "__main__":
    print(doubao_chat("What is the purpose of the function in the code snippet?"))