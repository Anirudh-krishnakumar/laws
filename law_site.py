import streamlit as st
import requests
import pandas as pd
import json

# 🔹 LM Studio API URL (Ensure LM Studio is running)
LMSTUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

# 🔹 Load CSV for rare laws
CSV_FILE_PATH = "laws.csv"  # Ensure this file exists in the backend
laws_df = pd.read_csv(CSV_FILE_PATH)

# 🔹 Function to query LM Studio
def query_lmstudio(model, messages):
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 400
    }
    
    response = requests.post(LMSTUDIO_API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"

# 🔹 Function to fetch rare laws based on profession
def get_rare_laws(profession, language):
    filtered_laws = laws_df[laws_df["Profession"] == profession]
    csv_content = filtered_laws.to_csv(index=False)
    
    messages = [{
        "role": "user",
        "content": f"""
        Analyze the following legal dataset (CSV format) and suggest rare laws for the profession: {profession}.
        Provide results in {language}.

        ### Data (CSV format):
        {csv_content}

        ### Task:
        1. Identify laws that are **rarely cited** for {profession}.
        2. Explain why these laws might be less commonly referenced.
        3. Provide **insights** on how these rare laws impact legal practice.
        4. Suggest potential **scenarios** where these laws could be relevant.

        Provide structured reasoning in {language}.
        """
    }]
    
    return query_lmstudio("Llama-3.2-1B-Instruct-Q8_0-GGUF", messages)

# 🔹 Function to handle AI Lawyer Assistance
def get_legal_assistance(user_query):
    summary = query_lmstudio("Llama-3.2-1B-Instruct-Q8_0-GGUF", [
        {"role": "system", "content": "You are a professional legal consultant. Summarize this legal case formally."},
        {"role": "user", "content": f"Summarize this legal situation:\n\n{user_query}"}
    ])

    legal_measures = query_lmstudio("Llama-3.2-1B-Instruct-Q8_0-GGUF", [
        {"role": "system", "content": "You are an AI lawyer providing structured legal solutions."},
        {"role": "user", "content": f"Provide legal analysis and solutions for:\n\n{summary}"}
    ])

    return summary, legal_measures

# 🔹 Streamlit UI
st.title("LawSnap - AI Legal Platform")

# 🔹 Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["📜 Rare Law Finder", "⚖️ AI Lawyer Assistance"])

# 🔹 Page 1: Rare Law Finder
if page == "📜 Rare Law Finder":
    st.header("📜 Discover Rare Laws Based on Your Profession")
    
    profession = st.selectbox("Select Your Profession", laws_df["Profession"].unique())
    language = st.selectbox("Select Preferred Language", ["English", "Hindi", "Tamil", "Telugu", "Bengali"])
    
    if st.button("Get Rare Laws"):
        rare_laws = get_rare_laws(profession, language)
        st.subheader("🔍 AI-Generated Rare Law Insights:")
        st.write(rare_laws)

# 🔹 Page 2: AI Lawyer Assistance
elif page == "⚖️ AI Lawyer Assistance":
    st.header("⚖️ AI-Powered Lawyer Assistance")
    
    user_query = st.text_area("Enter your legal query:")
    
    if st.button("Get Legal Assistance"):
        summary, legal_measures = get_legal_assistance(user_query)
        
        st.subheader("📄 Case Summary:")
        st.write(summary)
        
        st.subheader("🛡️ Legal Analysis & Suggested Measures:")
        st.write(legal_measures)
