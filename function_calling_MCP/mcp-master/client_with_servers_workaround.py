from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from contextlib import AsyncExitStack
from openai import OpenAI
from dotenv import load_dotenv
import asyncio
import json
import sys
import os

load_dotenv()
openai = OpenAI()

class MCPClient:
    def __init__(self):
        self.session = None
        self.exit_stack = AsyncExitStack()
        self.tools = []
        self.tool_names = []

    async def connect_to_server(self, server_info):
        """連接 MCP 伺服器

        Args:
            server_info: MCP 伺服器的連接資訊
        """

        server_params = StdioServerParameters(**server_info[1])

        stdio_transport = await (
            self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
        )
        self.read, self.write = stdio_transport
        self.session = await (
            self.exit_stack.enter_async_context(
                ClientSession(self.read, self.write)
            )
        )

        await self.session.initialize()

        # 取得 MCP 伺服器提供的工具資訊
        response = await self.session.list_tools()
        tools = response.tools
        for tool in tools:
            tool.inputSchema.pop('oneOf', None)
            tool.inputSchema.pop('allOf', None)
            self.tools.append({
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            })
        self.tool_names = [tool.name for tool in tools]

        print('-' * 20)
        print(f"已連接 {server_info[0]} 伺服器")
        print('\n'.join(
            [f'    - {name}' for name in self.tool_names]
        ))
        print('-' * 20)

    async def cleanup(self):
        """釋放資源"""
        await self.exit_stack.aclose()

async def get_reply_text(clients, query, prev_id):
    """單次問答"""
    
    messages = [{"role": "user", "content": query}]
    # 把 clients 中個別項目的 tools 串接在一起
    tools = []
    for client in clients:
        tools += client.tools

    while True:
        # 使用 Responses API 請 LLM 生成回覆
        response = openai.responses.create(
            # model="gpt-4.1-mini",
            model="gpt-4.1",
            input=messages,
            tools=tools,
            previous_response_id=prev_id,
        )

        # 處理回應並執行工具
        final_text = []
        messages = []

        prev_id = response.id
        for output in response.output:
            if output.type == 'message': # 一般訊息
                final_text.append(output.content[0].text)
            elif output.type == 'function_call': # 使用工具
                tool_name = output.name
                tool_args = eval(output.arguments)
                for client in clients:
                    if tool_name in client.tool_names:
                        break
                else:
                    # 如果沒有找到對應的工具，則跳過這個迴圈
                    continue
                print(f"準備使用 {tool_name}(**{tool_args})")
                print('-' * 20)
                # 使用 MCP 伺服器提供的工具
                result = await client.session.call_tool(
                    tool_name, tool_args
                )
                print(f"{result.content[0].text}")
                print('-' * 20)

                messages.append({
                    # 建立可傳回函式執行結果的字典
                    "type": "function_call_output", # 設為工具輸出類型的訊息
                    "call_id": output.call_id, # 叫用函式的識別碼
                    "output": result.content[0].text # 函式傳回值
                })
        if messages == []:
            break
    return "\n".join(final_text), prev_id

async def chat_loop(clients):
    """聊天迴圈"""
    print("直接按 ↵ 可結束對話")

    prev_id = None
    while True:
        try:
            query = input(">>> ").strip()

            if query == '':
                break

            reply, prev_id = await get_reply_text(
                clients, query, prev_id
            )
            print(reply)

        except Exception as e:
            print(f"\nError: {str(e)}")

async def main():
    if (not os.path.exists("mcp_servers.json") or
        not os.path.isfile("mcp_servers.json")):
        print("Error:找不到 mcp_servers.json 檔", file=sys.stderr)
        return
    
    with open("mcp_servers.json", "r", encoding="utf-8") as f:
        try:
            server_infos = tuple(
                json.load(f)['mcpServers'].items()
            )
        except:
            print(
                "Error: mcp_servers.json 檔案格式錯誤", 
                file=sys.stderr
            )
            return
    
    if len(server_infos) == 0:
        print(
            "Error: mcp_servers.json 檔案內沒有任何伺服器", 
            file=sys.stderr
        )
        return
    
    clients = []
    try:
        for server_info in server_infos:
            client = MCPClient()
            await client.connect_to_server(server_info)
            clients.append(client)
        await chat_loop(clients)
    finally:
        # 反向清除資源，確保所有伺服器都能正常關閉
        for client in clients[::-1]:
            await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
