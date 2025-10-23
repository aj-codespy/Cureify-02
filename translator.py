from googletrans import Translator
import streamlit as st

# Language mapping for Indian languages
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
    'Punjabi': 'pa',
    'Odia': 'or',
    'Assamese': 'as',
    'Sanskrit': 'sa',
    'Urdu': 'ur',
    'Nepali': 'ne',
    'Sindhi': 'sd',
    'Konkani': 'gom',
    'Manipuri': 'mni',
    'Bodo': 'brx',
    'Dogri': 'doi'
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
    """
    Translate medical output with special handling for medical terms
    
    Args:
        text (str): Medical analysis text to translate
        target_language (str): Target language code
    
    Returns:
        str: Translated medical text
    """
    if target_language == 'en':
        return text
    
    try:
        # Add context to help with medical translation
        context_text = f"This is a medical analysis report. Please translate the following text accurately, preserving medical terminology: {text}"
        
        translator = Translator()
        result = translator.translate(context_text, dest=target_language)
        
        # Clean up the result by removing the context prefix if it appears
        translated_text = result.text
        if "This is a medical analysis report" in translated_text:
            # Find where the actual translation starts
            start_idx = translated_text.find(":") + 1
            if start_idx > 0:
                translated_text = translated_text[start_idx:].strip()
        
        return translated_text
        
    except Exception as e:
        st.warning(f"Medical translation failed: {str(e)}. Showing original text.")
        return text
