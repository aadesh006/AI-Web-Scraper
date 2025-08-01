import streamlit as st
import pandas as pd
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_gemini

st.set_page_config(page_title="AI Web-Scraper", page_icon="", layout="wide")
st.markdown("<h1 style='text-align: center;'>AI Web Scraper</h1>", unsafe_allow_html=True)
url = st.text_input("Enter the Website URL: ")
text = st.empty()

if st.button("Scrape Site"):
    text.write("Scraping...")
    result = scrape_website(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)
    
    st.session_state.dom_content = cleaned_content

    with st.expander("Viw DOM Content"):
        st.text_area("DOM Content: ", cleaned_content, height=300)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:

            dom_chunks = split_dom_content(st.session_state.dom_content)
            parsed_result = parse_with_gemini(dom_chunks, parse_description)
            st.write(parsed_result)

            if isinstance(parsed_result, list) and isinstance(parsed_result[0], dict):
                df = pd.DataFrame(parsed_result)
                csv = df.to_csv(index=False).encode("utf-8")

                st.download_button(
                    label="Download as CSV",
                    data=csv,
                    file_name="scraped_dataset.csv",
                    mime="text/csv"
                )
            else:
                st.info("Parsed result is not in tabular format. Showing raw output.")
                txt = str(parsed_result).encode("utf-8")
                st.download_button("Download as TXT", data=txt, file_name="scraped_dataset.txt")