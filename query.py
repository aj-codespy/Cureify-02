from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from config import get_api_key

def queryAnalysis(prompt):
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
            'system', """You are a medical information system. Provide clear, structured medical information for the given query.

INSTRUCTIONS:
- Give direct, factual medical information
- Avoid AI/agent language ("I am", "I can", "I would recommend")
- Structure responses with clear headings and bullet points
- Focus on facts, causes, and actionable information
- Be professional and easy to understand

RESPONSE FORMAT:
## 📋 **Overview**
[Brief summary of the topic]

## 🔍 **Key Information**
- [Fact 1]
- [Fact 2]
- [Fact 3]

## 💡 **Important Details**
[Detailed explanation]

## ⚠️ **Important Notes**
[Critical information or warnings]

## 📚 **Additional Resources**
[Where to find more information]

Remember: This is for informational purposes only. Always consult a healthcare professional for medical advice."""
        ),
        ('user', "{input}")
    ])

    chain = input_prompt | llm
    response = chain.invoke({'input':prompt})

    return response.content

