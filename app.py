import streamlit as st
from PIL import Image
# Removed datetime as it's not directly used in app.py
from main import mainAgent
# Removed translator functionality for simplicity
from chat_manager import get_chat_manager

st.title('Cureify: Medical AI Assistant')
# Simplified description
st.markdown("Medical analysis and symptom checker")

# Initialize chat manager
chat_manager = get_chat_manager()

# Simple chat controls
if st.sidebar.button("Clear Chat"):
    chat_manager.clear_chat()
    st.rerun()

# Main input section
prompt = st.text_input('Enter your symptoms or medical query')
img = st.file_uploader('Upload an image (optional)', type=['png', 'jpg', 'jpeg'])

if img:
    image = Image.open(img)
    st.image(image, caption="Uploaded Image", width=300)

if st.button('Analyze', type="primary"):
    if prompt or img:
        with st.spinner('Analyzing...'):
            try:
                result = mainAgent(prompt, img, chat_manager)
                
                if result:
                    st.markdown("### Medical Analysis")
                    st.write(result) # Display result directly without translation
                            
                else:
                    st.error("Unable to process request. Please try again.")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter symptoms or upload an image.")

st.markdown("---")
st.markdown("**Cureify** - Medical AI Assistant | *For informational purposes only*")