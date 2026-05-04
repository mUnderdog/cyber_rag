import mlflow

evaluation_data = [
    {
        "question": "What is broken access control?",
        "expected_keywords": ["unauthorized", "access", "authorization"]
    },
    {
        "question": "How to prevent injection attacks?",
        "expected_keywords": ["input validation", "parameterized", "queries"]
    },
    {
        "question": "What is GDPR data minimisation?",
        "expected_keywords": ["data", "necessary", "minimal"]
    },
    {
        "question": "What is phishing?",
        "expected_keywords": []  # should NOT exist → hallucination test
    }
]


from rag_chat import get_rag_response

def  evaluate():
    results = []
    
    for item in evaluation_data:
        with mlflow.start_run():
            question = item["question"]
            expected_keywords = item["expected_keywords"]
            
            response = get_rag_response(question).lower()

            print("\n===================")
            print("Question: ", question)
            print("Response: ", response)

            if not expected_keywords:
                if "i don't know" in response:
                    score = 1
                else:
                    score = 0
            
            else:
                match_count = sum(1 for word in expected_keywords if word in response)
                score = match_count/len(expected_keywords)

            mlflow.log_param("question", question)
            mlflow.log_metric("score", score)

            results.append(score)

    avg_score = sum(results)/len(results)
    print("\nFinal Score: ", avg_score)

evaluate()