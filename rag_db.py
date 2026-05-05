import chromadb
from sentence_transformers import SentenceTransformer
import os

os.environ["TRANSFORMERS_NO_TORCHVISION"] = "1"
os.environ["ANONYMIZED_TELEMETRY"] = "False"

model = None
collection = None


def load_data():
    docs = []
    for file in ["data/GDPR.txt", "data/OWASP.txt", "data/CIS.txt"]:
        with open(file, "r") as f:
            content = f.read()
            sections = content.split("\n\n")
            for section in sections:
                if len(section.strip()) > 50:
                    docs.append(section.strip())
    return docs


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

def retrieve(query):
    init_db()

    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    return results["documents"][0]