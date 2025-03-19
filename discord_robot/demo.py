#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chat-robot.demo
# @Calendar: 2024-12-26 15:51
# @Time: 15:51
# @Author: mammon, kiramario


from loguru import logger
import aiohttp
import asyncio
from aiohttp import ClientError, ClientSession, hdrs
from typing import Callable, Coroutine, Any, TypeVar, Union, Dict
import json, time



class FetchMethod:
    get = hdrs.METH_GET
    post = hdrs.METH_POST
    put = hdrs.METH_PUT



def imagine():
    DRAW_VERSION=""
    GUILD_ID=""
    CHANNEL_ID=""
    APPLICATION_ID=""
    SESSION_ID=""
    DATA_ID=""
    USER_TOKEN=""
    PROXY_URL="http://127.0.0.1:7897"

    payload = {
        "type": 2,
        "application_id": APPLICATION_ID,
        "guild_id": GUILD_ID,
        "channel_id": CHANNEL_ID,
        "session_id": SESSION_ID,
        "data": {
                "version": DRAW_VERSION,
                "id": DATA_ID,
                "name": "imagine",
                "type": 1,
                "options": [{
                    "type": 3,
                    "name": "prompt",
                    "value": "goat"
                }],
                "attachments": []
            }
    }

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": USER_TOKEN
    }
    TRIGGER_URL = "https://discord.com/api/v9/interactions"

    async def fetch(
            session: ClientSession,
            url: str,
            method: str = FetchMethod.post, **kwargs
    ) -> Union[bool, None]:
        logger.debug(f"Fetch: {url}, {kwargs}")
        async with session.request(method, url, **kwargs) as resp:
            if not resp.ok:
                return None
            return True

    async def imagine():
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers=HEADERS
        ) as session:
            # async with session.get('http://httpbin.org/get') as resp:
            #     print(resp.status)
            #     print(await resp.text())

            return await fetch(session, TRIGGER_URL, data=json.dumps(payload), proxy=PROXY_URL)

    asyncio.run(imagine())


def run():

    pass


if __name__ == "__main__":
    # print(discord.__version__)
    run()
