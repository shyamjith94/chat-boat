# Chat-Boat 🤖

A modern, intelligent chatbot framework built with **LangChain**, **LangGraph**, and **Streamlit**. Chat-Boat enables developers to create sophisticated multi-use-case chatbot applications with seamless integration of LLMs, web search capabilities, and news aggregation features.

## 🎯 Overview

Chat-Boat is an open-source chatbot framework designed to simplify building AI-powered conversational applications. It leverages LangChain and LangGraph for robust AI orchestration and Streamlit for an intuitive web-based user interface. The project supports multiple language models, various use cases, and extensible tool integrations.

### Key Features

- **Multi-LLM Support**: Groq, OpenAI (TODO), and Google Gemini (TODO)
- **Multiple Use Cases**: Basic chatbot, web search chatbot, AI news aggregator, and blog generator
- **Tool Integration**: Tavily web search for real-time information retrieval
- **Graph-Based Architecture**: Powered by LangGraph for complex workflow management
- **Streamlit UI**: Interactive, user-friendly interface with real-time responses
- **Extensible Design**: Easy to add new models, tools, and use cases
- **State Management**: Sophisticated state handling using TypedDict-based graph states
- **Health Checks**: Automatic model validation and connectivity verification

---

## 📋 Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Available Models](#available-models)
- [Use Cases](#use-cases)
- [Tools & Integrations](#tools--integrations)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Keys Setup](#api-keys-setup)
- [Development](#development)
- [Contributing](#contributing)

---

## 📦 Requirements

- **Python**: 3.12.0 or higher
- **OS**: Windows, macOS, or Linux

### Core Dependencies

- `langchain` - LLM framework and abstractions
- `langchain-groq` - Groq LLM integration
- `langgraph` - Graph-based workflow orchestration
- `streamlit` - Web UI framework
- `tavily-python` - Web search API client
- `langchain-tavily` - Tavily integration for LangChain
- `pydantic` - Data validation and settings management

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/shyamjith94/chat-boat.git
cd chat-boat
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Using venv
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run src/app.py
```

The application will open in your default browser at `http://localhost:8501`.

---

## 🏗️ Project Structure

```
chat-boat/
├── README.md
├── src/
│   ├── __init__.py
│   ├── app.py                          # Application entry point
│   └── chatbot/
│       ├── __init__.py
│       ├── main.py                     # Chatbot initialization and main logic
│       ├── assets/                     # Static assets and resources
│       ├── core/                       # Core utilities and configurations
│       │   ├── __init__.py
│       │   ├── constant.py             # System constants and messages
│       │   ├── model_base.py           # Base model class
│       │   ├── enum/
│       │   │   ├── __init__.py
│       │   │   └── model.py            # Enums for models, use cases, and tools
│       │   └── schema/
│       │       ├── __init__.py
│       │       └── input_control.py    # Pydantic schemas for input validation
│       ├── graphs/
│       │   ├── __init__.py
│       │   └── graph_builder.py        # LangGraph graph construction logic
│       ├── models/
│       │   ├── __init__.py
│       │   └── groq.py                 # Groq LLM model implementation
│       ├── nodes/
│       │   ├── __init__.py
│       │   ├── basic_node.py           # Basic chatbot processing node
│       │   ├── tavily_node.py          # Web search node using Tavily
│       │   └── news_node.py            # News fetching and summarization node
│       ├── states/
│       │   ├── __init__.py
│       │   └── state.py                # LangGraph state definitions
│       ├── tools/
│       │   ├── __init__.py
│       │   └── tavily.py               # Tavily tool configuration
│       └── ui/
│           ├── __init__.py
│           ├── ui_config.ini           # UI configuration file
│           ├── ui_config.py            # Configuration loader
│           └── streamlit/
│               ├── __init__.py
│               ├── load.py             # Streamlit UI components loading
│               └── response.py         # Response display logic
```

---

## 🧠 Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    STREAMLIT UI LAYER                       │
│  (User Input → Configuration → Model Selection)             │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                 INITIALIZATION LAYER                        │
│  (InitializeChatbot → Model Loading → Graph Setup)          │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  LANGGRAPH LAYER                            │
│  (Graph Building → State Management → Node Execution)       │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐ ┌────▼─────┐ ┌─────▼──────┐
│ BASIC NODE   │ │TAVILY NODE│ │ NEWS NODE  │
│              │ │           │ │            │
│Basic Chat    │ │Web Search │ │News Fetch& │
│Processing    │ │with Tools │ │Summarize   │
└──────────────┘ └─────┬─────┘ └────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  LLM LAYER                                  │
│  (Groq, OpenAI*, Gemini*) - *Coming Soon                    │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **User Input**: User provides message and configuration via Streamlit UI
2. **Initialization**: `InitializeChatbot` loads UI and initializes LLM model
3. **Graph Building**: `GraphBuilder` constructs appropriate graph based on use case
4. **Execution**: LangGraph executes the graph with the user message as input
5. **Response**: Output is collected and displayed in Streamlit

---

## 🤖 Available Models

### Supported LLMs

| Model Provider | Status | Notes |
|---|---|---|
| **Groq** | ✅ Active | Fast inference, currently primary model |
| **OpenAI** | 🔄 TODO | GPT-4, GPT-3.5 integration coming soon |
| **Google Gemini** | 🔄 TODO | Gemini Pro integration in development |

### Using Groq Models

Groq provides fast, open-source LLM inference. Supported models include:
- `mixtral-8x7b-32768`
- `llama2-70b-4096`
- `llama-2-7b-chat`

Get your API key at: [Groq Console](https://console.groq.com)

---

## 💡 Use Cases

### 1. **Basic Chatbot**
A simple conversational chatbot without external tools.

**Architecture**: User Input → LLM Processing → Response

**When to use**: General conversation, Q&A, creative writing

```
Flow: START → BasicChatbotNode → END
```

### 2. **Chatbot with Tool** (Web Search)
Integrates Tavily web search for real-time information retrieval.

**Architecture**: User Query → LLM with Tool Binding → Tavily Search → Tool Node → LLM Response

**When to use**: Current events, weather, statistics, research questions

```
Flow: START → TavilyNode → Tools Condition → ToolNode → TavilyNode → END
```

**Features**:
- Real-time web search results
- Up-to-date information retrieval
- Tool integration with LLM reasoning

### 3. **AI News Aggregator**
Fetches and summarizes news articles from multiple sources using Tavily.

**Architecture**: News Topic → Tavily Fetch → Article Collection → LLM Summarization → Summary Output

**When to use**: News summaries, trend analysis, topical updates

```
Flow: START → fetch_news → summarize_news → END
```

**Features**:
- Time-range filtering (Daily, Weekly, Monthly, Yearly)
- Multi-source aggregation
- AI-powered summarization
- Structured output with key points and sources

### 4. **Blog Generator** (TODO)
Generates blog posts based on user input and research.

**Status**: Under development

---

## 🛠️ Tools & Integrations

### Tavily Search

**Purpose**: Real-time web search and news retrieval

**Integration Points**:
- `tools/tavily.py` - Tool configuration
- `nodes/tavily_node.py` - Web search node implementation
- `nodes/news_node.py` - News-specific implementation

**API**: Get key at [Tavily](https://tavily.com)


**Configuration Options**:
- `max_results`: Maximum number of search results
- `time_range`: Filter by time (d, w, m, y)
- `topic`: Search topic filter (e.g., "news")
- `include_answer`: Include direct answer in results

### Tool Node

The `ToolNode` from LangGraph manages tool execution and integration with the LLM.

---

## 📖 Usage

### Basic Setup via UI

1. **Start the application**:
   ```bash
   streamlit run src/app.py
   ```

2. **Configure in sidebar**:
   - Select LLM provider (e.g., Groq)
   - Choose model (e.g., mixtral-8x7b-32768)
   - Enter API key
   - Select use case
   - For web search: Enter Tavily API key

3. **Enter message**: Type your query in the chat input

4. **Receive response**: View the AI-generated response with optional tool results

### Example Queries

#### Basic Chatbot
```
"What is the capital of France?"
"Explain quantum computing in simple terms"
```

#### Web Search Chatbot
```
"What is the current Bitcoin price?"
"What are the latest AI breakthroughs in 2024?"
```

#### News Aggregator
```
- Select "AI News" use case
- Set frequency: "Weekly"
- Query: "Artificial Intelligence updates"
- Response: Summarized news with key points and sources
```

---

## ⚙️ Configuration

### UI Configuration (`ui/ui_config.ini`)

```ini
[DEFAULT]
PAGE_TITLE = Chat-Boat
LLM_OPTIONS = GROQ,OPENAI,GEMINI
GROQ = mixtral-8x7b-32768,llama2-70b-4096
OPENAI = gpt-4,gpt-3.5-turbo
GEMINI = gemini-pro
USE_CASE_OPTIONS = Basic Chatbot,Chatbot with tool,AI News,Blog generator
TOOLS = Tavily
```

### Graph State Schema

Defined in `states/state.py`:

```python
class GraphState(TypedDict):
    messages: Annotated[List, add_messages]  # Chat messages history
    summary: List                              # Summarized content
    news_data: str                            # Fetched news data
    news_frequency: str                       # Time range for news
```

### Model Base Info Schema

Defined in `core/schema/input_control.py`:

```python
class ModelBaseInfo(BaseModel):
    selected_llm: str           # LLM provider
    selected_model: str         # Specific model name
    api_key: str               # LLM API key
    selected_use_case: str     # Application use case
```

---

## 🔑 API Keys Setup

### Groq API Key
1. Visit [Groq Console](https://console.groq.com)
2. Sign up or log in
3. Navigate to API Keys section
4. Create new API key
5. Copy and paste into Streamlit UI

### Tavily API Key
1. Visit [Tavily](https://tavily.com)
2. Sign up for an account
3. Go to dashboard
4. Copy your API key
5. Paste into the "Tavily API Key" field when using web search features

**Security Note**: API keys are treated as passwords. Never commit them to version control. Use `.gitignore` to exclude sensitive files.

---

## 🔧 Development

### Adding a New LLM Provider

1. Create a new file in `models/` (e.g., `models/openai.py`)
2. Extend `ModelBase` class
3. Implement `get_llm_model()` method
4. Add to `ModelNameEnum` in `core/enum/model.py`
5. Update `core/schema/input_control.py` if needed
6. Add case in `main.py` `_get_llm_model()` method

### Adding a New Use Case

1. Create node class in `nodes/` (e.g., `nodes/custom_node.py`)
2. Implement node logic inheriting from base patterns
3. Add use case to `ModelUseCaseEnum` in `core/enum/model.py`
4. Add graph building method in `graphs/graph_builder.py`
5. Add case in `setup_graph()` method

### Adding a New Tool

1. Create tool module in `tools/` (e.g., `tools/new_tool.py`)
2. Implement tool initialization and execution
3. Add to `ModelToolsEnum` in `core/enum/model.py`
4. Update UI configuration in `ui/ui_config.ini`
5. Add conditional logic in `ui/streamlit/load.py`

---

## 📝 Key Components Explained

### InitializeChatbot (`main.py`)
- Initializes the entire chatbot application
- Loads Streamlit UI
- Handles LLM model selection and initialization
- Manages graph building and execution
- Displays responses to users

### GraphBuilder (`graphs/graph_builder.py`)
- Constructs LangGraph graphs based on use case
- Manages node connections and state flow
- Supports different workflow patterns
- Compiles and returns executable graphs

### Node Classes
- **BasicChatbotNode**: Simple LLM inference
- **TavilyNode**: Web search integration with tool binding
- **NewsNode**: News fetching and summarization

### State Management
- Uses TypedDict for type-safe state definitions
- Supports message aggregation via `add_messages` reducer
- Maintains context across graph execution

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:


### Contribution Guidelines
- Follow PEP 8 style guide for Python code
- Add docstrings to functions and classes
- Include error handling and validation
- Test new features before submitting
- Update README for major changes

---

## 📄 License

This project is open source. See LICENSE file for details.

---


### Common Issues

**Issue**: "Module not found" error
- **Solution**: Ensure all dependencies are installed: `pip install -r requirements.txt`

**Issue**: Streamlit connection refused
- **Solution**: Ensure port 8501 is not in use. Run: `streamlit run src/app.py --logger.level=debug`

**Issue**: API key not working
- **Solution**: Verify API key is correct, has proper permissions, and is not expired

**Issue**: Graph execution fails
- **Solution**: Check API key validity, ensure models are available, verify internet connection for web search

---

---

## ✨ Features Highlights

✅ **Multi-Model Support** - Use different LLMs interchangeably
✅ **Real-Time Web Search** - Powered by Tavily
✅ **News Aggregation** - Summarize news with AI
✅ **Modular Architecture** - Easy to extend and customize
✅ **State Management** - Sophisticated workflow orchestration
✅ **User-Friendly UI** - Streamlit-based interface
✅ **Type Safety** - Pydantic schemas and TypedDict
✅ **Open Source** - Community-driven development

---

**Happy Chatting! **

