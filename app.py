import streamlit as st
from PIL import Image
from datetime import datetime
from main import mainAgent
from translator import create_language_selector, translate_medical_output, get_language_display_name
from chat_manager import get_chat_manager

st.title('Cureify: Medical AI Assistant')
st.markdown("Multi-lingual medical analysis and symptom checker")

# Initialize chat manager
chat_manager = get_chat_manager()

# Language selection in sidebar
selected_language_code = create_language_selector()

# Simple chat controls
if st.sidebar.button("Clear Chat"):
    chat_manager.clear_chat()
    st.rerun()

# Show recent messages only
chat_history = chat_manager.get_chat_history(limit=3)
if chat_history:
    st.sidebar.markdown("**Recent Messages:**")
    for msg in chat_history[-3:]:
        role = "You" if msg['role'] == 'user' else "AI"
        st.sidebar.text(f"{role}: {msg['content'][:50]}...")

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
                    # Translate if needed
                    if selected_language_code != 'en':
                        translated_result = translate_medical_output(result, selected_language_code)
                    else:
                        translated_result = result
                    
                    st.markdown("### Medical Analysis")
                    st.write(translated_result)
                            
                else:
                    st.error("Unable to process request. Please try again.")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter symptoms or upload an image.")

st.markdown("---")
st.markdown("**Cureify** - Medical AI Assistant | *For informational purposes only*")