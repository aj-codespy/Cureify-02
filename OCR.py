import PIL.Image
import google.generativeai as genai
from query import queryAnalysis

genai.configure(api_key='AIzaSyBozQi2V59ZCzUI6smDyDHt1j9sSSkcZbE')
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

def OCR(img, prompt):
    imgFile = PIL.Image.open(img)
    baseprompt = "Extract all the text from the image in a clear and well defined manner."
    response = model.generate_content([baseprompt, imgFile])
    output = queryAnalysis(response.text + prompt)
    return output

