#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chat-robot.Greeting
# @Calendar: 2025-01-05 22:15
# @Time: 22:15
# @Author: mammon, kiramario
import datetime
import discord, asyncio
from discord.ext import commands, tasks
from discord import Intents, Message, Attachment
from loguru import logger
import re
import requests
import xxhash

class AttachementListener(commands.Cog):
    def __init__(self, bot):
        print("AttachementListener init")
        self.bot = bot
        self.content = ""

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        print(f"AttachementListener: {message.content}")
        print(f"message.author.id = {message.author.id}")
        if str(message.author.id) == "936929561302675456":
            customer_content_match = re.search(r"\*\*.+\*\*", message.content)
            if customer_content_match:
                customer_content = (customer_content_match.group()).lstrip("\*\*").strip("\*\*")
                self.content = customer_content
                print(f"self.content: {self.content}")

            if len(message.attachments) > 0:
                hash_value = xxhash.xxh64(self.content.encode("utf-8")).hexdigest()
                print(f"hash_value = {hash_value}")
                url = message.attachments[0].url
                print(f"url = {url}")

                response = requests.get(url)
                if response.status_code == 200:
                    with open(f'C:\\Users\\mammon\\Desktop\\md_pics\\{hash_value}.jpg', 'wb') as file:
                        file.write(response.content)
                    print('图片下载并保存成功')
                else:
                    print('请求图片失败，状态码：', response.status_code)

async def setup(bot):
    await bot.add_cog(AttachementListener(bot))

def run():
    pass


if __name__ == "__main__":
    start = datetime.datetime.now()
    run()
    exec_time = (datetime.datetime.now() - start).total_seconds()
    print(f"run total spend: {exec_time:.3f}s\n")
