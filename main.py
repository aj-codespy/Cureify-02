from router import routerAgent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
def mainAgent(prompt, img=None):
    output = routerAgent(img, prompt)
    return output
    # if 'unstructured' in ouptut:
    #     response = structAgent(prompt, ouptut)
    #     return response
    # else:
    #     return ouptut

