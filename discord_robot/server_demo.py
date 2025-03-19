#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chat-robot.sever_demo
# @Calendar: 2025-01-04 11:08
# @Time: 11:08
# @Author: mammon, kiramario

import time
from aiohttp import web
import discord
from discord.ext import commands
from discord import Intents, Message
from loguru import logger
import aiohttp, json, asyncio
from aiohttp import ClientError, ClientSession, hdrs
from typing import Callable, Coroutine, Any, TypeVar, Union, Dict


# 创建中间件
def cors_middleware(allow_all, origins, allow_credentials, expose_headers, allow_headers, allow_methods):
    @web.middleware
    async def middleware(request, handler):
        if allow_all or request.headers.get('Origin') in origins:
            response = await handler(request)
            logger.debug(f"middleware: {response}")
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true' if allow_credentials else 'false'
            response.headers['Access-Control-Expose-Headers'] = expose_headers
            response.headers['Access-Control-Allow-Headers'] = allow_headers
            response.headers['Access-Control-Allow-Methods'] = ', '.join(allow_methods)
            return response
        return web.Response(status=403, text="CORS not allowed")
    return middleware


class FetchMethod:
    get = hdrs.METH_GET
    post = hdrs.METH_POST
    put = hdrs.METH_PUT

routes = web.RouteTableDef()

@routes.get('/{timesleep}')
async def hello(request):
    timesleep = int(request.match_info['timesleep'])
    await asyncio.sleep(timesleep)
    return web.Response(text=f"Hello, world: {timesleep}")


def get_discord_payload(prompt):
    DRAW_VERSION = "1237876415471554623"
    GUILD_ID = "1321731390030741536"
    CHANNEL_ID = "1321731390584258582"
    APPLICATION_ID = "936929561302675456"
    SESSION_ID = "19757397a15dcb53ceca6b3822f96b5c"
    DATA_ID = "938956540159881230"


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
                "value": prompt
            }],
            "attachments": []
        }
    }
    return payload

@routes.post('/submit_prompt')
async def submit_prompt(request):
    data = await request.post()
    # data = await request.json()

    print(data)
    print(data.get("prompt"))
    return web.Response(text=f"submit_prompt finish")


@routes.post('/imagine')
async def imagine(request):
    # user_token 会变化
    USER_TOKEN = ""
    PROXY_URL = "http://127.0.0.1:7897"
    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": USER_TOKEN
    }
    TRIGGER_URL = "https://discord.com/api/v9/interactions"

    data = await request.json()
    prompt = data.get('prompt')
    print(prompt)
    payload = get_discord_payload(prompt)

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

    async def image():
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers=HEADERS
        ) as session:
            return await fetch(session, TRIGGER_URL, data=json.dumps(payload), proxy=PROXY_URL)

    await image()
    return web.Response(text=f"imagine finish")


async def defaultHandler(request):
    return web.Response(text="welcome onlyfuns")

def run():
    logger.debug("server start by pycharm")
    web.run_app(app = init_func([]),  host='localhost',  port=9999)

def init_func(argv):
    app = web.Application(
        middlewares=[
            cors_middleware(
                allow_all=True,
                origins=['*'],
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
                allow_methods=["POST", "GET", "OPTIONS", "PATCH"],
            )
        ]
    )

    app.add_routes([web.route('*', '/default', defaultHandler)])
    app.add_routes([web.route('OPTIONS', '/submit_prompt', defaultHandler)])
    app.add_routes(routes)
    return app

if __name__ == "__main__":
    run()
