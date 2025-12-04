from typing import Any, List
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
from langchain_tavily import TavilySearch
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_community.agent_toolkits import SQLDatabaseToolkit

def get_tavily_tool(tavily_api_key: str):
    """tavily llm web search tool

    Args:
        tavily_api_key (str): user provided api key for tavily

    Returns:
        _type_: tool
    """
    return TavilySearch(max_result=2, tavily_api_key=tavily_api_key)
    


def get_sql_tool(db, llm_model):
    """Create sql tool. The wrapper provides a simple interface to execute
    SQL queries and fetch results:
    Params:
        model: llm model
        db: sql data bse
    """
    tool_kit = SQLDatabaseToolkit(db=db,llm=llm_model)
    tools = tool_kit.get_tools()
    return tools

    

def create_tools_node(tools: List[Any]):
    """_summary_

    Args:
        tools (List[Any]): _description_
    """
    return ToolNode(tools)
