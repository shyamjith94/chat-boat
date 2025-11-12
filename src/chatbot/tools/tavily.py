from typing import Any, List
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
from langchain_tavily import TavilySearch


def get_tavily_tool(tavily_api_key: str):
    """tavily llm web search tool

    Args:
        tavily_api_key (str): user provided api key for tavily

    Returns:
        _type_: tool
    """
    return TavilySearch(max_result=2, tavily_api_key=tavily_api_key)
    


def create_tools_node(tools: List[Any]):
    """_summary_

    Args:
        tools (List[Any]): _description_
    """
    return ToolNode(tools)
