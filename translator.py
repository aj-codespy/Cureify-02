from googletrans import Translator
import streamlit as st

# Simplified language mapping
INDIAN_LANGUAGES = {
    'English': 'en',
    'Hindi': 'hi',
    'Bengali': 'bn',
    'Telugu': 'te',
    'Marathi': 'mr',
    'Tamil': 'ta',
    'Gujarati': 'gu',
    'Kannada': 'kn',
    'Malayalam': 'ml',
    'Punjabi': 'pa'
}

def translate_text(text, target_language='en'):
    """
    Translate text to the target language using Google Translate
    
    Args:
        text (str): Text to translate
        target_language (str): Target language code (e.g., 'hi', 'en', 'bn')
    
    Returns:
        str: Translated text
    """
    if not text or not text.strip():
        return text
    
    try:
        translator = Translator()
        
        # Detect source language
        detected = translator.detect(text)
        source_lang = detected.lang
        
        # If source and target are the same, return original text
        if source_lang == target_language:
            return text
        
        # Translate the text
        result = translator.translate(text, src=source_lang, dest=target_language)
        return result.text
        
    except Exception as e:
        st.warning(f"Translation failed: {str(e)}. Showing original text.")
        return text

def get_language_display_name(language_code):
    """
    Get the display name for a language code
    
    Args:
        language_code (str): Language code (e.g., 'hi', 'en')
    
    Returns:
        str: Display name of the language
    """
    for display_name, code in INDIAN_LANGUAGES.items():
        if code == language_code:
            return display_name
    return language_code.upper()

def create_language_selector():
    """
    Create a language selector dropdown for Streamlit
    
    Returns:
        str: Selected language code
    """
    st.sidebar.markdown("### 🌐 Language Selection")
    selected_language = st.sidebar.selectbox(
        "Choose output language:",
        options=list(INDIAN_LANGUAGES.keys()),
        index=0,  # Default to English
        help="Select the language for the medical analysis output"
    )
    
    return INDIAN_LANGUAGES[selected_language]

def translate_medical_output(text, target_language='en'):
    """Simple medical text translation"""
    if target_language == 'en':
        return text
    
    try:
        translator = Translator()
        result = translator.translate(text, dest=target_language)
        return result.text
    except:
        return text
