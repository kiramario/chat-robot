#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chat-robot.kimi
# @Calendar: 2025-03-22 12:43
# @Time: 12:43
# @Author: mammon, kiramario
import datetime, json, requests, uuid, time
from os.path import expanduser
from openai import OpenAI
from loguru import logger
import tiktoken
import sqlite3

def get_secrets():
    with open(expanduser('~/chat-robot.env')) as f:
        secrets = json.load(f)
    return secrets["kimi"]

# FIXME: 每次对话请求一个client还是可以通用一个client
kimi_client = OpenAI(
    api_key=get_secrets()["api_key"],
    base_url="https://api.moonshot.cn/v1",
)

messages = [
    {
        "role": "system",
        "content": "你具有上下文推理能力，请你根据上文的内容，进行逻辑上的推理"
    },
]

specific_model = "moonshot-v1-8k"


def get_token(messages: list):
    api_key = get_secrets()["api_key"]
    url = "https://api.moonshot.cn/v1/tokenizers/estimate-token-count"
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}
    data = {'model': specific_model, "messages" : messages}

    # response: requests.Response = requests.post(url, data = json.dumps(data), headers=headers)
    response: requests.Response = requests.post(url,  json=data, headers=headers)
    response_json = response.json()

    # 测试：获取特定模型的编码
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(messages[0]["content"])
    # 计算 token 数量
    token_count = len(tokens)
    print("Token 数量:", token_count)

    if response_json["code"] == 0:
        return response_json["data"]["total_tokens"]

def chat_with_history(input: str, history: list):
    history.append({
        "role": "user",
        "content": input,
    })

    completion = kimi_client.chat.completions.create(
        model = specific_model,
        messages = history,
        temperature = 0.3,
    )
    logger.info(completion)

    # 计算token
    cost_token = get_token(history)
    logger.info("cost_token: ", cost_token)

    assistant_message = completion.choices[0].message
    history.append({
        "role": "assistant",
        "content": assistant_message.content
    })

    logger.info("*" * 30)
    # logger.info(assistant_message)
    return assistant_message.content

def run():
    def test1():
        print(chat_with_history("所有A都是B", messages))
        print(chat_with_history("C是A", messages))
        print(chat_with_history("请问C是不是B", messages))

        print("final message: ", str(messages))

    def test2():
        print(get_token(messages))

    # test1()
    # test2()

if __name__ == "__main__":
    start = datetime.datetime.now()
    run()
    exec_time = (datetime.datetime.now() - start).total_seconds()
    print(f"run total spend: {exec_time:.3f}s\n")
