#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chat-robot.midjourney_prob
# @Calendar: 2025-01-05 21:04
# @Time: 21:04
# @Author: mammon, kiramario

import datetime
import discord, asyncio
from discord.ext import commands, tasks
from discord import Intents, Message
from loguru import logger

MIDJOURNEY_PROB_TOKEN=''

async def main():
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='$', proxy="http://127.0.0.1:7897", intents=intents, description='A bot that greets the user back.')

    @bot.event
    async def on_ready():
        logger.debug(f'midjourney_prob robot')
        logger.debug(f'Logged in as {bot.user.name}, id = {bot.user.id}')

    @bot.command()
    async def add(ctx, a: int, b: int):
        await ctx.send(a + b)

    await bot.load_extension("cogs.Greeting")
    await bot.load_extension("cogs.AttachementListener")

    await bot.start(MIDJOURNEY_PROB_TOKEN)

if __name__ == "__main__":
    start = datetime.datetime.now()
    asyncio.run(main())
    exec_time = (datetime.datetime.now() - start).total_seconds()
    print(f"run total spend: {exec_time:.3f}s\n")
