from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st

load_dotenv()

template = (
    "You are tasked with extracting specific information from the following text content: {dom_content}. "
    "Please follow these instructions carefully: \n\n"
    "1. **Extract Information:** Only extract the information that directly matches the provided description: {parse_description}. "
    "2. **No Extra Content:** Do not include any additional text, comments, or explanations in your response. "
    "3. **Empty Response:** If no information matches the description, return an empty string ('')."
    "4. **Direct Data Only:** Your output should contain only the data that is explicitly requested, with no other text."
    "5. **Readable by AI Model:** Your main task is that the data should be readable by an LLM model for its development."
    "6. **Tabular Format:** Try to give dataset in well documented tabular format."
)

#change this if you are using a different LLM model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

def parse_with_gemini(dom_chunks, parse_description):
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    parsed_results = []

    progress_text = st.empty()
    progress_bar = st.progress(0)

    for i, chunk in enumerate(dom_chunks, start=1):
        response = chain.invoke(
            {"dom_content": chunk, "parse_description": parse_description}
        )

        print(f"Parsed batch: {i} of {len(dom_chunks)}")
        progress_text.write(f"Parsed batch: {i} of {len(dom_chunks)}")
        parsed_results.append(response.content)
        progress_bar.progress(i / len(dom_chunks))

    progress_text.empty()
    progress_bar.empty()
    st.markdown("<h3 style='text-align: center;'>Data Retrived</h3>", unsafe_allow_html=True)
    return "\n".join(parsed_results)
