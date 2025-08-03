from openai import OpenAI
from flask import Flask
from flask import render_template
import time
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI()

def get_ephemeral_key():
    # 生成臨時金鑰
    response = client.beta.realtime.sessions.create(
        model='gpt-4o-realtime-preview'
    )
    # 把時效時間顯示在瀏覽器的終端機上
    print(
        f'Expires at: '
        f'{time.ctime(response.client_secret.expires_at)}'
    )
    # 傳回臨時金鑰
    return response.client_secret.value

app = Flask(__name__)

# 設定靜態檔案的路徑
@app.route('/')
def index():
    return render_template('index.html')

# 取得臨時金鑰的路徑
@app.route('/key')
def key():
    return get_ephemeral_key()

if __name__ == '__main__':
    app.run("0.0.0.0", 5000)
