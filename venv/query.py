from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import get_api_key

def queryAnalysis(prompt):
    llm = ChatGoogleGenerativeAI(
        model='gemini flash 2.0',
        temperature=0,
        api_key=get_api_key(),
        max_tokens=None,
        timeout=30,
        max_retries=2
    )
    
    input_prompt = ChatPromptTemplate.from_messages([
        (
            'system', "You're a medical specialist and your task is to provide a detailed answer for the given query. The answer should be in depth and approx about 300 words."
        ),
        ('user', "{input}")
    ])

    chain = input_prompt | llm
    response = chain.invoke({'input':prompt})

    return response.content

