from fastapi import HTTPException
from fastapi import FastAPI
from pydantic import BaseModel

from rag_chat import get_rag_response
from evaluation import evaluate

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI Security Policy Assistant", description=" RAG-based Assistant for Cyber Security Policies")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(request: ChatRequest):
    try:
           response = get_rag_response(request.message)
           return {
            "query": request.message,
            "response": response
           }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
@app.get("/evaluate")
def run_evaluation():
    evaluate()
    return {"message": "Evaluation completed. Check logs."}

@app.get("/health")
def health():
    return {"status": "running"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)