import streamlit as st
import pandas as pd
import requests
from duckduckgo_search import DDGS  # DuckDuckGo search API

# Groq API interaction function
def parse_with_groq_api(text, prompt):
    """Interact with Groq API to extract information based on the prompt."""
    groq_api_url = "https://api.groq.com/v1/completions"
    headers = {
        "Authorization": "Bearer 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",  # Replace with your Groq API key
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",  # Replace with the appropriate model
        "messages": [
            {"role": "system", "content": prompt},
            {"role": "user", "content": text},
        ],
        "max_tokens": 100  # Adjust based on your needs
    }

    try:
        response = requests.post(groq_api_url, headers=headers, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            return response_data['choices'][0]['message']['content']
        else:
            error_message = response.json().get("error", "Unknown error")
            return f"Error: {error_message}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {str(e)}"

# DuckDuckGo search API function
def get_search_results(query):
    """Search for the query using DuckDuckGo API."""
    if not query.strip():  # Ensure query is not empty
        return [{"title": "No results", "href": "", "body": "Query was empty"}]
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=3)
            return [
                {"title": r.get("title", ""), "href": r.get("href", ""), "body": r.get("body", "")}
                for r in results
            ]
    except Exception as e:
        return [{"title": "Error", "href": "", "body": str(e)}]

# Main function for Streamlit app
def main():
    st.title("AI Agent - Information Retriever")

    # Upload CSV or Google Sheets link input
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if not uploaded_file:
        st.warning("Please upload a CSV file to continue.")
        st.stop()

    # Load data from CSV
    try:
        data = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Error reading the file: {e}")
        st.stop()

    # Select the main entity column
    entity_column = st.selectbox("Select the primary column for entities", data.columns)

    # Input custom prompt with validation
    st.write("Enter a prompt that includes '{company}' to dynamically replace it with values from the selected column.")
    custom_prompt = st.text_input("Enter prompt (e.g., '
