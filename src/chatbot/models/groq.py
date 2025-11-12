from src.chatbot.core import ModelBase
from langchain_groq import ChatGroq
import streamlit as st
import os
from src.chatbot.core import common_messages
from src.chatbot.core.schema import ModelBaseInfo

class GroqLLm(ModelBase):
    def __init__(self, user_input:ModelBaseInfo):
        self.model_name = user_input.get("selected_model")
        self.api_key = user_input.get("api_key")
        self.model = None

    
    def get_llm_model(self):
        self.model = ChatGroq(model=self.model_name, api_key=self.api_key)
        return self._validate_model()

    def _validate_model(self):
        try:
            if not st.session_state.get("health_check", False):
                response = self.model.invoke(
                common_messages,
                max_tokens=20
            )
                st.success("Model health check fine")
                st.session_state["health_check"] = True
                print("Model reply:", response.content)
            os.environ["GROQ_API_KEY"] = self.api_key
            return self.model  
        except Exception as e:
            print(f"Groq API test failed: {e}")
            st.error("Groq API test failed:")

    
