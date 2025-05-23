
import json
from datetime import timedelta
from typing import cast

from langchain_core.messages import AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from shared.models import llm


class Agent():
    def __init__(
        self,
        tools: list
    ):
        self.tools = tools
        self.tool_node = ToolNode(self.tools)
        graph = StateGraph(MessagesState)

        # definitions
        graph.add_node(self.call_model)
        graph.add_node(self.tool_node)

        # navigation
        graph.set_entry_point(self.call_model.__name__)
        graph.add_conditional_edges(
            self.call_model.__name__,
            self.should_call_tool_or_end,
        )
        graph.add_edge(self.tool_node.name, self.call_model.__name__)

        self.graph = graph.compile()
        self.graph.get_graph().print_ascii()


    @classmethod
    async def create(
        cls,
        auth_header: str,
        mcp_urls: dict[str, str]
    ):
        mcp_client = MultiServerMCPClient(
            {
                key: {
                    "transport": "streamable_http",
                    "timeout": timedelta(seconds=100),
                    "sse_read_timeout": timedelta(seconds=100),
                    "url": url,
                    "headers": {
                        "Authorization": f"Bearer {auth_header}"
                    },
                    "session_kwargs": None,
                    "terminate_on_close": True
                } for (key, url) in mcp_urls.items()
            }
        )
        tools = await mcp_client.get_tools()
        return cls(tools)

    async def call_model(self, state: MessagesState):
        print("Calling Model")
        print(state)
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                        Use tools when needed instead of asking permission.
                        Don't reference the tool use in your response content.
                    """.strip(),
                ),
                *state["messages"],
            ]
        )
        chain = prompt | llm.bind_tools(self.tools)
        response = await chain.ainvoke({})
        return {"messages": [response]}
    

    def should_call_tool_or_end(self, state: MessagesState):
        last_message = cast(AIMessage, state["messages"][-1])
        if last_message.tool_calls:
            print(f"Calling tool(s): {json.dumps(last_message.tool_calls, indent=2)}")
            return self.tool_node.name
        return END