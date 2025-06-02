from openai import OpenAI
import requests

def dpseek_chat(question):
    """单次调用deepseek API获取答案"""
    client = OpenAI(api_key="sk-23c9c90c502840c0b43c9d92bd403504", base_url="https://api.deepseek.com")
    
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
    client = OpenAI(base_url="https://ark.cn-beijing.volces.com/api/v3",api_key="fa38bef1-f5d2-4679-b752-fc56e770a5f4")

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
    client = OpenAI(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",api_key="sk-89b18a26982d43b1952518f03c346f5e")

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
    client = OpenAI(base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",api_key="sk-89b18a26982d43b1952518f03c346f5e")

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

def siliconflow_chat(question):

    """单次调用siliconflow API获取答案"""
    url = "https://api.siliconflow.cn/v1/chat/completions"
    
    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": [{"role": "user", "content": question}],
        "stream": False,
        "max_tokens": 4096,
        "temperature": 0.7,
        "top_p": 0.7,
        "top_k": 50,
        "frequency_penalty": 0.5,
        "n": 1,
        "response_format": {"type": "text"}
    }
    headers = {
        "Authorization": "Bearer sk-isynoyqwkemchrmzxhiolofftxdjtebgpybfhwykydcrialh",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    # full_response = response.text
    # print(full_response)
    if response.status_code == 200:
        responsetxt = response.json()["choices"][0]["message"]["content"]
        return responsetxt
    else:
        return f"Error: {response.status_code}", ""
    

if __name__ == "__main__":
    print(doubao_chat("What is the purpose of the function in the code snippet?"))