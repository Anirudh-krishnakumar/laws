# LawSnap

LawSnap is an AI-powered legal awareness platform that helps users
discover rare Indian laws, understand legal concepts in simple language,
and test their knowledge through interactive quizzes. The platform
leverages Large Language Models (LLMs) running locally through LM Studio
to provide intelligent legal assistance while keeping inference local.

## Features

### Rare Law Finder

-   Discover profession-specific rare Indian laws
-   AI-generated explanations
-   Multilingual support
-   Simple, easy-to-understand legal insights

### AI Lawyer Assistance

-   Ask legal questions in natural language
-   Receive concise AI-generated legal summaries
-   Simplifies complex legal terminology

### Rare Law Quiz

-   AI-generated multiple-choice questions
-   Profession-based quizzes
-   Reward points system
-   Detailed legal explanations after every answer
-   Retry and progress tracking

### Legal References

-   AI-generated explanations with legal context
-   Practical examples
-   References to constitutional provisions, statutes, and landmark
    judgments

## Technology Stack

-   Python
-   Streamlit
-   Pandas
-   LM Studio
-   Llama 3.2 1B Instruct (GGUF)
-   Requests
-   Regular Expressions

## Project Structure

``` text
LawSnap/
│── app.py
│── laws.csv
│── requirements.txt
│── README.md
└── assets/
```

## Installation

### Clone the repository

``` bash
git clone https://github.com/Anirudh-krishnakumar/LawSnap.git
cd LawSnap
```

### Install dependencies

``` bash
pip install -r requirements.txt
```

### Install and Start LM Studio

1.  Install LM Studio.
2.  Download the **Llama-3.2-1B-Instruct-Q8_0-GGUF** model.
3.  Start the local server at:

```{=html}
<!-- -->
```
    http://localhost:1234

### Run the application

``` bash
streamlit run app.py
```

## Dataset

The application uses a CSV dataset containing:

-   Profession
-   Law Name
-   Description

The dataset powers both the Rare Law Finder and the AI-generated
quizzes.

## Workflow

1.  User selects a profession.
2.  A relevant law is retrieved from the dataset.
3.  The selected law is sent to the local LLM.
4.  The AI generates:
    -   Law explanation
    -   Quiz question
    -   Multiple-choice options
    -   Legal references
    -   Practical examples
5.  Users earn points by answering quizzes correctly.

## Future Enhancements

-   Voice-based legal assistant
-   OCR support for legal documents
-   Case law search
-   Lawyer recommendation system
-   Document summarization
-   User authentication
-   Leaderboard

## Screenshots

Add screenshots for: - Home Page - Rare Law Finder - AI Lawyer
Assistance - Rare Law Quiz - Legal Explanation

## Requirements

-   Python 3.10+
-   Streamlit
-   Pandas
-   Requests
-   LM Studio
-   Llama 3.2 GGUF Model

## Disclaimer

LawSnap is intended for educational and legal awareness purposes only.
The generated content should not be considered professional legal
advice. Users should consult a qualified legal professional for official
legal guidance.

## License

This project is licensed under the MIT License.

## Author

**Anirudh Krishnakumar**

GitHub: https://github.com/Anirudh-krishnakumar
