import chromadb
from sentence_transformers import SentenceTransformer
import os

os.environ["TRANSFORMERS_NO_TORCHVISION"] = "1"
os.environ["ANONYMIZED_TELEMETRY"] = "False"

model = None
collection = None

def init_db():
    global model, collection

    if model is None:
        model = SentenceTransformer('all-MiniLM-L6-v2')

        client = chromadb.Client()
        collection = client.get_or_create_collection(name="security_policies")

        docs = load_data()

        for i, doc in enumerate(docs):
            embedding = model.encode(doc).tolist()
            collection.add(documents=[doc], embeddings=[embedding], ids=[str(i)])