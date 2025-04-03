import requests
import json

# 🔹 LM Studio API URL (Ensure LM Studio is running)
LMSTUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

# 🔹 Define function to communicate with LM Studio
def query_lmstudio(model, messages):
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.3,  # Maintain professional tone
        "max_tokens": 400
    }
    
    response = requests.post(LMSTUDIO_API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"

# 🔹 Step 1: Take user legal query
def get_user_query():
    return input("Enter your legal query: ")

# 🔹 Step 2: Summarize the query while ensuring compliance
def summarize_query(user_query):
    messages = [
        {"role": "system", "content": 
            "You are a professional legal consultant specializing in tax law and compliance. "
            "Your role is to summarize legal matters in an informative way, ensuring neutrality and professionalism."},
        {"role": "user", "content": f"Summarize this legal situation without making assumptions about intent:\n\n{user_query}"}
    ]
    return query_lmstudio("Llama-3.2-1B-Instruct-Q8_0-GGUF/llama-3.2-1b-instruct-q8_0.gguf", messages)

# 🔹 Step 3: Suggest legal measures while avoiding rejection
def suggest_legal_measures(summary):
    messages = [
        {"role": "system", "content": 
            "You are a legal expert providing information on tax regulations and compliance. "
            "Provide a detailed response outlining general legal measures, emphasizing tax compliance and resolution strategies."},
        {"role": "user", "content": f"Provide a structured legal analysis and resolution options for this case:\n\n{summary}"}
    ]
    return query_lmstudio("Llama-3.2-1B-Instruct-Q8_0-GGUF/llama-3.2-1b-instruct-q8_0.gguf", messages)

# 🔹 Step 4: Recommend a tax lawyer
def recommend_lawyer():
    lawyers = [
        {"name": "Advocate Ramesh Gupta", "specialty": "Tax & Financial Law", "contact": "+91-9887765432"},
        {"name": "Advocate Priya Sharma", "specialty": "Corporate & Tax Law", "contact": "+91-9234567890"},
        {"name": "Advocate Arjun Mehta", "specialty": "Business Compliance Law", "contact": "+91-9012345678"}
    ]
    return lawyers[1]  # Select a relevant lawyer

# 🔹 Run the AI Lawyer Assistance System
if __name__ == "__main__":
    user_query = get_user_query()  # Step 1
    summary = summarize_query(user_query)  # Step 2
    legal_advice = suggest_legal_measures(summary)  # Step 3
    lawyer = recommend_lawyer()  # Step 4
    
    # 🔹 Output results
    print("\n🔹 **Case Summary:**\n", summary)
    print("\n🔹 **Legal Analysis & Suggested Measures:**\n", legal_advice)
    print("\n🔹 **Recommended Legal Counsel:**", lawyer["name"], "-", lawyer["specialty"], "\n   📞 Contact:", lawyer["contact"])
