import PIL.Image
import os
import google.generativeai as genai
from config import configure_genai

# Configure genai with API key from Streamlit secrets
configure_genai()

def imgQuery(img, prompt):
    sample_file_1 = PIL.Image.open(img)

    model = genai.GenerativeModel(model_name="gemini-2.0-flash")

    basePrompt = """Analyze the medical image and provide a structured response to the user's query.

INSTRUCTIONS:
- Provide direct, factual medical analysis
- Avoid AI/agent language ("I am", "I can", "I would recommend")
- Structure responses with clear headings and bullet points
- Focus on what can be observed in the image
- If the image is not medical-related, state that clearly

RESPONSE FORMAT:
## 🖼️ **Image Analysis**
[What is observed in the image]

## 🔍 **Key Findings**
- [Finding 1]
- [Finding 2]
- [Finding 3]

## 💡 **Medical Interpretation**
[What the findings mean medically]

## ⚠️ **Important Notes**
[Any concerns or recommendations]

If the image is not medical-related, respond with: "This image does not appear to contain medical information. Please upload a medical image for analysis.""""

    response = model.generate_content([prompt, sample_file_1])

    return response.text