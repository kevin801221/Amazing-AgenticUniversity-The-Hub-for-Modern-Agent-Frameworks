# 匯入 os 模組，用於讀取環境變數
import os
# 匯入 requests 模組，用於發送 HTTP 請求
import requests
# 匯入 json 模組，用於處理 JSON 格式的數據
import json
# 從 langchain.tools 匯入 tool 裝飾器，用於將一個普通函數轉換為 LangChain 工具
from langchain.tools import tool

# 定義一個名為 SearchTools 的類別，用於封裝所有與搜索相關的工具
class SearchTools:

    # 使用 @tool 裝飾器，將下面的 searchInfo 函數定義為一個 LangChain 工具
    # 這樣 crewAI 的代理就能夠識別並使用這個工具
    @tool
    def searchInfo(query: str):
        """在網上搜索關於指定內容的相關信息"""
        # 這個工具的實際功能是調用下面的 search 方法來完成的
        # 這裡的 docstring (文檔字符串) 非常重要，它會被 LLM 用來理解這個工具的功能和用途
        return SearchTools.search(query)

    # 這是一個靜態方法，負責執行實際的網絡搜索邏輯
    def search(query: str):
        # Serper API 的端點 URL
        url = "https://google.serper.dev/news"

        # 準備要發送給 API 的 payload (負載)
        # 這裡我們將搜索查詢 (query) 和一些參數 (如語言 'hl') 轉換為 JSON 字符串
        payload = json.dumps({
            "q": query,
            "hl": "zh-tw"  # 指定搜索結果的語言為繁體中文
        })
        
        # 準備 HTTP 請求的 headers (標頭)
        headers = {
            # 從環境變數中讀取 SERPER_API_KEY，這是 API 的認證金鑰
            'X-API-KEY': os.environ['SERPER_API_KEY'],
            # 指定請求內容的格式為 JSON
            'Content-Type': 'application/json'
        }

        # 使用 requests.request 方法發送一個 POST 請求
        response = requests.request("POST", url, headers=headers, data=payload)

        # 解析 API 返回的 JSON 響應，並提取 'news' 鍵對應的值，這部分是新聞列表
        results = response.json()['news']

        # 創建一個空列表，用來存放格式化後的新聞字符串
        string = []
        # 遍歷每一條新聞結果
        for result in results:
            try:
                # 將每條新聞的標題、日期、來源和摘要等信息格式化為一個字符串
                string.append('\n'.join([
                    f"標題: {result['title']}",
                    f"時間: {result['date']}",
                    f"來源: {result['source']}",
                    f"摘要: {result['snippet']}",
                    "\n-----------------"  # 添加分隔線，使輸出更清晰
                ]))
            except KeyError:
                # 如果某條新聞缺少了某個鍵 (如 'title')，會引發 KeyError
                # 這裡使用 try-except 來捕捉這個錯誤，並簡單地跳過這條新聞，避免程式中斷
                next

        # 使用 '\n'.join() 將所有格式化後的新聞字符串合併成一個大的字符串
        content = '\n'.join(string)
        # 在最終結果的開頭加上 "Search result: "，然後返回
        return f"\nSearch result: {content}\n"}