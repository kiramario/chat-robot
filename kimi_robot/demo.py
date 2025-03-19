#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chat-robot.demo
# @Calendar: 2024-12-09 23:03
# @Time: 23:03
# @Author: mammon, kiramario

from openai import OpenAI
from os.path import expanduser

chat_robot_env = expanduser('~/chat-robot.env')

def run():
    client = OpenAI(
        api_key="",
        base_url="https://api.moonshot.cn/v1",
    )

    completion = client.chat.completions.create(
        model="moonshot-v1-8k",
        messages=[
            {
                "role": "system",
                "content": "你是 Kimi，由 Moonshot AI 提供的人工智能助手，你更擅长中文和英文的对话。你会为用户提供安全，有帮助，准确的回答。同时，你会拒绝一切涉及恐怖主义，种族歧视，黄色暴力等问题的回答。Moonshot AI 为专有名词，不可翻译成其他语言。"
            },
            {
                "role": "user",
                "content": "帮我用【mermaid】生成一个用户登录类图，类图包括以下功能\n 1. 用户登录 \n 2. 用户退出 \n 3. 用户创建 \n 4. 用户删除"
            },
        ],
        temperature=0.3,
    )

    answer = completion.choices[0].message

    print("*" * 30)
    print(answer)


if __name__ == "__main__":
    run()
