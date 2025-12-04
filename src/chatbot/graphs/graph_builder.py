from src.chatbot.states import GraphState
from langgraph.graph import StateGraph, START, END

from src.chatbot.nodes import BasicChatbotNode, TavilyNode, NewsNode
from src.chatbot.core.schema import ModelBaseInfo
from src.chatbot.core.enum import ModelUseCaseEnum
from langgraph.prebuilt import tools_condition
import streamlit as st

from src.chatbot.tools import get_tavily_tool, create_tools_node
from src.chatbot.graphs import SqlGraphBuilder
from src.chatbot.core.enum import ModelToolsEnum

class GraphBuilder:
    def __init__(self, user_input:ModelBaseInfo, llm_model=None):
        self.user_input = user_input
        self.model = llm_model  # This should be the actual LLM object, not a string
        self.graph_builder = StateGraph(GraphState)
        self.sql_graph = SqlGraphBuilder(user_input, llm_model)

    def _basic_chatbot_graph(self):
        """to build the basic chat bot it use BasicChatBot node
            it will set both entry and exit of the graph, 
        """
        self.basic_chatbot_node = BasicChatbotNode(self.model)
        
        # nodes
        self.graph_builder.add_node("chatbot", self.basic_chatbot_node.process)

        # edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def _tavily_chatbot_graph(self):
        """Tavily web search to get web based response on
            the user queries 
        """
        tavily_api_key = self.user_input.get("tavily_api_key")
        tools = [get_tavily_tool(tavily_api_key)]
        tools_node = create_tools_node(
         tools    
        )
        
        self.tavily_chatbot = TavilyNode(self.model, tools=tools)
        
         # nodes
        self.graph_builder.add_node("chatbot", self.tavily_chatbot.process_with_tool)
        # self.graph_builder.add_node("tavily", self.tavily_chatbot.process)
        self.graph_builder.add_node("tools", tools_node)

        # edges
        self.graph_builder.add_edge(START, "chatbot")
        self.graph_builder.add_conditional_edges("chatbot", tools_condition)
        self.graph_builder.add_edge("tools", "chatbot")
        self.graph_builder.add_edge("chatbot", END)

    def _news_graph_builder(self):
        """use case is news. building graph new optimizer 
            and provide summarized news, use tavily tool for fetch news
        """
        tavily_api_key = self.user_input.get("tavily_api_key")
        news_node_obj = NewsNode(self.model, tavily_api_key)
        
        # nodes
        self.graph_builder.add_node("fetch_news", news_node_obj.fetch_news)
        self.graph_builder.add_node("summarize_news", news_node_obj.summarize_news)
        # self.graph_builder.add_node("save_result", "")

        # edges
        self.graph_builder.set_entry_point("fetch_news")
        self.graph_builder.add_edge("fetch_news", "summarize_news")
        # self.graph_builder.add_edge("summarize_news", "save_result")
        self.graph_builder.add_edge("summarize_news", END)
        
        
        


    def setup_graph(self, use_case: str):
        try:
            # Convert string to enum value
            selected_use_case = ModelUseCaseEnum(use_case)
            
            match selected_use_case:
                case ModelUseCaseEnum.BASIC_CHATBOT:
                    self._basic_chatbot_graph()
                
                case ModelUseCaseEnum.CHAT_WITH_TOOL:
                    if ModelToolsEnum(self.user_input.get("selected_tool")) == ModelToolsEnum.SQL:
                        self.graph_builder = self.sql_graph.sql_graph_builder()
                    else:
                        self._tavily_chatbot_graph()                        
                case ModelUseCaseEnum.AI_NEWS:
                    self._news_graph_builder()
                
                case ModelUseCaseEnum.BLOG_GENERATOR:
                    # TODO: Add Gemini implementation
                    raise NotImplementedError("Gemini model not implemented yet")
                
                case _:
                    raise ValueError(f"Unsupported use case type: {selected_use_case}")
            return self.graph_builder.compile()
        
        except ValueError as e:
            st.error(f"Invalid use case selection: {str(e)}")
            return 