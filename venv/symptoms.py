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
        model='gemini flash 2.0',
        temperature=0,
        api_key=get_api_key(),
        max_tokens=None,
        timeout=30,
        max_retries=2
    )
    prompt = ChatPromptTemplate.from_messages([
        ("system", '''Role: You are a Medical Diagnosis Specialist AI with deep expertise in diseases, symptoms, and medical conditions. Your task is to analyze user symptoms and identify the most probable diagnosis.
Instructions:
Diagnosis: If symptoms clearly indicate a disease, provide a concise yet detailed explanation.
Clarification: If multiple conditions match, ask relevant follow-up questions to narrow it down.
Uncertainty: If data is insufficient, respond with:
"I can't make a definitive diagnosis based on the given data. Please provide more details."
Guidance: Offer medical insights but do not provide prescriptions or treatment advice—recommend consulting a doctor when necessary.
Keep responses accurate, structured, and professional while maintaining an empathetic tone. Ask only one question at a time.'''),
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


# prompt1 = 0
# chatHistory = []
# while prompt1 != '1':
#     prompt1 = input('Enter your symptoms: ')
#     output = retrieve_and_answer(prompt1, chatHistory)
#     print(output)

#print(chatHistory)

