import PIL.Image
import os
import google.generativeai as genai
from config import configure_genai

# Configure genai with API key from Streamlit secrets
configure_genai()

def woundAnalysis(img, prompt):
    basePrompt = '''
        You're a medical specialist and your task is to identify the wound from the given image and based on that do it's detailed analysis like what could be the cause of the wound, how to treat it, what are the symptoms of the wound, what are the precautions to be taken, what are the things that should be kept in mind while treating the wound and what are the things that should be kept in mind while taking care of the wound. And lastly how much time will it take to heal and what are the things that should be kept in mind while healing the wound.
    ''' 
    
    model = genai.GenerativeModel(model_name="gemini flash 2.0")
    imgFile = PIL.Image.open(img)

    response = model.generate_content([basePrompt+prompt, imgFile])
    return response.text

