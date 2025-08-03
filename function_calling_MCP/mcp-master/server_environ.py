from mcp.server.fastmcp import FastMCP
import os

mcp = FastMCP("show_env")

@mcp.tool()
async def show_env() -> str:
    """顯示環境變數
    """
    content = ""
    for key, value in os.environ.items():
        content += f"- {key}: {value}\n"
    return content

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')