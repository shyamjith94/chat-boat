from typing import Dict
from src.chatbot.ui import LoadStreamlitUi, DisplayStreamlitResponse
import streamlit as st
from src.chatbot.models import GroqLLm
from src.chatbot.core.enum import ModelNameEnum, ModelUseCaseEnum
from src.chatbot.core.schema import ModelBaseInfo
from src.chatbot.graphs import GraphBuilder



class InitializeChatbot:
    """ load all details
    """

    def __init__(self):
        self._ui = LoadStreamlitUi()
        self._llm_model = None

    def _get_llm_model(self, user_input: ModelBaseInfo):
        try:
            # Convert string to enum value
            selected_llm = ModelNameEnum(user_input.get("selected_llm"))
            
            match selected_llm:
                case ModelNameEnum.GROQ:
                    obj = GroqLLm(user_input)
                    return obj.get_llm_model()
                case ModelNameEnum.OPENAI:
                    # TODO: Add OpenAI implementation
                    raise NotImplementedError("OpenAI model not implemented yet")
                case ModelNameEnum.GEMINI:
                    # TODO: Add Gemini implementation
                    raise NotImplementedError("Gemini model not implemented yet")
                case _:
                    raise ValueError(f"Unsupported model type: {selected_llm}")
        except ValueError as e:
            st.error(f"Invalid model selection: {str(e)}")
            return None

    

    def load_ui(self):
        input_user = self._ui.load_streamlit_ui()

        if not input_user:
            st.error("Failed to load user input")
            return
        
        if not input_user["api_key"]:
            st.warning("Enter the api key to play")
            return 
        
        

        model = self._get_llm_model(input_user)
        model_name = input_user.get("selected_model")
        use_case = input_user.get("selected_use_case")
        
        # Create columns for text input and send button on same line
        user_message = st.text_input("enter the message")
        
        if not user_message:
            return

        try:
            graph_builder = GraphBuilder(input_user, model)
            graph = graph_builder.setup_graph(use_case)
            display_res = DisplayStreamlitResponse(use_case, graph, user_message)
            display_res.display_response()
            
        except Exception as e:
            print(e)
            print(f"graph builder exception {str(e)}")
            return
        
        print(input_user)