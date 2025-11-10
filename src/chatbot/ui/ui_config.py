from configparser import ConfigParser
import os
from pathlib import Path


class Config:
    def __init__(self, config_file="ui_config.ini"):

        self.base_dir = Path(__file__).resolve().parent
        self.file = os.path.join(self.base_dir, config_file)
        if not os.path.exists(self.file):
            raise FileNotFoundError("UI Config file not found")
        
        self.config = ConfigParser()
        self.config.read(self.file, encoding="utf-8")

    def get_llm_option(self):
        return self.config["DEFAULT"].get("LLM_OPTIONS", "").split(",")

    def get_use_case_option(self):
        return self.config["DEFAULT"].get("USE_CASE_OPTIONS", "").split(",")

    def get_model_option(self, model_name: str):
        return self.config["DEFAULT"].get(model_name, "").split(",")

    def get_page_title(self):
        return self.config["DEFAULT"].get("PAGE_TITLE", "").strip()
    

    

