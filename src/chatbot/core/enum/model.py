from enum import Enum


class ModelNameEnum(Enum):
    GROQ = "GROQ"
    OPENAI = "OPENAI"
    GEMINI = "GEMINI"


class ModelUseCaseEnum(Enum):
    BASIC_CHATBOT = "Basic Chatbot"
    CHAT_WITH_TOOL = "Chatbot with tool"
    AI_NEWS = "AI News"
    BLOG_GENERATOR = "Blog generator"


class ModelToolsEnum(Enum):
    TAVILY="Tavily"

class NewsTimeFrame(Enum):
    DAILY="Daily"
    WEEKLY="Weekly"
    MONTHLY="Monthly"