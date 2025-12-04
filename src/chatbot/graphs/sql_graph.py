from langgraph.graph import START, END, StateGraph
from src.chatbot.core.schema import ModelBaseInfo
from src.chatbot.nodes import SqlNode
from src.chatbot.states import GraphState
from src.chatbot.tools import get_sql_tool, create_tools_node
from langchain_community.utilities import SQLDatabase
import os

class SqlGraphBuilder:
    def __init__(self, user_input:ModelBaseInfo, llm_model=None):
        self.user_input = user_input
        self.llm_model = llm_model
        self.graph_builder = StateGraph(GraphState)
        self.db = self._create_db() 

    def _create_db(self):
        db_path = self.user_input.get("sql_file_path")
        if os.path.exists(db_path):
            db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
            return db
        else:
            print("****** Db file not fount in sql graph builder ******")
            raise FileNotFoundError("Db file not fount in sql graph builder")

         
    def sql_graph_builder(self):
       
        tools = get_sql_tool(self.db, self.llm_model)
        tools_node = create_tools_node(tools)
        
        nodes = SqlNode(model=self.llm_model,db=self.db)

         # nodes
        self.graph_builder.add_node("generate_query", nodes.generate_query)
        self.graph_builder.add_node("check_generated_query", nodes.check_sql_query)
        self.graph_builder.add_node("rewrite_user_query", nodes.rewrite_the_user_query)
        # self.graph_builder.add_node("run_sql_query", nodes.run_sql_query)
        self.graph_builder.add_node("run_sql_query", tools_node)

        # edges 
        self.graph_builder.add_edge(START, "generate_query")
        self.graph_builder.add_edge("generate_query", "check_generated_query")
        
        self.graph_builder.add_conditional_edges("check_generated_query", nodes.continue_or_not, {"run":"run_sql_query", "rewrite":"rewrite_user_query"})        
        self.graph_builder.add_edge("rewrite_user_query", "generate_query")
        self.graph_builder.add_edge("run_sql_query", END)

        return self.graph_builder