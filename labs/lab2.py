import os
import glob
import tiktoken
import numpy as np
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sklearn.manifold import TSNE
import plotly.graph_objects as go

MODEL = "gpt-4.1-nano"
db_name = "vector_db"
load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')
if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")
    

def load_kb_as_string():
    # How many characters in all the documents?
    knowledge_base_path = "knowledge-base/**/*.md"
    files = glob.glob(knowledge_base_path, recursive=True)
    print(f"Found {len(files)} files in the knowledge base")
    entire_knowledge_base = ""

    for file_path in files:
        print(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            entire_knowledge_base += f.read()
            entire_knowledge_base += "\n\n"

    print(f"Total characters in knowledge base: {len(entire_knowledge_base):,}")
    return entire_knowledge_base

def get_token_count(text):
    # How many tokens in all the documents?
    encoding = tiktoken.encoding_for_model(MODEL)
    tokens = encoding.encode(entire_knowledge_base)
    token_count = len(tokens)
    print(f"Total tokens for {MODEL}: {token_count:,}")
    return token_count

def load_kb_as_documents():
    # Load in everything in the knowledgebase using LangChain's loaders
    folders = glob.glob("knowledge-base/*")
    documents = []
    for folder in folders:
        doc_type = os.path.basename(folder)
        loader = DirectoryLoader(folder, glob="**/*.md", loader_cls=TextLoader, loader_kwargs={'encoding': 'utf-8'})
        folder_docs = loader.load()
        print(folder_docs)
        for doc in folder_docs:
            doc.metadata["doc_type"] = doc_type
            documents.append(doc)
    print(f"Loaded {len(documents)} documents")
    return documents

def get_chunks(documents: list):
    # Divide into chunks using the RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    print(f"Divided into {len(chunks)} chunks")
    print(f"First chunk:\n\n{chunks[0]}")
    return chunks


def get_vector_store(chunks: list):
    # Pick an embedding model
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    #embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

    if os.path.exists(db_name):
        Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()

    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=db_name)
    print(f"Vectorstore created with {vectorstore._collection.count()} documents")
    return vectorstore

def investigate_vector_store(vectorstore: Chroma):
    # Let's investigate the vectors
    collection = vectorstore._collection
    count = collection.count()
    sample_embedding = collection.get(limit=1, include=["embeddings"])["embeddings"][0]
    dimensions = len(sample_embedding)
    print(f"There are {count:,} vectors with {dimensions:,} dimensions in the vector store")


class VisualizationData:
    def __init__(self, vectorstore: Chroma):
        self.vectorstore = vectorstore
        self.collection = vectorstore._collection
        self.result = self.collection.get(include=['embeddings', 'documents', 'metadatas'])
        self.vectors = np.array(self.result['embeddings'])
        self.documents = self.result['documents']
        self.metadatas = self.result['metadatas']
        self.doc_types = [metadata['doc_type'] for metadata in self.metadatas]
        self.colors = [['blue', 'green', 'red', 'orange'][['products', 'employees', 'contracts', 'company'].index(t)] for t in self.doc_types]

def visualize_2d(visualization_data: VisualizationData):
    # Reduce the dimensionality of the vectors to 2D using t-SNE
    # (t-distributed stochastic neighbor embedding)
    tsne = TSNE(n_components=2, random_state=42)
    reduced_vectors = tsne.fit_transform(visualization_data.vectors)
    # Create the 2D scatter plot
    fig = go.Figure(data=[go.Scatter(
        x=reduced_vectors[:, 0],
        y=reduced_vectors[:, 1],
        mode='markers',
        marker=dict(size=5, color=visualization_data.colors, opacity=0.8),
        text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(visualization_data.doc_types, visualization_data.documents)],
        hoverinfo='text'
    )])

    fig.update_layout(title='2D Chroma Vector Store Visualization',
        scene=dict(xaxis_title='x',yaxis_title='y'),
        width=800,
        height=600,
        margin=dict(r=20, b=10, l=10, t=40)
    )

    fig.show()


def visualize_3d(visualization_data: VisualizationData):
    tsne = TSNE(n_components=3, random_state=42)
    reduced_vectors = tsne.fit_transform(visualization_data.vectors)
    # Create the 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
        x=reduced_vectors[:, 0],
        y=reduced_vectors[:, 1],
        z=reduced_vectors[:, 2],
        mode='markers',
        marker=dict(size=5, color=visualization_data.colors, opacity=0.8),
        text=[f"Type: {t}<br>Text: {d[:100]}..." for t, d in zip(visualization_data.doc_types, visualization_data.documents)],
        hoverinfo='text'
    )])

    fig.update_layout(
        title='3D Chroma Vector Store Visualization',
        scene=dict(xaxis_title='x', yaxis_title='y', zaxis_title='z'),
        width=900,
        height=700,
        margin=dict(r=10, b=10, l=10, t=40)
    )

    fig.show()

if __name__ == "__main__":
    # entire_knowledge_base: str = load_kb_as_string()
    # print(entire_knowledge_base)
    # token_count:int = get_token_count(entire_knowledge_base)
    # print(f"Token count: {token_count}")
    
    # Load the documents and create the vector store
    documents: list = load_kb_as_documents()
    # print(documents[1].page_content)
    # print(documents[1].metadata)
    chunks: list = get_chunks(documents)
    vectorstore: Chroma = get_vector_store(chunks)
    investigate_vector_store(vectorstore)
    
    visualization_data = VisualizationData(vectorstore)
    # visualize_2d(visualization_data)
    visualize_3d(visualization_data)