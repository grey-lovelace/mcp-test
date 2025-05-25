Example of a quick MCP Server and MCP Client as Langgraph Agent.

It is recommended to use the dev container

1. Run `poetry install`
2. Get AWS credentials loaded. It currently uses the `dev` profile to talk to AWS bedrock, but you can change it to whatever yours is named in `src/shared/models.py`.
3. Run `poetry run python src/tools.py` to start the MCP server.
4. In a new terminal run `poetry run python src/client.py` to start the FastAPI server that runs our Langgraph agent.
5. Call GET `localhost:8001/test` to invoke the agent with a stock prompt.

### NOTE

This was originally created to test phoenix MCP traces, but the phoenix code is all commented out for now. This also means there is no need to start the docker compose file right now.