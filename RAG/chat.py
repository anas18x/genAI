from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import os
from dotenv import load_dotenv
load_dotenv()
from groq import Groq

embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
)    

vector_db = QdrantVectorStore.from_existing_collection(
        url = os.getenv("url"),
        collection_name="rag-demo",
        api_key = os.getenv("QDRANT_API_KEY"),
        embedding= embedding_model
)


# use query
user_query = input("💭 ask something : ")

# Relevant chunks from the vector db
search_result = vector_db.similarity_search(query=user_query)

SYSTEM_PROMPT = f"""
you are a helpful assistant. answer the question based on the context retreived from a PDF file along with page_contents and page number.

you should answer the question based on the context provided. If the question is not related to the context, say sorry I can only answer questions related to the context.

context: {search_result}
"""

response = Groq(api_key=os.getenv("GROQ_API_KEY")).chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query},
    ],
)

print("🤖 -> : ", response.choices[0].message.content)