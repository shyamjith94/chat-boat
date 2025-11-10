

from typing import Dict
from src.chatbot.states import GraphState


class BasicChatbotNode:
    """Create basic chatbot
    """
    def __init__(self, model):
        self.model = model

    def process(self, state:GraphState)-> Dict:
        """Process the input and generate the result for user
        """

        return {"messages": self.model.invoke(state["messages"])}