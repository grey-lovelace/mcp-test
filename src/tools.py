from fastmcp import FastMCP
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from shared.models import llm
# from shared.models import tracer_provider

mcp = FastMCP("Jokes", instructions="""
    Use these tools to create jokes of different varieties.
""")
# tracer = tracer_provider.get_tracer("misc_tools")

@mcp.tool()
# @tracer.tool(name="MCP.limerick")
async def limerick(subject_matter: str) -> str:
    """Tells a knock knock joke about a subject matter."""
    template = ChatPromptTemplate.from_messages([
        ("human", "Create the most hilarious limerick you can about {subject_matter}")
    ])
    chain = template | llm | StrOutputParser()
    return await chain.ainvoke({"subject_matter": subject_matter})

@mcp.tool()
# @tracer.tool(name="MCP.knock_knock")
async def knock_knock(subject_matter: str) -> str:
    """Tells a knock knock joke about a subject matter."""
    template = ChatPromptTemplate.from_messages([
        ("human", "Create the most hilarious knock knock joke you can about {subject_matter}")
    ])
    chain = template | llm | StrOutputParser()
    return await chain.ainvoke({"subject_matter": subject_matter})

if __name__ == "__main__":
    mcp.run(transport="streamable-http")