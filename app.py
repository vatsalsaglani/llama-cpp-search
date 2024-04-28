from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api_schemas import ChatPayload
from search_gen import search, llm

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def index():
    return {"ok": True}


@app.post("/api/chat")
async def api_chat(payload: ChatPayload):
    if payload.resp_type == "complete":
        op = llm.__complete__(payload.messages, max_tokens=payload.max_tokens)
        return {"ok": True, "text": op}
    elif payload.resp_type == "stream":
        return StreamingResponse(llm.__stream__(payload.messages,
                                                max_tokens=payload.max_tokens),
                                 media_type="text/event-stream")


@app.get("/search")
async def api_search(q: str):
    return StreamingResponse(search(q), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run("app:app", port=8900, host="0.0.0.0")
