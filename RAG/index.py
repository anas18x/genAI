from pathlib import Path
import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()

pdf_path = Path(__file__).parent / "AnasShakil-14166.pdf"

loader = PyPDFLoader(
           file_path = pdf_path,
           mode = "single",
           pages_delimiter = "\n",
)

# Load the PDF and split it into pages
docs = loader.load()

# split the docs into small chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50, #
)
chunks = text_splitter.split_documents(documents=docs)
# print(chunks[0])
# print("Total chunks:", len(chunks))



# vector Embedding
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)    

# Store embeddings in Qdrant
vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url = os.getenv("url"),
    collection_name="rag-demo",
    api_key = os.getenv("QDRANT_API_KEY"),
)

print("Vector store created successfully!")