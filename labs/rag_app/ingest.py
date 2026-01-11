import os
import glob
from pathlib import Path
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_core.documents import Document

MODEL = "gpt-4.1-nano"
DB_NAME = str(Path(__file__).parent.parent / "vector_db_openai_embeddings")
KNOWLEDGE_BASE = str(Path(__file__).parent.parent.parent / "knowledge-base")
print(KNOWLEDGE_BASE)
load_dotenv(override=True)


# Use Directory Loader to load all md file from knowledge base in a list of Document objects
def fetch_documents() -> list[Document]:
    folders = glob.glob(str(Path(KNOWLEDGE_BASE) / "*"))
    documents = []
    for folder in folders:
        doc_type = os.path.basename(folder)
        loader = DirectoryLoader(
            folder, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={"encoding": "utf-8"}
        )
        folder_docs = loader.load()
        for doc in folder_docs:
            doc.metadata["doc_type"] = doc_type
            documents.append(doc)
    return documents

# Use RecursiveCharacterTextSplitter to split the documents into chunks of 500 characters with 200 character overlap
def create_chunks(documents) -> list[Document]:
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    return chunks

# Create a vector store with the embeddings
def create_vector_store_with_embeddings(chunks, embeddings):
    if os.path.exists(DB_NAME):
        Chroma(persist_directory=DB_NAME, embedding_function=embeddings).delete_collection()

    vectorstore = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=DB_NAME
    )

    collection = vectorstore._collection
    count = collection.count()
    
    # use a sample embedding to get the dimensions of the vector store
    sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
    dimensions = len(sample_embedding)
    print(f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store")
    return vectorstore


if __name__ == "__main__":
    print("Ingesting data...")
    documents: list[Document] = fetch_documents()
    print(f"Found {len(documents)} documents")

    chunks: list[Document] = create_chunks(documents)
    print(f"Created {len(chunks)} chunks")
    print(chunks[0])
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    vectorstore:Chroma = create_vector_store_with_embeddings(chunks, embeddings)
    print(f"Vector store created with {vectorstore._collection.count()} documents")
    
    print("Ingestion complete")