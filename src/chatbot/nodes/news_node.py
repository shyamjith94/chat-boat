from urllib import response
from tavily import TavilyClient
from src.chatbot.states import GraphState

class NewsNode:

    def __init__(self, model, api_key):
        """Ai news node

        Args:
            model (_type_): llm model
        """
        self.tavily = TavilyClient(api_key=api_key)
        self.model = model

        self.state = {}

    def fetch_news(self, state:GraphState):
        """fetch news from tavily client

        Args:
            state (GraphState): LLm graph state
            frequency (str): news range frequency like. 
                monthly, daily, weekly
        """
        
        frequency = state["news_frequency"].lower()
        topic = state["messages"][0].content.lower()
        time_range_map = {"daily": "d", "weekly":"w", "monthly": "m", "year":"y"}
        day_range_map = {"daily": 1, "weekly":7, "monthly":30, "year":366}

        response = self.tavily.search(
            query=topic,
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=20,
            days=day_range_map[frequency]
        )
        state["news_data"] = response.get("results", [])
        self.state["news_data"] = state.get("news_data")
        return state


    def summarize_news(self, state: GraphState):
        """summarize the news using llm model

        Args:
            state (GraphState): LLm state
        """

        # Use a plain string template for the summarization prompt. Some
        # ChatPromptTemplate helpers expect prompt message objects or
        # prompt-template classes; to avoid mismatches across langchain
        # versions we build a simple string and format it with articles.
        prompt_template = """
        ### Context:
        Below are multiple news articles or snippets retrieved from Tavily. Each item may include a title, summary, source, and publication date.

        ### Requirements:
        - Read and analyze all the provided articles summarize each one.

        ### Output Format:
        - **Date:** Mention the date of the news
        - **Headline Summary:** A 1-sentence high-level summary of all news combined.
        - **Key Points:** 3–5 concise bullet points capturing essential facts.
        - **Sources Covered:** Mention 2–3 main outlets or dates if available.
        - **URL:** Mention the date of the news
        

        ### Input Articles:
        {article}
        """

        news_items = self.state.get("news_data", [])
        article_str = "\n\n".join([
            f"content:{news.get('content', '')}\n\nurl:{news.get('url', '')}\n\ndate:{news.get('published_news', '')}"
            for news in news_items
        ])

        response = self.model.invoke(prompt_template.format(article=article_str))
        state["summary"] = response.content if response.content else "Content not found"
        self.state["summary"] = state["summary"]
        return {"messages":response}

            
            
        