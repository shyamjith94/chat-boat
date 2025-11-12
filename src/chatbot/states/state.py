from typing import List
from typing_extensions import TypedDict, Annotated
from langgraph.graph import add_messages
from langchain.messages import AnyMessage

class GraphState(TypedDict):
    """Model state structure that used in graph 

    Args:
        TypedDict (_type_): _description_
    """
    messages:Annotated[List, add_messages]
    summary:List
    news_data:str
    news_frequency:str

    