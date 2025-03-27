import streamlit as st 
from main import mainAgent

st.title('Cureify: Clinical Decision Support System.')

prompt = st.input('Enter your prompt')
img = st.file_uploader('Upload an image')

result = mainAgent(prompt, img)

if st.button('Submit'):
    st.write(result)