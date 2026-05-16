from langchain_core.prompts import PromptTemplate

rag_prompt = PromptTemplate.from_template("""
Answer from the provided context only. If you don't know the answer just say `I dont't know'.
                                          
<context>
{context}
</context>

<question>
{question}
</question>
""")