from pydantic import BaseModel
import uuid


class Volceengine_app(BaseModel):
    appid: str  
    token: str
    cluster: str

class Volceengine_user(BaseModel):
    uid: str = "388808087185088"

class Volceengine_audio(BaseModel):
    voice_type: str
    encoding: str = "mp3"
    speed_ratio: float = 1.0
    volume_ratio: float = 1.0
    pitch_ratio: float = 1.0

class Volceengine_req_request(BaseModel):
    reqid: str = str(uuid.uuid4())
    text: str
    text_type: str = "plain"
    operation: str = "query"
    with_frontend: int = 1
    frontend_type: str = "unitTson"

class Volceengine_req_body(BaseModel):
    app: Volceengine_app  
    user: Volceengine_user
    audio: Volceengine_audio
    request: Volceengine_req_request