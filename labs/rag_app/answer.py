from pathlib import Path
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, convert_to_messages
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv(override=True)

MODEL = "gpt-4.1-nano"
DB_NAME = str(Path(__file__).parent.parent / "vector_db_openai_embeddings")

RETRIEVAL_K = 10

retriever = None
llm = None

SYSTEM_PROMPT = """
You are a knowledgeable, friendly assistant representing the company Insurellm.
You are chatting with a user about Insurellm.
If relevant, use the given context to answer any question.
If you don't know the answer, say so.
Context:
{context}
"""

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
vectorstore:Chroma = Chroma(persist_directory=DB_NAME, embedding_function=embeddings)
retriever = vectorstore.as_retriever()
llm:ChatOpenAI = ChatOpenAI(temperature=0, model_name=MODEL)


def fetch_context(question: str) -> list[Document]:
    """
    Retrieve relevant context documents for a question.
    """
    return retriever.invoke(question, k=RETRIEVAL_K)

def combined_question(question: str, history: list[dict] = []) -> str:
    """
    Combine all the user's messages into a single string.
    """
    prior = "\n".join(m["content"] for m in history if m["role"] == "user")
    return prior + "\n" + question

def answer_question(question: str, history: list[dict] = []) -> tuple[str, list[Document]]:
    """
    Answer the given question with RAG; return the answer and the context documents.
    Args:
        question: The current user question to answer
        history: List of previous conversation messages (from Gradio chatbot).
                 Each dict has "role" ("user" or "assistant") and "content" keys.
                 Used to provide context for better retrieval and conversation continuity.
    """
    combined = combined_question(question, history)
    docs = fetch_context(combined)
    context = "\n\n".join(doc.page_content for doc in docs)
    system_prompt = SYSTEM_PROMPT.format(context=context)
    messages = [SystemMessage(content=system_prompt)]
    messages.extend(convert_to_messages(history))
    messages.append(HumanMessage(content=question))
    response = llm.invoke(messages)
    return response.content, docs


if __name__ == "__main__":
    print("We assume we have a vector store with embeddings already created by the ingest.py script")
    
    context: list[Document] = fetch_context("Who is Averi Lancaster?")
    print(f"Found {len(context)} documents relevat to the context")
    [print(doc.metadata) for doc in context]
    
    response_without_history, context_without_history = answer_question("What is her salary", [])
    print(f"Answer without history: {response_without_history}")
    [print(doc.metadata) for doc in context_without_history]
    
    response_with_history, context_with_history = answer_question("What is her salary", [{"role": "user", "content": "Who is Averi Lancaster?"}, {"role": "assistant", "content": "Averi Lancaster is the CEO of Insurellm"}])
    print(f"Answer with history: {response_with_history}")
    [print(doc.metadata) for doc in context_with_history]
    