import PIL.Image
import os
import google.generativeai as genai
from woundAnalysis import woundAnalysis
from OCR import OCR
from imgQuery import imgQuery

genai.configure(api_key='AIzaSyDtB4bETfNDyvpzA_NnBKMrr56rdiOE8bQ')

def imgClassifier(img, prompt):
    base_prompt = "You are an image classifier agent, you have to classify the image into 3 categories, if the image is an xray, enter xray and if the image is a prescription or medicine image, enter ocr and if it is some kind of wound or accident image enter wound and if its anything other than this then enter other. Always reply with only one of the given options" 
    
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    imgFile = PIL.Image.open(img)

    response = model.generate_content([base_prompt, imgFile])
    
    if 'wound' in response.text:
        output = woundAnalysis(img, prompt)
    # elif 'xray' in response.text:
    #     output = xrayAnalysis(img, prompt)
    elif 'ocr' in response.text:
        output = OCR(img, prompt)
        
    else:
        output = imgQuery(img, prompt)
        
    return output
    
