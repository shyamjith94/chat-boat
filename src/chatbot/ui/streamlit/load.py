from email import iterators
from http.client import REQUEST_ENTITY_TOO_LARGE
from logging import config
from typing import List
from src.chatbot.ui import Config
from src.chatbot.core.enum import ModelNameEnum
from src.chatbot.core.schema import ModelBaseInfo
import streamlit as st
from src.chatbot.core.enum import ModelUseCaseEnum, ModelToolsEnum,NewsTimeFrame
from operator import attrgetter

class LoadStreamlitUi:
    def __init__(self):
        self._config = Config()
        self._controls: ModelBaseInfo = {}
        self._icons = self._config.load_icons()
        
        st.markdown("""
            <style>
            [data-testid="stSidebar"] {
                background-color: white !important; 
                padding-top: 1rem;
                padding-bottom: 3rem;
            }
            [data-testid="stSidebar"] > div:first-child {
                overflow-y: auto;
                background-color: var(--secondary-background-color) !important;
            }
            </style>
        """, unsafe_allow_html=True)
        

    def _on_llm_change(self):
        """Streamlit callback when selected LLM changes.
        """
        # Mark that LLM changed so the UI can react on the next run
        st.session_state["health_check"] = True

    def _get_model_names(self, selected_llm: str | None = None):
        """Return model names for the currently selected LLM.

        Priority for determining selected LLM:

        """
        if selected_llm is None:
            selected_llm = st.session_state.get(
                "selected_llm", self._controls.get("selected_llm"))

        try:
            model_name = self._config.get_model_options(selected_llm)
            if not model_name:
                return ["Model not found"]
            return [name.capitalize() for name in model_name]
        except Exception:
            # log and return fallback
            print("model selection key error")
            return ["Model not found"]

    def load_streamlit_ui(self):
        st.set_page_config(
            page_title=self._config.get_page_title(), layout="wide")
        st.header(self._config.get_page_title())

       

        with st.sidebar:

            llm_options = self._config.get_llm_options()
            use_case_option = self._config.get_use_case_options()

            st.selectbox("Select LLm", llm_options,
                         key="selected_llm", on_change=self._on_llm_change)
            # synchronize into controls for other code paths
            self._controls["selected_llm"] = st.session_state.get(
                "selected_llm")

            llm_model_option: List[str] = self._get_model_names()

            # model select box uses a key so value is kept in session_state
            self._controls["selected_model"] = st.selectbox(
                "Select model", llm_model_option, key="selected_model", on_change=self._on_llm_change)
            self._controls["api_key"] = st.text_input(
                "Api key", type="password", icon=self._icons.get("key"))
            self._controls["selected_use_case"] = st.selectbox(
                "Select use case", use_case_option)

            try:
                use_case = ModelUseCaseEnum(
                    self._controls.get("selected_use_case"))

                # play with tools
                if use_case == ModelUseCaseEnum.CHAT_WITH_TOOL:
                    tools_option = self._config.get_model_tools()
                    self._controls["selected_tool"] = st.selectbox(
                        "Select tool", tools_option)

                    try:
                        if ModelToolsEnum(self._controls.get("selected_tool")) == ModelToolsEnum.TAVILY:
                            self._controls["tavily_api_key"] = st.text_input(
                                "enter tavily api key https://app.tavily.com/home", type="password", icon=self._icons.get("key"))
                    except KeyError:
                        print(f"Tool selection error")
                        st.error("tool selection error")
                if use_case == ModelUseCaseEnum.AI_NEWS:
                    get_values = list(map(attrgetter("value"), NewsTimeFrame))
                    self._controls["news_frequency"] = st.selectbox(
                        f"{self._icons.get("calendar")}Select time frame", get_values)
                    self._controls["selected_tool"] = ModelToolsEnum.TAVILY.value
                    self._controls["tavily_api_key"] = st.text_input(
                                "enter tavily api key https://app.tavily.com/home", type="password", icon=self._icons.get("key"))
                    
            except KeyError:
                print(f"Use case selection error")
                st.error("Use case selection error")

        return self._controls
