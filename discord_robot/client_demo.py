#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chat-robot.client_demo
# @Calendar: 2025-01-04 19:18
# @Time: 19:18
# @Author: mammon, kiramario
import aiohttp
import asyncio
import datetime
import requests
import json

def requete_timesleep(timesleep):
    print(f"start sleep {timesleep}")
    content = requests.get(f"http://127.0.0.1:9999/{timesleep}")
    print(f"Res {content.content}")

def requetes():
    requete_timesleep(3)
    requete_timesleep(4)




async def getHello(session, timesleep):
    resp = await session.get(f'http://127.0.0.1:9999/{timesleep}')
    content = await resp.text()

    print(resp.status)
    print(content)

    resp.close()
    return content


async def getHello2(session, timesleep):
    print(f"start sleep {timesleep}")
    async with session.get(f'http://127.0.0.1:9999/{timesleep}') as response:
        content = await response.text()
        print(f"getHello2 {content}")
    return content

async def imagine(session):
    async with session.post(f"http://127.0.0.1:9999/imagine",  data=json.dumps({"prompt": "The mythical creature from China's 'Shan Hai Jing' (The Classic of Mountains and Seas), it looks like bird,it has only one beak, one wing, one eye. "})) as response:
        content = await response.text()
        print(f"imagine content = {content}")
    return content


async def main():
    async with aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=30),
                headers={
                    "Content-Type": "application/json",
                    # "Content-Type": "application/x-www-form-urlencoded",
                }) as session:
        results = await asyncio.gather(getHello2(session, 3), getHello2(session, 4), imagine(session))
        print(results)

def run():
    start = datetime.datetime.now()
    asyncio.run(main())
    # requetes()
    exec_time = (datetime.datetime.now() - start).total_seconds()
    print(f"Pour faire 10 requêtes, sprend {exec_time:.3f}s\n")




if __name__ == "__main__":
    run()
