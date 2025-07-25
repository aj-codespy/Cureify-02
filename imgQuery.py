import PIL.Image
import os
import google.generativeai as genai

genai.configure(api_key='AIzaSyBozQi2V59ZCzUI6smDyDHt1j9sSSkcZbE')

def imgQuery(img, prompt):
    sample_file_1 = PIL.Image.open(img)

    model = genai.GenerativeModel(model_name="gemini-2.0-flash")

    basePrompt = "You are a medical specialist and your task is to answer the query based on the given image and the prompt you have to answer the user's medical query. And if it is not a medical thing then just answer it is not a valid medical input."

    response = model.generate_content([prompt, sample_file_1])

    return response.text
