
from .retrievers import retriver
from .chains import rag_chain


async def ask_question(question: str):
    retrieved_docs = await retriver.ainvoke(question)

    context = "\n\n".join(doc.page_content for doc in retrieved_docs)

    async for each_chunk in rag_chain.astream(input={
        "context": context, "question": question
    }):
        # since StrOutput parser is added to the chain therefore already coming as text
        # otherwise, might have to use each_chunk.content
        if each_chunk:
            # \n\n for better readability.
            yield f"data: {each_chunk}\n\n"
    
    yield "data: [DONE]\n\n"