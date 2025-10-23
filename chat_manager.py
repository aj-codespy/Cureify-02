import streamlit as st
from datetime import datetime
from typing import List, Dict, Any
from langchain_core.messages import HumanMessage, AIMessage

class ChatManager:
    """Manages conversation state and chat history"""
    
    def __init__(self):
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'conversation_context' not in st.session_state:
            st.session_state.conversation_context = {
                'user_profile': {},
                'medical_history': [],
                'current_symptoms': [],
                'language_preference': 'en'
            }
    
    def add_message(self, role: str, content: str, message_type: str = "general", metadata: Dict = None):
        """Add a message to the chat history"""
        message = {
            'role': role,  # 'user' or 'assistant'
            'content': content,
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'message_type': message_type,  # 'general', 'symptom', 'image', 'query'
            'metadata': metadata or {}
        }
        st.session_state.chat_history.append(message)
    
    def get_chat_history(self, limit: int = None) -> List[Dict]:
        """Get chat history, optionally limited to last N messages"""
        if limit:
            return st.session_state.chat_history[-limit:]
        return st.session_state.chat_history
    
    def get_conversation_context(self) -> Dict:
        """Get current conversation context"""
        return st.session_state.conversation_context
    
    def update_context(self, key: str, value: Any):
        """Update conversation context"""
        st.session_state.conversation_context[key] = value
    
    def clear_chat(self):
        """Clear all chat history"""
        st.session_state.chat_history = []
        st.session_state.conversation_context = {
            'user_profile': {},
            'medical_history': [],
            'current_symptoms': [],
            'language_preference': 'en'
        }
    
    def get_langchain_messages(self, limit: int = 10) -> List:
        """Convert chat history to LangChain message format for AI context"""
        recent_messages = self.get_chat_history(limit)
        langchain_messages = []
        
        for msg in recent_messages:
            if msg['role'] == 'user':
                langchain_messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                langchain_messages.append(AIMessage(content=msg['content']))
        
        return langchain_messages
    
    def get_symptom_context(self) -> List[str]:
        """Get current symptoms from conversation context"""
        return st.session_state.conversation_context.get('current_symptoms', [])
    
    def add_symptom(self, symptom: str):
        """Add a symptom to the current context"""
        if symptom not in st.session_state.conversation_context['current_symptoms']:
            st.session_state.conversation_context['current_symptoms'].append(symptom)
    
    def get_medical_history(self) -> List[str]:
        """Get medical history from conversation"""
        return st.session_state.conversation_context.get('medical_history', [])
    
    def add_to_medical_history(self, entry: str):
        """Add entry to medical history"""
        if entry not in st.session_state.conversation_context['medical_history']:
            st.session_state.conversation_context['medical_history'].append(entry)
    
    def display_chat_history(self, language: str = 'en'):
        """Display simplified chat history"""
        if not st.session_state.chat_history:
            return
        
        st.markdown("**Recent Messages:**")
        for message in st.session_state.chat_history[-3:]:
            role = "You" if message['role'] == 'user' else "AI"
            st.text(f"{role}: {message['content'][:50]}...")
    
    def get_conversation_summary(self) -> str:
        """Generate a summary of the current conversation for AI context"""
        if not st.session_state.chat_history:
            return "No previous conversation."
        
        summary_parts = []
        
        # Add symptoms context
        symptoms = self.get_symptom_context()
        if symptoms:
            summary_parts.append(f"Current symptoms discussed: {', '.join(symptoms)}")
        
        # Add recent conversation
        recent_messages = self.get_chat_history(5)  # Last 5 messages
        conversation_text = []
        for msg in recent_messages:
            role = "User" if msg['role'] == 'user' else "Assistant"
            conversation_text.append(f"{role}: {msg['content']}")
        
        if conversation_text:
            summary_parts.append(f"Recent conversation:\n" + "\n".join(conversation_text))
        
        return "\n\n".join(summary_parts)

# Global chat manager instance
def get_chat_manager() -> ChatManager:
    """Get the global chat manager instance"""
    return ChatManager()
