from typing import Any, List, Dict
import streamlit as st
from src.chatbot.core.enum import ModelUseCaseEnum
from langchain.messages import HumanMessage, AIMessage, ToolMessage


class DisplayStreamlitResponse:
    def __init__(self, use_case:str, graph:Any, user_message: str, input_user: Dict):
        self.use_case = use_case
        self.graph = graph
        self.user_message = user_message
        self.user_input = input_user


    def display_response(self):
        use_case = ModelUseCaseEnum(self.use_case)
        # initialize persistent chat history in session_state
        if "chat_history" not in st.session_state:
            # each entry: {"role": "user"|"assistant", "content": str}
            st.session_state["chat_history"] = []

        # helper to render stored history
        def _render_history():
            for msg in st.session_state.get("chat_history", []):
                role = msg.get("role")
                content = msg.get("content")
                tools = msg.get("tools")
                if role == "user":
                    with st.chat_message("user"):
                        st.write(content)
                    if tools:   
                        with st.chat_message("assistant"):
                            st.write(tools)
                else:
                    with st.chat_message("assistant"):
                        if tools:   
                                st.write(tools)
                        st.write(content)

        # show previous messages first
        _render_history()

        if use_case == ModelUseCaseEnum.BASIC_CHATBOT:
            # record and render the user's message
            user_entry = {"role": "user", "content": self.user_message}
            st.session_state["chat_history"].append(user_entry)
            
            with st.chat_message("user"):
                st.write(self.user_message)

            # stream assistant response(s) and append to history
            assistant_text_parts: List[str] = []
            for event in self.graph.stream({"messages": HumanMessage(self.user_message)}):
                for value in event.values():
                    # value may contain a single message or a list under "messages"
                    raw = value.get("messages") if isinstance(value, dict) else value
                    msg = raw
                    if isinstance(raw, list):
                        msg = raw[0]

                    # extract text from message-like objects
                    text = ""
                    if hasattr(msg, "content"):
                        text = getattr(msg, "content")
                    elif isinstance(msg, dict) and "content" in msg:
                        text = msg["content"]

                    if text:
                        assistant_text_parts.append(text)

            assistant_full = "\n".join(assistant_text_parts).strip()
            if assistant_full:
                st.session_state["chat_history"].append({"role": "assistant", "content": assistant_full})
                with st.chat_message("assistant"):
                    st.write(assistant_full)

       
        
        elif use_case == ModelUseCaseEnum.CHAT_WITH_TOOL or use_case == ModelUseCaseEnum.AI_NEWS:
            # record and render the user's message
            try:
                user_entry = {"role": "user", "content": self.user_message}
                st.session_state["chat_history"].append(user_entry)
                with st.chat_message("user"):
                    st.write(self.user_message)

                with st.chat_message("assistant"):
                    tools_placeholder = st.empty()
                    tools_placeholder.markdown("Thinking...")
                
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    message_placeholder.markdown("Thinking...")

                assistant_text_parts: List[str] = []
                used_tools_str = ""
                news_frequency = self.user_input.get("news_frequency", "")
                
                for response in self.graph.stream({"messages":HumanMessage(self.user_message), "news_frequency":news_frequency}):
                    for event in response.values():
                        raw = event.get("messages") if isinstance(event, dict) else event
                        if isinstance(raw, list) and len(raw) > 0:
                            message = raw[0]
                        else:
                            message = raw

                        if type(message) == HumanMessage:
                            continue
                        
                        elif type(message) == AIMessage:
                            if message.content:
                                # accumulate streamed assistant chunks and update placeholder
                                assistant_text_parts.append(message.content)
                                # update the message placeholder with accumulated content
                                message_placeholder.markdown("\n".join(assistant_text_parts))
                                
                            if len(message.tool_calls):
                                used_tools_str += ", ".join(tool.get("name", "") for tool in message.tool_calls)
                                tools_placeholder.markdown(used_tools_str)
                                                    

                assistant_full = "\n".join(assistant_text_parts).strip()
                if assistant_full:
                    st.session_state["chat_history"].append({"role": "assistant", "content": assistant_full, "tools":used_tools_str})
            except Exception as e:
                with st.chat_message("assistant"):
                    st.session_state["chat_history"].append({"role": "assistant", "content": str(e), "tools":used_tools_str})
                    message_placeholder.markdown(str(e))

                
        else:
            return





     # elif use_case == ModelUseCaseEnum.CHAT_WITH_TOOL:
        #     response = self.graph.invoke({"messages":HumanMessage(self.user_message)})
        #     for message in response["messages"]:
        #         if type(message)  == HumanMessage:
        #             with st.chat_message("user"):
        #                 st.write(message.content)
        #         # want to display the tool message
        #         # elif type(message)  == ToolMessage:
        #         #     print("tool message")
        #         #     with st.chat_message("ai"):
        #         #         st.write(message.content)
                
        #         elif type(message)  == AIMessage and message.content:
        #             print("assistant message")
        #             with st.chat_message("assistant"):
        #                 st.write(message.content)
                        
        #         elif type(message)  == AIMessage and len(message.tool_calls):
        #             with st.chat_message("assistant"):
        #                 st.write(", ".join(tool.get("name", "") for tool in message.tool_calls))