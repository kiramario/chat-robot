#coding=utf-8

import json, os, base64, requests
from os.path import expanduser, expandvars
from speech_robot.tts.schema import Volceengine_app,  Volceengine_audio, Volceengine_req_body, Volceengine_req_request, Volceengine_user
from dotenv import load_dotenv

def get_secrets():
    with open(expanduser('~/chat-robot.env')) as f:
        secrets = json.load(f)
    return secrets["volcengine"]

def get_reqbody(text: str) -> Volceengine_req_body:
    secrets = get_secrets()
    appid = "3613331191"
    cluster = "volcano_tts"
    access_token = secrets["access_token"]
    voice_type = "BV700_V2_streaming"

    request_body = Volceengine_req_body(
        app = Volceengine_app(appid=appid, token=access_token, cluster=cluster),
        user = Volceengine_user(uid="388808087185088"),
        audio = Volceengine_audio(voice_type=voice_type),
        request = Volceengine_req_request(text = text)
    )

    return request_body

"""
生成音频文件，返回存放地址
"""
def generate_voice_file(text: str) -> str:
    secrets = get_secrets()
    access_token = secrets["access_token"]
    host = "openspeech.bytedance.com"
    api_url = f"https://{host}/api/v1/tts"

    request_body = get_reqbody(text)

    load_dotenv("./speech_robot/.env.template")
    mp3_dir = os.getenv("TTS_DIR")

    if mp3_dir is None:
        print("mp3 is none")
        return

    header = {"Authorization": f"Bearer;{access_token}"}
    try:
        resp = requests.post(api_url, request_body.model_dump_json(), headers=header)
        print(f"resp body: \n{resp.json()}")
        if "data" in resp.json():
            data = resp.json()["data"]
            with open(f"{mp3_dir}\\test_submit.mp3", "wb") as f:
                f.write(base64.b64decode(data))
            return f"{mp3_dir}\\test_submit.mp3"
        
    except Exception as e:
        e.with_traceback()
    
if __name__ == "__main__":
    # request_body = get_reqbody("sdf")
    # print(request_body.model_dump_json())

    # app = Volceengine_app(appid="appid", token="token", cluster="cluster")
    # print(app.model_dump())
    # print(app.model_dump_json())
    # print(app.model_validate({
    #     "appid": "appid",
    #     "token": "access_token",
    #     "cluster": "cluster"
    # }))

    audio = Volceengine_audio(voice_type="voice_type")
    print(audio.model_dump_json())