from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def structAgent(prompt, output):
    llm = ChatGoogleGenerativeAI(
        model='gemini-1.5-flash',
        temperature=0,
        api_key='AIzaSyDtB4bETfNDyvpzA_NnBKMrr56rdiOE8bQ',
        max_tokens=None,
        timeout=30,
        max_retries=2
    )
    
    input_prompt = ChatPromptTemplate.from_messages([
        (
            'system', "You're a output structure generator, your task is to generate a structured output based on the given prompt and it's answer. Make sure that the output should properly answer the prompt in a simple and easy to understand manner. Here's the answer: {answer}"
        ),
        MessagesPlaceholder("chat_history"),
        ('user', "{input}")
    ])

    chain = input_prompt | llm
    response = chain.invoke({'input':prompt, 'answer':output})
    return response.content
