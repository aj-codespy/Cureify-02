from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import get_api_key

def structAgent(prompt, output):
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.0-flash',
        temperature=0,
        api_key=get_api_key(),
        max_tokens=None,
        timeout=30,
        max_retries=2
    )
    
    input_prompt = ChatPromptTemplate.from_messages([
        (
            'system', "You're a medical output structure generator. Your task is to format the given medical response in a clear, professional, and easy-to-understand manner. Structure the output with proper headings, bullet points, and clear explanations. Make it user-friendly for patients while maintaining medical accuracy. Here's the medical response to format: {answer}"
        ),
        ('user', "Please format this medical response for the query: {input}")
    ])

    chain = input_prompt | llm
    response = chain.invoke({'input': prompt, 'answer': output})
    return response.content
