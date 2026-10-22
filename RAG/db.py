from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Document
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("api_key")
url = os.getenv("url")

# connect to Qdrant Cloud
client = QdrantClient(
    url=url,
    api_key=api_key,
    cloud_inference=True
)