from groq import Groq
from rag_db import retrieve
import time
import mlflow
import os


client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_rag_response(user_query: str):
    with mlflow.start_run():
        start = time.time()
        contexts = retrieve(user_query)
        
        if not contexts:
            return "No relevant policy information found."

        contexts = sorted(contexts, key=lambda x: len(x), reverse=True)    

        contexts = [c for c in contexts if len(c) > 50]

        print("\n=== RETRIEVED CHUNKS ===")
        for i, c in enumerate(contexts):
            print(f"[{i+1}] {c[:200]}...\n")

        context_text = "\n\n".join(contexts[:3])

        mlflow.log_param("context", context_text[:500])

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
        "role": "system",
        "content": f"""
    You are a cybersecurity expert assistant.

    You must follow these rules:
    1. Answer ONLY using the provided context.
    2. If the answer is not present, say:
    "I don't know based on the provided policies."
    3. Be precise, structured, and technical.
    4. Do NOT make assumptions.
    5. If context is insufficient or unclear, do NOT guess.

    Format your answer like this:

    Definition:
    <clear explanation>

    Example:
    <real-world example>

    Prevention / Recommendation:
    <actionable steps>

    Context:
    {context_text}
    """
    },
                {
                    "role": "user",
                    "content": user_query
                }
            ]
        )

        result = response.choices[0].message.content

        end = time.time()
        latency = end-start
        print("Response Time: ", latency)

        mlflow.log_metric("latency", latency)
        mlflow.log_metric("context_len", len(context_text))

        return result

print(get_rag_response("What is broken access control?"))