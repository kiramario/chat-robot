#!/usr/bin/env python
# -*- coding: utf-8 -*-
# chat-robot.demo
# @Calendar: 2024-12-28 21:13
# @Time: 21:13
# @Author: mammon, kiramario

#python 3.8
import time
import hmac
import hashlib
import base64
import urllib.parse
import asyncio
import aiohttp
import json

def run():
    timestamp = str(round(time.time() * 1000))
    secret = ''
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    url = f"https://oapi.dingtalk.com/robot/send?access_token=&timestamp={timestamp}&sign={sign}"

    HEADERS = {
        "Content-Type": "application/json;charset=utf-8"
    }
    data_info = {
        "msgtype": "text",
        "text": {
            "content": "【测试】kensunglaser push"
        },
        # 这是配置需要@的人
        "at": {
            "atMobiles": [
                "18980406079"
            ],
            "atUserIds": [],
            "isAtAll": False
        }
    }
    value = json.dumps(data_info)

    async def send():
        async with aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers=HEADERS
        ) as session:
            async with session.post(url, data=value) as resp:
                print(resp.status)
                print(await resp.text())

    asyncio.run(send())

if __name__ == "__main__":
    run()
