import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage
import pickle
import os
from config import get_api_key

model = SentenceTransformer('all-MiniLM-L6-v2')

def load_vector_db(index_path="faiss_index.idx", chunks_file="text_chunks.pkl"):
    index = faiss.read_index(index_path)
    with open(chunks_file, "rb") as f:
        text_chunks = pickle.load(f)
    return index, text_chunks

def get_text_embeddings(text):
    if not text.strip():
        return np.zeros(384)
    embeddings = model.encode([text])
    return embeddings

def answer_generation(input, chatHistory):
    llm = ChatGoogleGenerativeAI(
        model='gemini-2.0-flash',
        temperature=0,
        api_key=get_api_key(),
        max_tokens=None,
        timeout=30,
        max_retries=2
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", '''You are a medical analysis system. Analyze the provided symptoms and medical information to give a structured medical assessment.

INSTRUCTIONS:
- Provide direct, factual medical analysis
- Avoid AI/agent language ("I am", "I can", "I would recommend")
- Structure responses clearly with headings and bullet points
- Focus on possible conditions, causes, and recommended actions
- Be professional and empathetic
- If insufficient information, ask for specific additional details

RESPONSE FORMAT:
## 🎯 **Primary Concern**
[Main medical issue identified]

## 🔍 **Possible Conditions**
- [Condition 1 with likelihood]
- [Condition 2 with likelihood]
- [Condition 3 with likelihood]

## 📊 **Risk Assessment**
[Low/Medium/High risk based on symptoms]

## 💡 **Immediate Actions**
- [Action 1]
- [Action 2]
- [Action 3]

## ⚠️ **Red Flags to Watch**
[Warning signs that require immediate medical attention]

## 📋 **Additional Information Needed**
[Specific questions to clarify the condition]

Remember: This is for informational purposes only. Always consult a healthcare professional for proper diagnosis and treatment.'''),
        MessagesPlaceholder("chat_history"),
        ("human", "{Question}")
    ])
    chain = prompt | llm
    response = chain.invoke({"Question": input,  "chat_history": chatHistory})
    chatHistory.extend([HumanMessage(content=input), response.content])
    return response.content

def query_vector_db_with_rag(query_text, index, text_chunks, k=3):
    query_embedding = np.array(get_text_embeddings(query_text)).astype('float32').reshape(1, -1)
    distances, indices = index.search(query_embedding, k)
    retrieved_chunks = [text_chunks[i] for i in indices[0]]
    context = "\n".join(retrieved_chunks)
    return context

def retrieve_and_answer(query_text, chatHistory, index_path="faiss_index.idx", chunks_file="text_chunks.pkl", k=4):
    index, stored_chunks = load_vector_db(index_path, chunks_file)
    context = query_vector_db_with_rag(query_text, index, stored_chunks, k)
    response = answer_generation(f"Context: {context}\nQuestion: {query_text}", chatHistory)
    return response

def retrieve_and_answer_with_context(query_text, chat_manager, index_path="faiss_index.idx", chunks_file="text_chunks.pkl", k=4):
    """Enhanced version that uses chat manager for persistent conversation"""
    # Get conversation context
    conversation_summary = chat_manager.get_conversation_summary()
    
    # Load vector database
    index, stored_chunks = load_vector_db(index_path, chunks_file)
    context = query_vector_db_with_rag(query_text, index, stored_chunks, k)
    
    # Get LangChain messages for AI context
    langchain_messages = chat_manager.get_langchain_messages(limit=10)
    
    # Enhanced prompt with conversation context
    enhanced_prompt = f"""Previous conversation context: {conversation_summary}

Current medical context from knowledge base: {context}

Current question: {query_text}

Please provide a comprehensive medical analysis considering the conversation history and current symptoms."""
    
    response = answer_generation(enhanced_prompt, langchain_messages)
    return response


# prompt1 = 0
# chatHistory = []
# while prompt1 != '1':
#     prompt1 = input('Enter your symptoms: ')
#     output = retrieve_and_answer(prompt1, chatHistory)
#     print(output)

#print(chatHistory)

