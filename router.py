from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from imageAgent import imgClassifier
from query import queryAnalysis
from symptoms import retrieve_and_answer

def routerAgent(img, prompt):
    base = '''From the given prompt, you have to find out which task do we have to perform, if it's an image, 
    we'll have to perform disease identification for that respond image. If it's a disease symptom related then output 
    symptoms. If it's any other task then respond with the word query.
    Whatever is the decision you make give it in All lowercase'''

    Agent = GoogleGenerativeAI(
        model='gemini-2.0-flash',
        temperature=0,
        api_key='AIzaSyDtB4bETfNDyvpzA_NnBKMrr56rdiOE8bQ',
        max_tokens=None,
        timeout=30,
        max_retries=2
    )
    role = ChatPromptTemplate.from_messages([
        (
            'system', f'{base}'
        ),
        ('user', "{input}")
    ])


    chain = role | Agent
    response = chain.invoke({'input':prompt})

    output = response.content 
    
    if img:
        imgAnalysis = imgClassifier(img, prompt)
        return imgAnalysis
    elif 'query' in output:
        queryOutput = queryAnalysis(prompt)
        return queryOutput
    elif 'symptom' in output:
         result = retrieve_and_answer(prompt)
         return result
    else:
        return output





