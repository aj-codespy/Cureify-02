import streamlit as st
from PIL import Image
from main import mainAgent
from googletrans import Translator

st.title('Cureify: Clinical Decision Support System')

# Language dropdown
languages = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Tamil": "ta",
    "Telugu": "te",
    "Bengali": "bn"
}
lang_choice = st.selectbox('Select Language', list(languages.keys()))

# Text and image input
prompt = st.text_input('Enter your symptoms or medical query')
img = st.file_uploader('Upload an image (optional)')

# Image display styling
if img:
    image = Image.open(img)
    st.markdown(
        """
        <style>
        .stImage img {
            max-width: 40%;
            max-height: 400px;
            display: block;
            margin: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.image(image, caption="Uploaded Image", use_container_width=True)

# Submit logic
if st.button('Submit'):
    if prompt or img:
        translator = Translator()
        lang_code = languages[lang_choice]
        
        # Translate the prompt only if it's not English
        translated_prompt = translator.translate(prompt, dest="en").text if lang_code != "en" else prompt
        
        # Call mainAgent with translated prompt
        result = mainAgent(translated_prompt, img)
        
        # Translate result back to original language if needed
        final_output = translator.translate(result, dest=lang_code).text if lang_code != "en" else result
        st.write(final_output)
    else:
        st.warning("Please enter symptoms or upload an image before submitting.")
