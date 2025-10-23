import PIL.Image
import google.generativeai as genai
from query import queryAnalysis
from config import configure_genai

# Configure genai with API key from Streamlit secrets
configure_genai()
model = genai.GenerativeModel(model_name="gemini flash 2.0")

def OCR(img, prompt):
    imgFile = PIL.Image.open(img)
    baseprompt = "Extract all the text from the image in a clear and well defined manner."
    response = model.generate_content([baseprompt, imgFile])
    output = queryAnalysis(response.text + prompt)
    return output

