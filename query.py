from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def queryAnalysis(prompt):
    llm = GoogleGenerativeAI(
        model='gemini-2.0-flash',
        temperature=0,
        api_key='AIzaSyBozQi2V59ZCzUI6smDyDHt1j9sSSkcZbE',
        max_tokens=None,
        timeout=30,
        max_retries=2
    )
    
    input_prompt = ChatPromptTemplate.from_messages([
        (
            'system', "You are talking to a doctor You're a medical specialist and your task is to provide a detailed answer for the given query. Also suggest the tests that need to be taken. The answer should be in depth and approx about 300 words."
        ),
        ('user', "{input}")
    ])

    chain = input_prompt | llm
    response = chain.invoke({'input':prompt})

    return response

