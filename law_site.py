import streamlit as st
import requests
import pandas as pd
import re
import json

# 🔹 LM Studio API URL
LMSTUDIO_API_URL = "http://localhost:1234/v1/chat/completions"

# 🔹 Load CSV for rare laws
CSV_FILE_PATH = "laws.csv"
laws_df = pd.read_csv(CSV_FILE_PATH)

# 🔹 Initialize session state
if "quiz_question" not in st.session_state:
    st.session_state.quiz_question = None
    st.session_state.options = []
    st.session_state.correct_answer = None
    st.session_state.law_title = None
    st.session_state.selected_option = None
    st.session_state.quiz_submitted = False

# 🔹 Function to query LM Studio
def query_lmstudio(model, messages):
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 500
    }
    
    response = requests.post(LMSTUDIO_API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(payload))
    
    if response.status_code == 200:
        try:
            response_json = response.json()
            return response_json["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Error parsing response: {str(e)}"
    else:
        return f"❌ LM Studio Error: {response.status_code} - {response.text}"

# 🔹 Function to generate quiz
# 🔹 Function to generate quiz
def generate_quiz(profession, language):
    filtered_laws = laws_df[laws_df["Profession"] == profession]
    
    if filtered_laws.empty:
        return None, None, None, None

    rare_law = filtered_laws.sample(1).iloc[0]  
    law_title = rare_law["Law Name"]
    law_description = rare_law["Description"]

    messages = [{
        "role": "user",
        "content": f"""
        Based on the following rare law, create a **multiple-choice question (MCQ)** with **4 options**:

        **Law:** {law_title}
        **Description:** {law_description}

        Ensure one option is correct, and provide the answer separately.
        Format the response as:
        - **Question:** [MCQ question]
        - **Options:**
          1. [Option Text]
          2. [Option Text]
          3. [Option Text]
          4. [Option Text]
        - **Correct Answer:** [Correct option number]
        """
    }]

    response = query_lmstudio("Llama-3.2-1B-Instruct-Q8_0-GGUF", messages)
    
    # Print the raw response for debugging
    print(f"Raw LLM response: {response}")
    
    if not response:
        return None, None, None, None

    try:
        # Split by newlines and clean up
        lines = [line.strip() for line in response.split('\n') if line.strip()]
        
        # Extract question
        question = None
        for line in lines:
            if "**Question:**" in line or "Question:" in line:
                question = line.replace("**Question:**", "").replace("Question:", "").strip()
                break
        
        if not question:
            print("Failed to extract question")
            return None, None, None, None
        
        # Extract options
        options = []
        option_pattern = re.compile(r'^\s*(\d+)\.\s+(.+)$')
        
        for line in lines:
            match = option_pattern.match(line)
            if match:
                option_number = int(match.group(1))
                option_text = match.group(2).strip()
                
                # Make sure we store options in the right order
                while len(options) < option_number - 1:
                    options.append("")  # Placeholder for missing options
                
                options.append(option_text)
        
        # Check if we have exactly 4 options
        if len(options) != 4:
            print(f"Expected 4 options, but got {len(options)}")
            return None, None, None, None
        
        # Extract correct answer
        correct_answer = None
        for line in lines:
            if "**Correct Answer:**" in line or "Correct Answer:" in line:
                try:
                    answer_part = line.split(":")[-1].strip()
                    correct_answer = int(re.search(r'(\d+)', answer_part).group(1))
                    break
                except (ValueError, AttributeError) as e:
                    print(f"Error extracting correct answer: {e}")
        
        if not correct_answer or correct_answer < 1 or correct_answer > 4:
            print(f"Invalid correct answer: {correct_answer}")
            return None, None, None, None
        
        return law_title, question, options, correct_answer

    except Exception as e:
        print(f"Error in generate_quiz: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None, None, None

# 🔹 Function to get explanation of the rare law
def get_explanation(law_title, law_description):
    messages = [
        {"role": "system", "content": "You are a legal expert specializing in Indian law."},
        {"role": "user", "content": f"""
        Provide a detailed explanation of this law with legal references:
        
        Law: {law_title}
        Description: {law_description}
        
        Your response should include:
        1. A clear explanation of the law in simple terms
        2. At least one practical example of how this law applies
        3. References to relevant sections of the Indian Constitution, statutes, or landmark court cases
        4. Formatted with proper citations in the style of Indian legal textbooks
        """
        }
    ]
    return query_lmstudio("Llama-3.2-1B-Instruct-Q8_0-GGUF", messages)

# 🔹 Streamlit UI
st.title("LawSnap - AI Legal Platform")

# 🔹 Sidebar for Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["📜 Rare Law Finder", "⚖️ AI Lawyer Assistance", "🎯 Rare Law Quiz"])

# 🔹 Page 1: Rare Law Finder
if page == "📜 Rare Law Finder":
    st.header("📜 Discover Rare Laws Based on Your Profession")
    
    profession = st.selectbox("Select Your Profession", laws_df["Profession"].unique())
    language = st.selectbox("Select Preferred Language", ["English", "Hindi", "Tamil", "Telugu", "Bengali"])
    
    if st.button("Get Rare Laws"):
        rare_laws = query_lmstudio("Llama-3.2-1B-Instruct-Q8_0-GGUF", [
            {"role": "system", "content": "Provide rare laws related to this profession."},
            {"role": "user", "content": f"Find rare laws for {profession} in {language}"}
        ])
        st.subheader("🔍 AI-Generated Rare Law Insights:")
        st.write(rare_laws)

# 🔹 Page 2: AI Lawyer Assistance
elif page == "⚖️ AI Lawyer Assistance":
    st.header("⚖️ AI-Powered Lawyer Assistance")
    
    user_query = st.text_area("Enter your legal query:")
    
    if st.button("Get Legal Assistance"):
        summary = query_lmstudio("Llama-3.2-1B-Instruct-Q8_0-GGUF", [
            {"role": "system", "content": "You are a legal assistant summarizing legal queries."},
            {"role": "user", "content": f"Summarize this query: {user_query}"}
        ])
        st.subheader("📄 Case Summary:")
        st.write(summary)

# 🔹 Page 3: Rare Law Quiz
# Initialize reward points in session state
# Initialize reward points in session state
if "reward_points" not in st.session_state:
    st.session_state.reward_points = 0
    st.session_state.quiz_attempts = 0
    st.session_state.current_quiz_id = None
    st.session_state.answered_quizzes = {}  # Track quiz attempts and correct answers

# Add this to the Rare Law Quiz section
if page == "🎯 Rare Law Quiz":
    st.header("🎯 Test Your Knowledge on Rare Laws")
    
    # Display the user's current points and attempts
    col1, col2 = st.columns(2)
    with col1:
        st.metric("🏆 Your Points", st.session_state.reward_points)
    with col2:
        st.metric("🔄 Quiz Attempts", st.session_state.quiz_attempts)
    
    st.markdown("---")
    
    profession = st.selectbox("Select Your Profession for Quiz", laws_df["Profession"].unique())
    language = st.selectbox("Select Language for Quiz", ["English", "Hindi", "Tamil", "Telugu", "Bengali"])
    
    if st.button("Start Quiz"):
        # Generate a unique ID for this quiz
        import uuid
        quiz_id = str(uuid.uuid4())
        st.session_state.current_quiz_id = quiz_id
        
        # Only increment attempts for new quizzes
        if quiz_id not in st.session_state.answered_quizzes:
            st.session_state.quiz_attempts += 1
            st.session_state.answered_quizzes[quiz_id] = {"attempts": 1, "correct_answer_given": False}
        
        filtered_laws = laws_df[laws_df["Profession"] == profession]
        if not filtered_laws.empty:
            rare_law = filtered_laws.sample(1).iloc[0]
            law_title = rare_law["Law Name"]
            law_description = rare_law["Description"]
            
            # Generate quiz using this law
            law_title, question, options, correct_answer = generate_quiz(profession, language)

            if question and options and correct_answer:
                st.session_state.quiz_question = question
                st.session_state.options = options
                st.session_state.correct_answer = correct_answer
                st.session_state.law_title = law_title
                st.session_state.law_description = law_description
                st.session_state.quiz_submitted = False
                st.session_state.explanation = None
                st.rerun()
            else:
                st.error("Failed to generate a quiz. Please try again.")

    if st.session_state.quiz_question:
        st.subheader(f"📝 Quiz on: **{st.session_state.law_title}**")
        
        # If the user has attempted this quiz before, show the number of attempts
        quiz_id = st.session_state.current_quiz_id
        if quiz_id in st.session_state.answered_quizzes and st.session_state.answered_quizzes[quiz_id]["attempts"] > 1:
            st.info(f"Attempts on this question: {st.session_state.answered_quizzes[quiz_id]['attempts']}")
        
        st.write(st.session_state.quiz_question)

        selected_option = st.radio("Select your answer:", st.session_state.options, key="quiz_radio")

        if st.button("Submit Answer"):
            if selected_option is not None:
                st.session_state.selected_option = selected_option
                st.session_state.quiz_submitted = True
                
                # Generate explanation if not already present
                if not st.session_state.get("explanation"):
                    with st.spinner("Generating legal explanation..."):
                        st.session_state.explanation = get_explanation(
                            st.session_state.law_title, 
                            st.session_state.get("law_description", "")
                        )
                st.rerun()

        if st.session_state.quiz_submitted:
            try:
                correct_index = st.session_state.correct_answer - 1
                is_correct = st.session_state.options[correct_index] == st.session_state.selected_option
                quiz_id = st.session_state.current_quiz_id
                
                # Check if we should award points (first correct answer for this quiz)
                if is_correct and not st.session_state.answered_quizzes[quiz_id]["correct_answer_given"]:
                    st.session_state.reward_points += 1
                    st.session_state.answered_quizzes[quiz_id]["correct_answer_given"] = True
                
                if is_correct:
                    if st.session_state.answered_quizzes[quiz_id]["attempts"] > 1:
                        st.success(f"✅ Correct Answer! +1 Point (After {st.session_state.answered_quizzes[quiz_id]['attempts']} attempts)")
                    else:
                        st.success("✅ Correct Answer! +1 Point")
                else:
                    st.error(f"❌ Incorrect. The correct answer is: {st.session_state.options[correct_index]}")
                
                # Display explanation
                if st.session_state.explanation:
                    st.markdown("---")
                    st.subheader("📚 Legal Explanation & References")
                    st.markdown(st.session_state.explanation)
                    
                    # Add citation box
                    st.markdown("""
                    <style>
                    .citation-box {
                        background-color: #f8f9fa;
                        border-left: 5px solid #6c757d;
                        padding: 10px 15px;
                        margin: 20px 0;
                        font-size: 0.9em;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f"""
                    <div class="citation-box">
                    <p><strong>How to cite:</strong></p>
                    <p>{st.session_state.law_title}, as explained in <em>Indian Constitutional Law</em>, 7th Edition, LexisNexis (2023)</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Add buttons for next actions
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("Try This Question Again"):
                        # Increment attempts for this quiz
                        st.session_state.answered_quizzes[quiz_id]["attempts"] += 1
                        # Reset only the submission state
                        st.session_state.quiz_submitted = False
                        st.rerun()
                
                with col2:
                    if st.button("Next Quiz"):
                        # Reset quiz state but keep points and attempts
                        st.session_state.quiz_question = None
                        st.session_state.options = []
                        st.session_state.correct_answer = None
                        st.session_state.law_title = None
                        st.session_state.selected_option = None
                        st.session_state.quiz_submitted = False
                        st.session_state.explanation = None
                        st.session_state.current_quiz_id = None
                        st.rerun()
                    
            except Exception as e:
                st.error(f"Error displaying results: {str(e)}")
                import traceback
                st.exception(traceback.format_exc())