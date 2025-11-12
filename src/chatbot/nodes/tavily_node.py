
from json import tool
from typing import Dict, List
from langchain.messages import HumanMessage
from src.chatbot.states import GraphState


class TavilyNode:
    """Web search
    """
    def __init__(self, model, tools=None):
        self.model = model
        self.tools = tools

    def process(self, state:GraphState)->Dict:
        """initialize web search and get content
        """
        user_query = state["messages"][-1] if state["messages"] else ""
        llm_response = self.model.invoke([HumanMessage(user_query)])
        tools_response = f"Tool integration for {user_query}"
        return {"messages":[llm_response, tools_response]}


    def process_with_tool(self, state):
        """process with tools

        Args:
            state (_type_): _description_
        """
        if not self.tools:
            raise ValueError("To process with tool tool are are empty.")

        model_with_tool = self.model.bind_tools(self.tools)
        
        return {"messages":[model_with_tool.invoke(state["messages"])]}
