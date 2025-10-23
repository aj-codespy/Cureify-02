from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from imageAgent import imgClassifier
from query import queryAnalysis
from symptoms import retrieve_and_answer
from config import get_api_key

def routerAgent(img, prompt):
    # If there's an image, always process it first
    if img:
        imgAnalysis = imgClassifier(img, prompt)
        return imgAnalysis
    
    # For text-only queries, determine the type
    base = '''You are a medical query classifier. Analyze the given prompt and determine what type of medical query it is:
    
    - If the user is describing symptoms, pain, discomfort, or asking about a medical condition they might have, respond with "symptoms"
    - If the user is asking general medical questions, drug information, or medical facts, respond with "query"
    - If the user is asking about treatment options, medications, or medical procedures, respond with "query"
    
    Respond with only one word: either "symptoms" or "query"'''

    Agent = ChatGoogleGenerativeAI(
        model='gemini-2.0-flash',
        temperature=0,
        api_key=get_api_key(),
        max_tokens=None,
        timeout=30,
        max_retries=2
    )
    role = ChatPromptTemplate.from_messages([
        ('system', base),
        ('user', "{input}")
    ])

    chain = role | Agent
    response = chain.invoke({'input': prompt})
    output = response.content.lower().strip()
    
    # Route based on classification
    if 'symptom' in output:
        # Initialize empty chat history for symptoms
        chatHistory = []
        result = retrieve_and_answer(prompt, chatHistory)
        return result
    else:
        # Default to query analysis for general medical questions
        queryOutput = queryAnalysis(prompt)
        return queryOutput





