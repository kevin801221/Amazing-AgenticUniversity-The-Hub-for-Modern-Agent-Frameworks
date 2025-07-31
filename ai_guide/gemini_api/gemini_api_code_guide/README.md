# Gemini API 使用指南與注意事項

本文件總結了在整合 Google Gemini API 過程中遇到的關鍵問題與最佳實踐。遵循此指南可以有效避免因環境、套件版本不匹配而導致的常見錯誤。

## 1. 環境設定 (Environment Setup)

為避免套件衝突，強烈建議使用獨立的虛擬環境。

**建議使用 `uv` 進行管理：**

1.  **建立虛擬環境：**
    ```bash
    uv venv
    ```

2.  **啟用環境：**
    ```bash
    source .venv/bin/activate
    ```

3.  **安裝必要的基礎套件：**
    ```bash
    uv pip install google-generativeai python-dotenv
    ```
    *   若需要處理結構化資料，可以再安裝 `pydantic`。

---

## 2. 關鍵實踐準則 (Key Best Practices)

以下是我們透過偵錯得出的三大核心準則，請務必遵守。

### 準則一：使用正確的導入方式

-   **應該 (Do):**
    ```python
    import google.generativeai as genai
    ```

-   **不應該 (Don't):**
    ```python
    from google import genai
    ```

-   **原因**：`from google import genai` 的寫法會與環境中其他 `google-*` 開頭的套件（如 `google-cloud-storage`）產生命名空間衝突，導致 `ImportError`。使用完整的路徑 `google.generativeai` 是最穩定、最不會出錯的方法。

### 準則二：使用正確的客戶端初始化方式

-   **應該 (Do):**
    ```python
    model = genai.GenerativeModel(model_name="gemini-2.5-flash")
    ```

-   **不應該 (Don't):**
    ```python
    client = genai.Client()
    ```

-   **原因**：`genai.Client()` 是出現在較新、但尚未對外公開的函式庫版本中的物件。當前透過 `pip` 或 `uv` 安裝的公開版本中，正確的初始化方式是使用 `genai.GenerativeModel()`。

### 準則三：使用手動定義的 JSON Schema

-   **建議 (Recommended):**
    ```python
    # 手動定義一個字典作為 Schema
    MANUAL_SCHEMA = {
        "type": "array",
        "items": { "type": "object", "properties": { ... } }
    }
    
    generation_config = genai.types.GenerationConfig(
        response_mime_type="application/json",
        response_schema=MANUAL_SCHEMA,
    )
    ```

-   **謹慎使用 (Use with Caution):**
    ```python
    # 直接傳遞 Pydantic 模型
    from pydantic import BaseModel
    class MySchema(BaseModel):
        ...
    
    generation_config = genai.types.GenerationConfig(
        response_mime_type="application/json",
        response_schema=MySchema,
    )
    ```

-   **原因**：雖�� SDK 支援 Pydantic，但我們在實測中發現，SDK 內部將 Pydantic 模型轉換為 JSON Schema 的功能可能不夠穩定，對於 `RootModel` 或其他複雜結構的支援有限，容易觸發 `Unknown field: $ref` 或 `unbound method` 等內部錯誤。**手動定義一個簡單的字典作為 Schema 是最可靠、最不會出錯的方法。**

---

## 3. 模型可用性問題 (Model Availability)

-   **症狀**：即使程式碼完全正確，依然收到 `404 Not Found` 錯誤。
    ```
    404 models/veo-2.0-generate-001 is not found for API version v1beta...
    ```

-   **診斷**：這通常不代表程式碼錯誤，而是代表**您的 API 金鑰沒有使用該模型的權限**。

-   **原因**：許多新模型（如 VEO）在發布初期處於**有限預覽 (Limited Preview)** 階段，需要額外申請或被加入白名單才能使用。

-   **解決方案**：
    1.  前往 Google Cloud Console 確認您的帳號權限與專案狀態。
    2.  聯繫 Google Cloud Support 詢問模型存取權限。
    3.  等待模型正式對所有開發者公開。

---

**參考範例：**
*   **結構化資料生成**：請參考 `gemini_structured.py`，它使用了上述所有最佳實踐。
*   **影片生成**：請參考 `gemini_api_VEO.py`，它展示了正確的程式碼結構，但請注意，其中的 VEO 模型在您獲得權限前將無法使用。
