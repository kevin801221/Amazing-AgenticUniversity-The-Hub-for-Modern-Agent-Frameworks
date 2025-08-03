from googlesearch import search
from pydantic import BaseModel, Field


# 描述 google_res 工具函式的參數
class GoogleRes(BaseModel):
    keyword: str = Field(description="要搜尋的關鍵字")
    num_results: int = Field(description="搜尋結果數目，不提供預設 5 筆")


tools = [
    {
        "type": "function",
        "name": "google_res",
        "description": "取得 Google 搜尋結果",
        "parameters": GoogleRes.model_json_schema(),
    }
]


def google_res(keyword, num_results=5):
    content = ""
    num_results = max(num_results, 5)  # 最少 5 筆
    for result in search(  # 一一串接搜尋結果
        keyword, advanced=True, num_results=num_results, lang="zh-TW"
    ):
        # 使用 markdown 格式整理搜尋結果
        content += f"- [{result.title}]({result.url})\n" f"    {result.description}\n"
    return content


# 叫用單一函式並且將函式執行結果組成訊息後傳回
def make_tool_msg(tool_call):
    tool_info = f"{tool_call.name}(**{tool_call.arguments})"
    result = eval(tool_info)
    return {  # 建立可傳回函式執行結果的字典
        "type": "function_call_output",  # 以工具角色送出回覆
        "call_id": tool_call.call_id,  # 叫用函式的識別碼
        "output": result,  # 函式傳回值
    }


def call_tools(tool_calls):
    msgs = []
    for tool_call in tool_calls:
        if tool_call.type == "function_call":
            msgs.append(make_tool_msg(tool_call))
    return msgs

def show_tools_info(response):
    for tool_call in response.output:
        if tool_call.type == 'function_call':
            tool_info = (
                f'{tool_call.name}'
                f'(**{tool_call.arguments})'
            )
            print(tool_info)