from typing import TypedDict, List, Dict

common_messages: List[Dict[str, str]] = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Say hello!"}
]