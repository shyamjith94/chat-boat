from src.chatbot.states import GraphState
from langgraph.graph import StateGraph, START, END

from src.chatbot.nodes import BasicChatbotNode
from src.chatbot.core.schema import ModelBaseInfo
from src.chatbot.core.enum import ModelUseCaseEnum
import streamlit as st



class GraphBuilder:
    def __init__(self, user_input:ModelBaseInfo, llm_model=None):
        self.user_input = user_input
        self.model = llm_model  # This should be the actual LLM object, not a string
        self.graph_builder = StateGraph(GraphState)


    def basic_chatbot_graph(self):
        """to build the basic chat bot it use BasicChatBot node
            it will set both entry and exit of the graph, 
        """
        self.basic_chatbot_node = BasicChatbotNode(self.model)
        
        # nodes
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)

        # edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)


    def setup_graph(self, use_case: str):
        try:
            # Convert string to enum value
            selected_use_case = ModelUseCaseEnum(use_case)
            
            match selected_use_case:
                case ModelUseCaseEnum.BASIC_CHATBOT:
                    self.basic_chatbot_graph()
                
                case ModelUseCaseEnum.CHAT_WITH_TOOL:
                    # TODO: Add OpenAI implementation
                    raise NotImplementedError("OpenAI model not implemented yet")
                
                case ModelUseCaseEnum.AI_NEWS:
                    # TODO: Add Gemini implementation
                    raise NotImplementedError("Gemini model not implemented yet")
                
                case ModelUseCaseEnum.BLOG_GENERATOR:
                    # TODO: Add Gemini implementation
                    raise NotImplementedError("Gemini model not implemented yet")
                
                case _:
                    raise ValueError(f"Unsupported use case type: {selected_use_case}")
            return self.graph_builder.compile()
        
        except ValueError as e:
            st.error(f"Invalid use case selection: {str(e)}")
            return 