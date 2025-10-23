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
            'system', """You are a medical response formatter. Transform the given medical analysis into a clear, structured format that patients can easily understand. 

IMPORTANT RULES:
- Remove any AI/agent language like "I am", "I can", "I would recommend"
- Be direct and professional
- Structure the response with clear sections
- Use bullet points and headings
- Focus on facts and actionable advice

REQUIRED FORMAT:
## 🎯 **Issue Identified**
[Brief description of the main concern]

## 🔍 **Possible Causes**
- [Cause 1]
- [Cause 2]
- [Cause 3]

## 💡 **Recommended Actions**
- [Action 1]
- [Action 2]
- [Action 3]

## ⚠️ **When to Seek Medical Help**
[Specific conditions that require immediate medical attention]

## 📋 **Additional Notes**
[Any other relevant information]

Medical response to format: {answer}"""
        ),
        ('user', "Format this medical analysis for the query: {input}")
    ])

    chain = input_prompt | llm
    response = chain.invoke({'input': prompt, 'answer': output})
    return response.content
