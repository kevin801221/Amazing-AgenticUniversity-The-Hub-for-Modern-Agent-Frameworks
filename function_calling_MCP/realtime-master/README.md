# 旗標科技《OpenAI API 開發手冊》第 8 章 範例

前置工作：

- Realtime API 需要 `openai[realtime]` 套件：

    ```
    uv add openai[realtime]
    ```

- 語音部分需要以下套件：

    ```
    uv add pyaudio
    uv add pydub
    uv add sounddevice
    uv add numpy
    ```

    如果使用 Python 3.13 以上版本，因為 ‵autioop‵ 從 3.13 版開始已經被移除了，要額外安裝 [`autioop-lts`](https://github.com/jiaaro/pydub/issues/725#issuecomment-2439291764) 套件補回來：

    ```
    uv add audioop-lts
    ```
- 非同步鍵盤偵測使用的是 `getchar` 套件

    ```
    uv add getchar
    ```

- 最後使用 falsk 架設網頁伺服器

    ```
    uc add flask
    ```
