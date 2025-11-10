from pydantic import BaseModel


class ModelBaseInfo(BaseModel):
    selected_llm:str
    selected_model:str
    api_key:str
    selected_use_case:str

