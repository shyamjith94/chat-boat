from langgraph.graph import END
from src.chatbot.states import GraphState
from typing import List, Dict, Literal
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage


class SqlNode:
    def __init__(self, model, db=None):
        self.model = model
        self.db = db


    def get_db_dialect(self):
        """Return data base dialect information
        """
        pass


    
    def generate_query(self, state:GraphState)-> Dict:
        """To generate sql query

        Args:
            state (GraphState): message state 
        """

       
        user_query = state["messages"][-1].content
        db_context = self.get_db_dialect()   # returns db.get_context()

        prompt = ChatPromptTemplate.from_messages([
            SystemMessage("You are an expert SQL generator. Only return the SQL query. No explanation."),
            HumanMessage(
                """### DATABASE INFORMATION
                    {db_schema}

                    ### USER QUESTION
                    {user_question}

                Generate the optimized SQL query."""
                )
        ])
        formatted = prompt.format_messages(
        db_schema=db_context,
        user_question=user_query
    )

    # Invoke LLM
        llm_response = self.model.invoke(formatted)
        return {"messages": self.model.invoke(state["messages"])}
    
    
    def check_sql_query(self, state:GraphState)-> Dict:
        """llm will verify the generated query is valid or not
            ita a conditional edge 
            if user query and sql query does not match pass wo query rewrite 
       Args:
            state (GraphState): message state 
        """
        pass

    def continue_or_not(self, state)->Literal["run", "rewrite"]:
        """_summary_

        Args:
            state (GraphState): message state 

        Returns:
            Literal: END, "rewrite_the_user_query"
        """
        pass
    

    def run_sql_query(self, state:GraphState)-> Dict:
        """run the sql query in database and return answer

        Args:
            state (GraphState): message state 
        """
        pass
    
    
    def rewrite_the_user_query(self, state:GraphState)->Dict:
        """rewrite the user query when agent fail to generate sql query

        Args:
            state (GraphState): message state 
        """
        pass
    

    