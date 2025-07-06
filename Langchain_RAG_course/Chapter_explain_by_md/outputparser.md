# 輸出解析器

本章節介紹了 LangChain 中各種輸出解析器的使用，這些解析器可將語言模型的輸出轉換為結構化格式。

## 檔案

- **01-PydanticOutputParser.ipynb**: 示範如何使用 `PydanticOutputParser` 將語言模型的輸出轉換為 Pydantic 物件，從而實現類型安全和資料驗證。
- **02-CommaSeparatedListOutputParser.ipynb**: 解釋如何使用 `CommaSeparatedListOutputParser` 將模型的輸出解析為逗號分隔的清單。
- **03-StructuredOutputParser.ipynb**: 介紹 `StructuredOutputParser`，一個用於將輸出解析為具有多個欄位的字典結構的工具，特別適用於功能較弱的模型。
- **04-JsonOutputParser.ipynb**: 示範如何使用 `JsonOutputParser` 將模型的輸出解析為 JSON 格式。
- **05-PandasDataFrameOutputParser.ipynb**: 解釋如何使用 `PandasDataFrameOutputParser` 將模型的輸出解析為 Pandas DataFrame，以便於資料分析和處理。
- **06-DatetimeOutputParser.ipynb**: 介紹 `DatetimeOutputParser`，一個用於將模型的輸出解析為 `datetime` 物件的工具。
- **07-EnumOutputParser.ipynb**: 示範如何使用 `EnumOutputParser` 將模型的輸出解析為預定義的列舉（Enum）值之一。
- **08-OutputFixingParser.ipynb**: 解釋如何使用 `OutputFixingParser` 自動修正格式不正確的輸出，確保其符合預期的結構。

## 核心概念

- **PydanticOutputParser**: 提供了一種強大的方式來定義和驗證模型的輸出，確保其符合預期的 Pydantic 模型。
- **CommaSeparatedListOutputParser**: 一個簡單而有效的工具，用於將模型的輸出解析為清單，便於後續處理。
- **StructuredOutputParser**: 一個靈活的解析器，允許您定義自訂的輸出結構，並將模型的輸出解析為該結構。
- **JsonOutputParser**: 一個通用的解析器，可將模型的輸出解析為 JSON 格式，便於與其他系統整合。
- **PandasDataFrameOutputParser**: 對於資料科學家和分析師來說，這是一個非常有用的工具，可將模型的輸出直接轉換為 Pandas DataFrame。
- **DatetimeOutputParser**: 處理日期和時間相關的輸出時，這個解析器可以確保輸出格式的一致性和正確性。
- **EnumOutputParser**: 當您需要模型的輸出是預定義選項之一時，這個解析器可以確保輸出的有效性。
- **OutputFixingParser**: 一個非常有用的工具，可以自動修正格式不正確的輸出，提高應用的穩定性和可靠性。
