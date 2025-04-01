from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def queryAnalysis(prompt):
    llm = GoogleGenerativeAI(
        model='gemini-2.0-flash',
        temperature=0,
        api_key='AIzaSyDtB4bETfNDyvpzA_NnBKMrr56rdiOE8bQ',
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

    return response

