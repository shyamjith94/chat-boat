from http.client import REQUEST_ENTITY_TOO_LARGE
from logging import config
from typing import List
from chatbot.ui import Config
from chatbot.core.enum import ModelNameEnum
from chatbot.core.schema import ModelBaseInfo
import streamlit as st

class LoadStreamlitUi:
    def __init__(self):
        self._config = Config()
        self._controls:ModelBaseInfo = {}

    def _get_model_names(self):
        try:
            model_name = self._config.get_model_option(self._controls["selected_llm"])
            if len(model_name) == 0:
                return ["Model not found"]
            return [name.capitalize() for name in model_name]
        except KeyError:
            print("model selection key error")
            return ["Model not found"]

    
    def load_streamlit_ui(self):
        st.set_page_config(page_title=self._config.get_page_title(), layout="wide")
        st.header(self._config.get_page_title())

        with st.sidebar:
            
            llm_options = self._config.get_llm_option()
            use_case_option = self._config.get_use_case_option()
            
            self._controls["selected_llm"] = st.selectbox("Select LLm", llm_options)
            llm_model_option:List[str] = self._get_model_names()
            
            self._controls["selected_model"] = st.selectbox("Select model", llm_model_option)
            # store api_key in controls (Config is not a mapping)
            self._controls["api_key"] = st.text_input("Api key", type="password")

            # update session state entries individually instead of overwriting
            # the entire session_state object
            st.session_state["selected_model"] = self._controls["selected_model"]
            st.session_state["api_key"] = self._controls["api_key"]
            self._controls["selected_use_case"] = st.selectbox("Select use case", use_case_option)

        return self._controls

    
        
