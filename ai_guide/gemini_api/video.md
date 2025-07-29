# Veo 3 影片生成教學

## 概述

Veo 3 是 Google 最先進的影片生成模型，能夠從文字提示生成高保真度的 8 秒 720p 影片，具有驚人的真實感和原生生成的音訊。Veo 3 在各種視覺和電影風格方面都表現出色。

## 基本影片生成

### 文字轉影片範例

以下是一個生成包含對話的影片範例：

```python
import time
from google import genai
from google.genai import types

client = genai.Client()

prompt = """A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.
A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"""

operation = client.models.generate_videos(
    model="veo-3.0-generate-preview",
    prompt=prompt,
)

# 輪詢操作狀態直到影片準備就緒
while not operation.done:
    print("正在等待影片生成完成...")
    time.sleep(10)
    operation = client.operations.get(operation)

# 下載生成的影片
generated_video = operation.response.generated_videos[0]
client.files.download(file=generated_video.video)
generated_video.video.save("dialogue_example.mp4")
print("生成的影片已儲存至 dialogue_example.mp4")
```

## 從圖片生成影片

### 圖片轉影片流程

以下程式碼展示了使用 Imagen 生成圖片，然後將該圖片作為影片的起始畫面：

> **注意**：Veo 3 的圖片轉影片功能即將推出！在此之前您可以使用 Veo 2（無音訊）。

```python
import time
from google import genai

client = genai.Client()

prompt = "Panning wide shot of a calico kitten sleeping in the sunshine"

# 步驟 1：使用 Imagen 生成圖片
imagen = client.models.generate_images(
    model="imagen-3.0-generate-002",
    prompt=prompt,
)

# 步驟 2：使用 Veo 2 和圖片生成影片
operation = client.models.generate_videos(
    model="veo-2.0-generate-001",
    prompt=prompt,
    image=imagen.generated_images[0].image,
)

# 輪詢操作狀態直到影片準備就緒
while not operation.done:
    print("正在等待影片生成完成...")
    time.sleep(10)
    operation = client.operations.get(operation)

# 下載影片
video = operation.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("veo2_with_image_input.mp4")
print("生成的影片已儲存至 veo2_with_image_input.mp4")
```

## 影片生成參數與規格

### 可用參數

| 參數 | 描述 | Veo 3 (預覽版) | Veo 2 (穩定版) |
|------|------|---------------|----------------|
| `prompt` | 影片的文字描述，支援音訊提示 | string | string |
| `negativePrompt` | 描述在影片中要避免的內容 | string | string |
| `image` | 要進行動畫化的初始圖片 | 不支援 | Image 物件 |
| `aspectRatio` | 影片的長寬比 | "16:9" | "16:9", "9:16" |
| `personGeneration` | 控制人物生成 | "allow_all" | "allow_all", "allow_adult", "dont_allow" |

### 使用參數自訂影片

您可以透過在請求中設定參數來自訂影片生成。例如，指定 `negativePrompt` 來引導模型：

```python
import time
from google import genai
from google.genai import types

client = genai.Client()

operation = client.models.generate_videos(
    model="veo-3.0-generate-preview",
    prompt="A cinematic shot of a majestic lion in the savannah.",
    config=types.GenerateVideosConfig(negative_prompt="cartoon, drawing, low quality"),
)

# 輪詢操作狀態直到影片準備就緒
while not operation.done:
    print("正在等待影片生成完成...")
    time.sleep(10)
    operation = client.operations.get(operation)

# 下載生成的影片
generated_video = operation.response.generated_videos[0]
client.files.download(file=generated_video.video)
generated_video.video.save("parameters_example.mp4")
print("生成的影片已儲存至 parameters_example.mp4")
```

## 處理非同步操作

影片生成是一項計算密集型任務。當您發送請求時，API 會啟動一個長時間執行的作業並立即回傳一個操作物件。然後您必須輪詢直到影片準備就緒，這由 `done` 狀態為 `true` 來表示。

```python
import time
from google import genai
from google.genai import types

client = genai.Client()

# 啟動作業後，您會得到一個操作物件
operation = client.models.generate_videos(
    model="veo-3.0-generate-preview",
    prompt="A cinematic shot of a majestic lion in the savannah.",
)

# 或者，您可以使用 operation.name 來取得操作
operation = types.GenerateVideosOperation(name=operation.name)

# 此迴圈每 10 秒檢查一次作業狀態
while not operation.done:
    time.sleep(10)
    # 重新整理操作物件以取得最新狀態
    operation = client.operations.get(operation)

# 完成後，結果在 operation.response 中
# ... 處理和下載您的影片 ...
```

## 模型功能比較

