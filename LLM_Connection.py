import requests

# LM Studio API URL (Change if running on a different port)
LMSTUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

# Read CSV file as text
file_path = "laws.csv"  # Ensure the path is correct
with open(file_path, "r", encoding="utf-8") as file:
    csv_content = file.read()

# Define API request payload
lmstudio_payload = {
    "model": "Llama-3.2-1B-Instruct-Q8_0-GGUF/llama-3.2-1b-instruct-q8_0.gguf",  # Adjust based on active model
    "messages": [{
        "role": "user",
        "content": f"""
        Analyze the following legal dataset (CSV format) and suggest rare laws for each profession.

        ### Data (CSV format):
        {csv_content}

        ### Task:
        1. Identify laws that are **rarely cited** for Doctor profession.
        2. Explain why these laws might be less commonly referenced.
        3. Provide **insights** on how these rare laws impact legal practice.
        4. Suggest potential **scenarios** where these laws could be relevant.

        Provide structured reasoning for each profession.
        """
    }],
    "temperature": 0.7,
    "max_tokens": 1000  # Adjust based on response length needed
}

# Send request to LM Studio
response = requests.post(LMSTUDIO_API_URL, headers={"Content-Type": "application/json"}, json=lmstudio_payload)

# Print response
if response.status_code == 200:
    print(response.json()["choices"][0]["message"]["content"])  # Extract response text
else:
    print(f"Error {response.status_code}: {response.text}")
