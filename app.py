import streamlit as st
from PIL import Image
from main import mainAgent
from googletrans import Translator
import asyncio

st.title('Cureify: Clinical Decision Support System')

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
lang_code = languages[lang_choice]

prompt = st.text_input('Enter your symptoms or medical query')
img = st.file_uploader('Upload an image (optional)')

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

async def translate_text(text, dest):
    translator = Translator()
    result = await translator.translate(text, dest=dest)
    return result.text

if st.button('Submit'):
    if prompt or img:
        try:
            if lang_code != "en":
                translated_prompt = asyncio.run(translate_text(prompt, "en"))
            else:
                translated_prompt = prompt

            result = mainAgent(translated_prompt, img)

            if lang_code != "en":
                final_output = asyncio.run(translate_text(result, lang_code))
            else:
                final_output = result

            st.write(final_output)
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter symptoms or upload an image before submitting.")
