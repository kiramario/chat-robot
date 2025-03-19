#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chat-robot.discord_demo
# @Calendar: 2025-01-05 20:36
# @Time: 20:36
# @Author: mammon, kiramario
import datetime
import discord
from discord.ext import commands
from discord import Intents, Message
from loguru import logger

MIDJOURNEY_PROB_TOKEN=''

def minimalBot():
    # 这里 proxy 根据你自己的需要进行填写，也可以不用填
    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(proxy="http://127.0.0.1:7897", intents=discord.Intents.all())

    @client.command()
    async def foo(ctx, arg):
        await ctx.send(arg)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('/imagine prompt:snail')

    client.run(MIDJOURNEY_PROB_TOKEN)

def command_demo():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='$', proxy="http://127.0.0.1:7897", intents=intents, description='A bot that greets the user back.')

    @bot.event
    async def on_ready():
        print('Logged in as')
        print(bot.user.name)
        print(bot.user.id)
        print('------')

    @bot.command()
    async def add(ctx, a: int, b: int):
        await ctx.send(a + b)

    @bot.event
    async def on_message(message: Message):
        content = message.content
        logger.debug(content)

    @bot.event
    async def on_message_edit(before: Message, after: Message):
        logger.debug(f"on_message_edit before: {before.content}")
        logger.debug(f"on_message_edit after: {after.content}")

    @bot.event
    async def on_message_delete(message: Message):
        logger.debug(f"on_message_delete: {message.content}")


    bot.run(MIDJOURNEY_PROB_TOKEN)

def run():
    command_demo()


if __name__ == "__main__":
    start = datetime.datetime.now()
    run()
    exec_time = (datetime.datetime.now() - start).total_seconds()
    print(f"run total spend: {exec_time:.3f}s\n")


