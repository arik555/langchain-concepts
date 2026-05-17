from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from .rag_services.core import ask_question
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # queue to hold the the requests in order
    app.state.request_queue = asyncio.Queue()

    # semaphore to strictly keep the concurrent requests under control
    app.state.concurrency_semaphore = asyncio.Semaphore(2)

    worker = asyncio.create_task(process_worker(app.state.request_queue, app.state.concurrency_semaphore))

    yield
    worker.cancel()
    app.state.request_queue = None
    app.state.concurrency_semaphore = None

app = FastAPI(lifespan=lifespan)

async def process_worker(queue: asyncio.Queue, semaphore: asyncio.Semaphore):
    while True:
        current_request, future_result = await queue.get()
        async with semaphore:
            try:
                question = current_request.query_params.get("question")
                print("Running Question", question)
                llm_call = ask_question(question=question)
                future_result.set_result(llm_call)
            except Exception as e:
                print(e)
                future_result.set_exception(e)
            finally:
                queue.task_done()


@app.get(path="/chat")
async def chat(request: Request):

    """
    1. Put the request into the Queue.
    2. Apply semaphores and get request to execute from the Queue.
    3. Immediately release the sempahore and return the streaming response.
    """

    print("Received Question", request.query_params.get("question"))

    request_queue = request.app.state.request_queue
    future_result = asyncio.get_running_loop().create_future()
    await request_queue.put((request, future_result))
    result = await future_result
        
    print("Answering Question", request.query_params.get("question"))
    return StreamingResponse(
        content=result,
        media_type="text/event-stream",
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, reload=True)