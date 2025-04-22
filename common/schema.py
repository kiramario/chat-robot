from pydantic import BaseModel
from enum import Enum

class Left(BaseModel):
    res: list[tuple] = []

class Right(BaseModel):
    msg: str = "failed"




if __name__ == "__main__":
    e1 = Left(res=[(1, "u1")])
    e1 = Right(msg="error")
    e1 = Right()



    match e1:
        case Left(res=res):
            print(res)
        case Right(msg=msg):
            print(f"r {msg}")
        case _:
            print("other")

    pass