| 功能 | 描述 | Veo 3 (預覽版) | Veo 2 (穩定版) |
|------|------|---------------|----------------|
| **音訊** | 原生生成音訊與影片 | ✔️ 始終開啟 | ❌ 僅靜音 |
| **輸入模式** | 用於生成的輸入類型 | 文字轉影片 | 文字轉影片、圖片轉影片 |
| **解析度** | 影片的輸出解析度 | 720p | 720p |
| **幀率** | 影片的輸出幀率 | 24fps | 24fps |
| **影片長度** | 生成影片的長度 | 8 秒 | 5-8 秒 |
| **每次請求影片數** | 每次請求生成的影片數量 | 1 | 1 或 2 |
| **狀態與詳情** | 模型可用性和詳細資訊 | 預覽版 | 穩定版 |

## Veo 提示指南

### 音訊提示（Veo 3）

使用 Veo 3，您可以提供音效、環境噪音和對話的提示。模型會捕捉這些提示的細微差別來生成同步的配樂。

**音訊提示類型**：
- **對話**：使用引號表示特定語音（例如：`"This must be the key," he murmured.`）
- **音效 (SFX)**：明確描述聲音（例如：`tires screeching loudly, engine roaring`）
- **環境噪音**：描述環境的聲音景觀（例如：`A faint, eerie hum resonates in the background`）

### 提示寫作基礎

好的提示是描述性的且清楚的。要充分利用 Veo，請從確定您的核心想法開始，透過添加關鍵字和修飾詞來精煉您的想法，並將影片特定術語納入您的提示中。

**提示中應包含的元素**：

1. **主體**：您希望在影片中出現的物件、人物、動物或景色
2. **動作**：主體正在做什麼（例如：走路、跑步或轉頭）
3. **風格**：使用特定的電影風格關鍵字指定創意方向
4. **攝影機位置和動作**：[可選] 控制攝影機的位置和移動
5. **構圖**：[可選] 鏡頭如何取景
6. **焦點和鏡頭效果**：[可選] 實現特定視覺效果
7. **氛圍**：[可選] 顏色和光線如何貢獻於場景

### 提示寫作技巧

- **使用描述性語言**：使用形容詞和副詞為 Veo 描繪清晰的畫面
- **增強面部細節**：將面部細節指定為照片的焦點，如在提示中使用「肖像」一詞

## 範例提示與輸出

### 基本元素範例

**主體和背景**：
```
一棟白色混凝土公寓大樓的建築渲染圖，具有流暢的有機形狀，與茂盛的綠色植物和未來主義元素無縫融合
```

**動作**：
```
一個女人在海灘上行走的廣角鏡頭，在日落時分望向地平線，看起來滿足和放鬆
```

**風格**：
```
黑色電影風格，男人和女人在街上行走，神秘，電影般，黑白
```

**攝影機運動和構圖**：
```
從一輛老式汽車在雨中行駛的 POV 鏡頭，加拿大夜晚，電影般
```

**氛圍**：
```
一個女孩在公園裡抱著可愛的金毛獵犬小狗的特寫，陽光
```

### 負面提示

負面提示指定您不希望在影片中出現的元素。

**正確做法**：
- ✅ 描述您不想看到的內容（例如：`wall, frame`）
- ❌ 不要使用指示性語言如「no」或「don't」（例如：`No walls`）

## 長寬比

Veo 允許您指定影片的長寬比：

- **寬螢幕 (16:9)**：適合橫向影片
- **直向 (9:16)**：僅 Veo 2 支援，適合手機觀看

## 限制與注意事項

### 技術限制
- **請求延遲**：最少 11 秒；最多 6 分鐘（尖峰時段）
- **影片保留**：生成的影片在伺服器上保存 2 天，之後會被移除
- **每次請求影片數**：Veo 3 為 1 個，Veo 2 為 1-2 個

### 地區限制
- `personGeneration: "allow_all"`（Veo 3 中的預設值）和圖片轉影片的人物生成（Veo 2）在歐盟、英國、瑞士、中東和北非地區不被允許

### 安全與品質
- **浮水印**：Veo 創建的影片使用 SynthID 進行浮水印標記
- **安全過濾**：生成的影片會通過安全過濾器和記憶檢查程序
- **內容政策**：違反條款和指導原則的提示會被阻止

## 最佳實踐總結

1. **詳細描述**：提供清晰、描述性的提示
2. **音訊整合**：利用 Veo 3 的音訊生成功能
3. **參數調整**：使用負面提示和其他參數精確控制輸出
4. **輪詢管理**：正確處理非同步操作
5. **及時下載**：在 2 天內下載生成的影片

---

*本教學基於 Veo 3 官方文檔整理，適合影片創作者和開發者參考使用。*