# Gemini API 文字生成教學

## 快速開始

### 開始之前

您需要一個 Gemini API 金鑰。如果您還沒有，可以在 [Google AI Studio](https://aistudio.google.com/) 免費取得。

### 安裝 Google GenAI SDK

使用 Python 3.9+，透過以下 pip 指令安裝 `google-genai` 套件：

```bash
pip install -q -U google-genai
```

### 進行第一次請求

以下是使用 `generateContent` 方法向 Gemini API 發送請求的範例，使用 Gemini 2.5 Flash 模型：

```python
from google import genai

# 客戶端會從環境變數 `GEMINI_API_KEY` 自動取得 API 金鑰
client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents="Explain how AI works in a few words"
)
print(response.text)
```

**重要提醒**：如果您將 API 金鑰設定為環境變數 `GEMINI_API_KEY`，Gemini API 函式庫會自動識別。否則，您需要在初始化客戶端時將 API 金鑰作為參數傳入。

### 設定環境變數

在終端機中設定 API 金鑰：

```bash
# Windows
set GEMINI_API_KEY=your-api-key-here

# macOS/Linux
export GEMINI_API_KEY=your-api-key-here
```

## 概述

Gemini API 可以從各種輸入（包括文字、圖片、影片和音訊）生成文字輸出，並使用 Gemini 模型來實現。

## 基本文字生成

這是一個接受單一文字輸入的基本範例：

```python
from google import genai

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="How does AI work?"
)
print(response.text)
```

## Gemini 2.5 的思考功能

### 預設啟用思考功能

2.5 Flash 和 Pro 模型預設啟用「思考」功能來增強品質，但這可能會增加執行時間和 token 使用量。

### 停用思考功能

在使用 2.5 Flash 時，您可以透過將思考預算設為零來停用思考功能：

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in a few words",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0)  # 停用思考功能
    ),
)
print(response.text)
```

**注意**：許多程式碼範例使用 Gemini 2.5 Flash 模型，該模型預設啟用「思考」功能以提升回應品質。您應該知道這可能會增加回應時間和 token 使用量。如果您優先考慮速度或希望降低成本，可以透過將思考預算設為零來停用此功能。思考功能僅在 Gemini 2.5 系列模型上可用，且無法在 Gemini 2.5 Pro 上停用。

## 系統指令與其他配置

### 系統指令

您可以使用系統指令來引導 Gemini 模型的行為。透過傳遞 `GenerateContentConfig` 物件來實現：

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a cat. Your name is Neko."),
    contents="Hello there"
)

print(response.text)
```

### 調整生成參數

`GenerateContentConfig` 物件也允許您覆蓋預設的生成參數，例如溫度值：

```python
from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=["Explain how AI works"],
    config=types.GenerateContentConfig(
        temperature=0.1
    )
)
print(response.text)
```

## 多模態輸入

### 圖片輸入

Gemini API 支援多模態輸入，允許您將文字與媒體檔案結合。以下範例展示如何提供圖片：

```python
from PIL import Image
from google import genai

client = genai.Client()

image = Image.open("/path/to/organ.png")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=[image, "Tell me about this instrument"]
)
print(response.text)
```

### 其他媒體格式

API 也支援文件、影片和音訊輸入與理解。

## 串流回應

### 為什麼使用串流

預設情況下，模型只有在整個生成過程完成後才會回傳回應。為了更流暢的互動，可以使用串流來逐步接收 `GenerateContentResponse` 實例。

```python
from google import genai

client = genai.Client()

response = client.models.generate_content_stream(
    model="gemini-2.5-flash",
    contents=["Explain how AI works"]
)
for chunk in response:
    print(chunk.text, end="")
```

## 多輪對話（聊天）

### 基本聊天功能

SDK 提供功能來收集多輪提示和回應到聊天中，讓您輕鬆追蹤對話歷史。

> **注意**：聊天功能僅作為 SDK 的一部分實現。在後台，它仍然使用 generateContent API。對於多輪對話，完整的對話歷史會在每個後續回合中發送給模型。

```python
from google import genai

client = genai.Client()
chat = client.chats.create(model="gemini-2.5-flash")

response = chat.send_message("I have 2 dogs in my house.")
print(response.text)

response = chat.send_message("How many paws are in my house?")
print(response.text)

for message in chat.get_history():
    print(f'role - {message.role}', end=": ")
    print(message.parts[0].text)
```

### 聊天串流

串流也可以用於多輪對話：

```python
from google import genai

client = genai.Client()
chat = client.chats.create(model="gemini-2.5-flash")

response = chat.send_message_stream("I have 2 dogs in my house.")
for chunk in response:
    print(chunk.text, end="")

response = chat.send_message_stream("How many paws are in my house?")
for chunk in response:
    print(chunk.text, end="")

for message in chat.get_history():
    print(f'role - {message.role}', end=": ")
    print(message.parts[0].text)
```

## 支援的模型

Gemini 系列中的所有模型都支援文字生成。要了解更多關於模型及其功能的資訊，請造訪模型頁面。

## 最佳實踐

### 提示技巧

**基本文字生成**：零樣本提示通常就足夠了，無需範例、系統指令或特定格式。

**客製化輸出**：
- 使用系統指令來引導模型
- 提供少數範例輸入和輸出來引導模型（通常稱為少樣本提示）

### 結構化輸出

在某些情況下，您可能需要結構化輸出，例如 JSON。請參考結構化輸出指南以了解如何實現。

## 下一步

現在您已經完成了第一次 API 請求，您可能想要探索以下指南，了解 Gemini 的實際應用：

- **思考功能** - 了解 Gemini 2.5 的思考機制
- **文字生成** - 深入了解文字生成功能
- **視覺理解** - 探索圖片和影片處理能力
- **長文本處理** - 處理大量文本內容
- **嵌入向量** - 文本向量化和語義搜索

## 重要參考資源

- API 參考文檔中的 `GenerateContentConfig` 完整參數列表
- 提示工程指南
- 圖片理解指南
- 結構化輸出指南
- 思考功能指南

---

*本教學基於 Gemini API 官方文檔整理，適合初學者到進階使用者參考。*