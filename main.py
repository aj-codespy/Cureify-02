from router import routerAgent
from structAgent import structAgent
from chat_manager import get_chat_manager
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def mainAgent(prompt, img=None, chat_manager=None):
    # Get chat manager if not provided
    if chat_manager is None:
        chat_manager = get_chat_manager()
    
    # Add user message to chat history
    chat_manager.add_message('user', prompt, 'general')
    
    # Process the request
    output = routerAgent(img, prompt, chat_manager)
    
    # Use structAgent to format the output better
    if output and len(output.strip()) > 0:
        try:
            structured_output = structAgent(prompt, output)
            return structured_output
        except Exception as e:
            # If structAgent fails, return the original output
            return output
    else:
        error_msg = "I'm sorry, I couldn't process your request. Please try again with more specific information."
        chat_manager.add_message('assistant', error_msg, 'error')
        return error_msg
    

prompt = 'What does this image say?'
img = 'wound.jpeg'

print(mainAgent(prompt, img))
