import streamlit as st
import google.generativeai as genai

def get_api_key():
    """
    Get the Google API key from Streamlit secrets.
    Returns the API key or raises an error if not found.
    """
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
        return api_key
    except KeyError:
        st.error("""
        **API Key not found!** 
        
        Please add your Google API key to Streamlit secrets:
        
        1. Create a `.streamlit/secrets.toml` file in your project root
        2. Add the following content:
        ```
        GOOGLE_API_KEY = "your_api_key_here"
        ```
        
        Or set it as an environment variable:
        ```
        export GOOGLE_API_KEY="your_api_key_here"
        ```
        """)
        st.stop()

def configure_genai():
    """
    Configure Google Generative AI with the API key from Streamlit secrets.
    """
    api_key = get_api_key()
    genai.configure(api_key=api_key)
    return api_key
