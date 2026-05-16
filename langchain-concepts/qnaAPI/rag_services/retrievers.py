from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

embeddings = OllamaEmbeddings(model="nomic-embed-text:v1.5", temperature=0)

vector_db = Chroma(collection_name="cricket_meta", embedding_function=embeddings, persist_directory="./langchain-concepts/rag/chroma_data/chroma_default_db")
retriver = vector_db.as_retriever(search_type="mmr", search_kwargs={"fetch_k": 50, "k": 5, "lambda_multi": 0.8})