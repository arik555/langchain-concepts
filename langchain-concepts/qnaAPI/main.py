from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from .rag_services.core import ask_question


app = FastAPI()

@app.get(path="/chat")
async def chat(question: str):
    return StreamingResponse(
        content=ask_question(question=question),
        media_type="text/event-stream",
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app)