# 設定指南

## 環境設定

要設定建構文檔所需的相依套件，您可以執行以下指令：

```bash
uv sync --group test
```

這個指令會使用 `uv` 套件管理工具來同步安裝測試群組中定義的所有相依套件。`uv` 是一個快速的 Python 套件管理工具，類似於 `pip` 但效能更佳。

## 本地運行文檔伺服器

要在本地啟動文檔伺服器，您可以執行：

```bash
make serve-docs
```

這將會在 [http://127.0.0.1:8000/langgraph/](http://127.0.0.1:8000/langgraph/) 啟動文檔伺服器。您可以在瀏覽器中開啟這個網址來查看本地建構的文檔。

## 執行 Jupyter Notebook

### 自動執行所有筆記本

如果您想要自動執行所有的 Jupyter notebook，以模擬 GitHub Actions 中的「Run notebooks」工作流程，您可以執行：

```bash
python _scripts/prepare_notebooks_for_ci.py
./_scripts/execute_notebooks.sh
```

### 跳過套件安裝指令執行

**注意**：如果您想要執行筆記本但跳過 `%pip install` 儲存格（例如您已經安裝了所需套件），您可以執行：

```bash
python _scripts/prepare_notebooks_for_ci.py --comment-install-cells
./_scripts/execute_notebooks.sh
```

### 關於虛擬環境的重要說明

**您不需要手動進入 `.venv` 虛擬環境！**

使用 `uv` 工具的重要優勢之一就是它會自動管理虛擬環境：

#### 為什麼不需要手動啟用虛擬環境：

1. **自動環境管理**：
   - 當您執行 `uv sync --group test` 時，`uv` 會自動創建並管理 `.venv` 目錄
   - 所有依賴都會安裝到這個虛擬環境中

2. **智能腳本執行**：
   - `_scripts/execute_notebooks.sh` 腳本會自動使用正確的 Python 環境
   - 腳本知道如何找到並使用 `.venv` 中安裝的套件

3. **路徑自動解析**：
   - 在 `docs` 目錄中執行 `python` 時，系統會自動使用 `.venv/bin/python`
   - 所有依賴都會從 `.venv/lib/python3.x/site-packages/` 中載入

#### 推薦的執行流程：

```bash
# 1. 確保在 docs 目錄中
cd docs

# 2. 安裝依賴（只需執行一次）
uv sync --group test

# 3. 直接執行腳本（無需手動啟用虛擬環境）
python _scripts/prepare_notebooks_for_ci.py --comment-install-cells
./_scripts/execute_notebooks.sh
```

#### 如何驗證環境設定：

```bash
# 檢查當前使用的 Python 路徑
which python

# 檢查已安裝的套件
pip list
```

這是現代 Python 工具的便利之處 - 自動化的環境管理讓開發更加簡單！

### VCR Cassette 機制說明

`prepare_notebooks_for_ci.py` 腳本會為筆記本中的每個儲存格添加 VCR cassette 上下文管理器，其運作機制如下：

* **首次執行**：當筆記本第一次執行時，包含網路請求的儲存格會將其網路請求和回應記錄到 VCR cassette 檔案中
* **後續執行**：當筆記本再次執行時，包含網路請求的儲存格會從 cassette 檔案中重播先前記錄的回應，而不會發出真實的網路請求

這種機制的優點：
- 提高執行速度（避免重複的網路請求）
- 降低 API 使用成本
- 確保測試結果的一致性
- 在沒有網路連線時也能執行筆記本

## 新增筆記本

### 建議的最佳實務

如果您要新增包含 API 請求的筆記本，**強烈建議**記錄網路請求以便後續重播。如果不這樣做，筆記本執行器每次運行筆記本時都會發出 API 請求，這可能會：
- 產生不必要的費用
- 降低執行速度
- 依賴外部服務的可用性

### 記錄網路請求的步驟

1. 首先確保執行 `prepare_notebooks_for_ci.py` 腳本：

```bash
python _scripts/prepare_notebooks_for_ci.py
```

2. 然後執行您的筆記本：

```bash
jupyter execute <path_to_notebook>
```

將 `<path_to_notebook>` 替換為您筆記本的實際路徑。

3. 執行完成後，您應該會在 `cassettes` 目錄中看到新記錄的 VCR cassette 檔案，同時請丟棄更新後的筆記本檔案（因為它包含了執行結果，我們只需要 cassette 檔案）。

## 更新現有筆記本

### 更新流程

如果您要更新現有的筆記本，請務必：

1. **刪除舊的 cassette 檔案**：在 `cassettes` 目錄中移除該筆記本的所有現有 cassette 檔案（每個 cassette 檔案都以筆記本名稱作為前綴）

2. **重新記錄**：然後按照上述「新增筆記本」章節的步驟重新執行

### 刪除特定筆記本的 cassette 檔案

要刪除特定筆記本的 cassette 檔案，您可以執行：

```bash
rm cassettes/<notebook_name>*
```

將 `<notebook_name>` 替換為您的筆記本名稱（不包含 `.ipynb` 副檔名）。這個指令會刪除所有以該筆記本名稱開頭的 cassette 檔案。
