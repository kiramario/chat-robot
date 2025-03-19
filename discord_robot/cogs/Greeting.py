#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chat-robot.Greeting
# @Calendar: 2025-01-05 22:15
# @Time: 22:15
# @Author: mammon, kiramario
import datetime
import discord, asyncio
from discord.ext import commands, tasks
from discord import Intents, Message
from loguru import logger


class Greetings(commands.Cog):
    def __init__(self, bot):
        print("greeting init")
        self.bot = bot
        self._last_member = None
        self.index = 0
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(minutes=10)
    async def printer(self):
        logger.debug(f"Greetings task loop: {self.index * 10} minutes")
        self.index += 1

    # @commands.Cog.listener()
    # async def on_message(self, message: Message):
    #     print(f"Greetings: {message.content}")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(f'Welcome {member.mention}.')

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        """Says hello"""
        member = member or ctx.author
        if self._last_member is None or self._last_member.id != member.id:
            await ctx.send(f'Hello {member.name}~ {self.index}')
        else:
            await ctx.send(f'Hello {member.name}... This feels familiar. {self.index}')
        self._last_member = member

async def setup(bot):
    await bot.add_cog(Greetings(bot))

def run():
    pass


if __name__ == "__main__":
    start = datetime.datetime.now()
    run()
    exec_time = (datetime.datetime.now() - start).total_seconds()
    print(f"run total spend: {exec_time:.3f}s\n")
