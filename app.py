import streamlit as st
from PIL import Image
from main import mainAgent

st.title('Cureify: Clinical Decision Support System')

prompt = st.text_input('Enter your symptoms or medical query')
img = st.file_uploader('Upload an image (optional)')

if img:
    image = Image.open(img)
    st.markdown(
        """
        <style>
        .stImage img {
            max-width: 40%; /* Adjust image size */
            max-height: 400px;
            display: block;
            margin: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.image(image, caption="Uploaded Image", use_container_width=True)

if st.button('Submit'):
    if prompt or img:
        with st.spinner('Analyzing your request...'):
            try:
                result = mainAgent(prompt, img)
                if result:
                    st.success("Analysis Complete!")
                    st.markdown("---")
                    st.markdown("### Medical Analysis Result:")
                    st.write(result)
                else:
                    st.error("Sorry, I couldn't process your request. Please try again with more specific information.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your API key configuration in the secrets file.")
    else:
        st.warning("Please enter symptoms or upload an image before submitting.")