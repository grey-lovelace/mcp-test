
import uvicorn
from fastapi import FastAPI

from shared.agent import Agent

app = FastAPI()

@app.get("/test")
async def test():
    agent = await Agent.create(
        auth_header="1234", # Will come from the auth passed in to FastAPI normally
        mcp_urls={
            "jokes": "http://localhost:8000/mcp"
        }
    )
    resp = await agent.graph.ainvoke({"messages": "Tell me a joke about being bald"})
    return resp

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)