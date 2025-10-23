import PIL.Image
import os
import google.generativeai as genai
from config import configure_genai

# Configure genai with API key from Streamlit secrets
configure_genai()

def woundAnalysis(img, prompt):
    basePrompt = '''Analyze the wound in the image and provide a structured medical assessment.

Provide a detailed analysis covering:
- Wound identification and classification
- Possible causes
- Treatment recommendations
- Care instructions
- Healing timeline
- Warning signs to watch for

Format the response with clear headings and bullet points. Be direct and professional without using AI/agent language.''' 
    
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")
    imgFile = PIL.Image.open(img)

    response = model.generate_content([basePrompt+prompt, imgFile])
    return response.text

