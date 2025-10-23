from router import routerAgent
from structAgent import structAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def mainAgent(prompt, img=None):
    output = routerAgent(img, prompt)
    
    # Use structAgent to format the output better
    if output and len(output.strip()) > 0:
        try:
            structured_output = structAgent(prompt, output)
            return structured_output
        except Exception as e:
            # If structAgent fails, return the original output
            return output
    else:
        return "I'm sorry, I couldn't process your request. Please try again with more specific information."
    

prompt = 'What does this image say?'
img = 'wound.jpeg'

print(mainAgent(prompt, img))
