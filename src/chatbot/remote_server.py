import os
from chatbot.research_server import mcp

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=int(os.getenv("PORT", "8001")),
        stateless_http=True,
        json_response=True,
    )
    