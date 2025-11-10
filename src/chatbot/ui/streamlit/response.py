from typing import Any
import streamlit as st
from src.chatbot.core.enum import ModelUseCaseEnum

class DisplayStreamlitResponse:
    def __init__(self, use_case:str, graph:Any, user_message: str):
        self.use_case = use_case
        self.graph = graph
        self.user_message = user_message


    def display_response(self):
        use_case = ModelUseCaseEnum(self.use_case)
        if use_case == ModelUseCaseEnum.BASIC_CHATBOT:
            for event in self.graph.stream({"messages": self.user_message}):
                print(event)
                for value in event.values():
                    print(value)
                    print(value["messages"])
                    with st.chat_message("user"):
                        st.write(self.user_message)
                    with st.chat_message("assistant"):
                        st.write(value["messages"].content)
                        