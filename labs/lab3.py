from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_huggingface import HuggingFaceEmbeddings
import gradio as gr

load_dotenv(override=True)


def get_vector_store(db_name: str):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=db_name, embedding_function=embeddings)
    return vectorstore

SYSTEM_PROMPT_TEMPLATE = """
You are a knowledgeable, friendly assistant representing the company Insurellm.
You are chatting with a user about Insurellm.
If relevant, use the given context to answer any question.
If you don't know the answer, say so.
Context:
{context}
"""

def answer_question(question: str, history):
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=context)
    response = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=question)])
    return response.content

if __name__ == "__main__":
    DB_NAME = "vector_db"
    vectorstore = get_vector_store(DB_NAME)
    retriever = vectorstore.as_retriever()
    llm = ChatOpenAI(temperature=0, model_name="gpt-4.1-nano")  
    view = gr.ChatInterface(answer_question, type="messages").launch(inbrowser=True)