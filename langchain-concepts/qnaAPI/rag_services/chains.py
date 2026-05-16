from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from .prompts import rag_prompt

llm = ChatOllama(model="llama3.1:latest", temperature=0.4, )
parser = StrOutputParser()

rag_chain = rag_prompt | llm | parser
