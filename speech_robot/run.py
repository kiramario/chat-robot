from fastapi import FastAPI
from starlette.responses import JSONResponse
import uvicorn, asyncio
import time

app = FastAPI()

@app.get("/helloword")
def helloword():
    return JSONResponse(content={"message": "Hello, world"})

@app.get("/terrible_ping")
async def terrible_ping():
    time.sleep(10) # I/O blocking operation for 10 seconds, the whole process will be blocked
    
    return {"pong": True}

@app.get("/good_ping")
def good_ping():
    time.sleep(10) # I/O blocking operation for 10 seconds, but in a separate thread for the whole `good_ping` route

    return {"pong": True}

@app.get("/perfect_ping")
async def perfect_ping():
    await asyncio.sleep(10) # non-blocking I/O operation

    return {"pong": True}

if __name__ == "__main__":
    uvicorn.run("run:app", port=5000, log_level="info")