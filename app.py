import streamlit as st
from PIL import Image
from datetime import datetime
from main import mainAgent
from translator import create_language_selector, translate_medical_output, get_language_display_name
from chat_manager import get_chat_manager

st.title('Cureify: Clinical Decision Support System')
st.markdown("### 🌍 Multi-lingual Medical AI Assistant")

# Add information about the app
st.info("""
**Welcome to Cureify!** 🏥

This AI-powered medical assistant can:
- Analyze medical symptoms and provide insights
- Process medical images (X-rays, prescriptions, wounds)
- Answer general medical questions
- Provide responses in multiple Indian languages

**How to use:**
1. Select your preferred language from the sidebar
2. Enter your symptoms or medical question
3. Optionally upload a medical image
4. Click "Analyze Medical Query" to get your personalized medical analysis
""")

# Initialize chat manager
chat_manager = get_chat_manager()

# Language selection in sidebar
selected_language_code = create_language_selector()

# Chat controls in sidebar
st.sidebar.markdown("### 💬 Conversation Controls")

# Show conversation stats
chat_history = chat_manager.get_chat_history()
if chat_history:
    st.sidebar.metric("Messages", len(chat_history))
    symptoms = chat_manager.get_symptom_context()
    if symptoms:
        st.sidebar.metric("Symptoms Tracked", len(symptoms))

# Clear chat button
if st.sidebar.button("🗑️ Clear Chat History", help="Clear all conversation history"):
    chat_manager.clear_chat()
    st.rerun()

# Export conversation (optional)
if chat_history:
    if st.sidebar.button("📄 Export Chat", help="Download conversation as text"):
        chat_text = "\n\n".join([f"{msg['role'].title()}: {msg['content']}" for msg in chat_history])
        st.sidebar.download_button(
            label="Download Chat",
            data=chat_text,
            file_name=f"cureify_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

# Display conversation history
chat_manager.display_chat_history(selected_language_code)

# Main input section
col1, col2 = st.columns([2, 1])

with col1:
    prompt = st.text_input('Enter your symptoms or medical query', 
                          placeholder="Describe your symptoms or ask a medical question...")
    img = st.file_uploader('Upload an image (optional)', 
                          type=['png', 'jpg', 'jpeg'], 
                          help="Upload medical images like X-rays, prescriptions, or wound photos")

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

if st.button('🔍 Analyze Medical Query', type="primary"):
    if prompt or img:
        with st.spinner('Analyzing your request...'):
            try:
                # Get the medical analysis with chat context
                result = mainAgent(prompt, img, chat_manager)
                
                if result:
                    st.success("Analysis Complete!")
                    st.markdown("---")
                    
                    # Translate the result if not English
                    if selected_language_code != 'en':
                        with st.spinner(f'Translating to {get_language_display_name(selected_language_code)}...'):
                            translated_result = translate_medical_output(result, selected_language_code)
                    else:
                        translated_result = result
                    
                    # Display the result
                    st.markdown(f"### 🏥 Medical Analysis Result ({get_language_display_name(selected_language_code)})")
                    st.write(translated_result)
                    
                    # Show language info
                    if selected_language_code != 'en':
                        with st.expander("🌐 Original English Version"):
                            st.write(result)
                    
                    # Show conversation context
                    if chat_manager.get_chat_history():
                        st.markdown("---")
                        st.markdown("### 📋 Current Conversation Context")
                        context = chat_manager.get_conversation_summary()
                        st.text_area("Context", context, height=100, disabled=True)
                            
                else:
                    st.error("Sorry, I couldn't process your request. Please try again with more specific information.")
                    
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                st.info("Please check your API key configuration in the secrets file.")
    else:
        st.warning("Please enter symptoms or upload an image before submitting.")

# Footer information
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p><strong>Cureify</strong> - Multi-lingual Medical AI Assistant</p>
    <p>Supports 20+ Indian languages | Powered by Google Gemini AI</p>
    <p><em>⚠️ This is for informational purposes only. Always consult a healthcare professional for medical advice.</em></p>
</div>
""", unsafe_allow_html=True)