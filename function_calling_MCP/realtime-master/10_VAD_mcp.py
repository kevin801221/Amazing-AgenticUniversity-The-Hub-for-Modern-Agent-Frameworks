from audio_util import CHANNELS 
from audio_util import SAMPLE_RATE
from audio_util import AudioPlayerAsync
from openai import AsyncOpenAI
from getchar import getkeys
from tool_utils import show_tools_info
from mcp_utils import load_mcp_servers
from mcp_utils import unload_mcp_servers
from mcp_utils import call_tools
import base64
import asyncio
from dotenv import load_dotenv

load_dotenv(override=True)

connection = None
audio_player = AudioPlayerAsync()
should_send_audio = asyncio.Event()
connected = asyncio.Event()
tools = None

async def handle_realtime_connection():
    global connection

    client = AsyncOpenAI()

    async with client.beta.realtime.connect(
        model="gpt-4o-realtime-preview",
    ) as conn:
        
        connection = conn

        await connection.session.update(
            session={
                "instructions": "使用繁體中文",
                'tools': tools,
                "voice": "shimmer",
                'input_audio_transcription': {
                    'model': 'gpt-4o-transcribe',
                }
            }
        )

        try:
            async for event in conn:
                print(event.type)
                if event.type == "session.created":
                    connected.set()
                # 回應內容的語音也是一段一段送來
                elif event.type == "response.audio.delta":
                    bytes_data = base64.b64decode(event.delta)
                    audio_player.add_data(bytes_data)
                # 如果使用者有講新的話，就停止播放音訊，避免干擾
                elif (event.type == 
                      "input_audio_buffer.speech_started"):
                    audio_player.stop()
                # 當回應內容的文字送完了，就印出來
                elif (event.type == 
                      "response.audio_transcript.done"):
                    print(event.transcript)
                elif (event.type == 
                      "conversation.item."
                      "input_audio_transcription.completed"):
                    print('> ' + event.transcript)
                elif event.type == "response.done":
                    msgs = await call_tools(
                        event.response.output
                    )
                    if msgs == []: continue
                    show_tools_info(event.response)
                    for msg in msgs:
                        await (
                            connection.conversation.item.create(
                            item=msg
                        ))
                    await connection.response.create()             

        except asyncio.CancelledError:
            pass

async def send_mic_audio():
    global connection
    import sounddevice as sd  # type: ignore

    read_size = int(SAMPLE_RATE * 0.02)

    stream = sd.InputStream(
        channels=CHANNELS,
        samplerate=SAMPLE_RATE,
        dtype="int16",
    )
    stream.start()

    try:
        while True:
            # 先累積基本的音訊資料
            if stream.read_available < read_size:
                await asyncio.sleep(0)
                continue

            # 等待按下 r 鍵才開始傳送音訊資料
            await should_send_audio.wait()

            data, _ = stream.read(read_size)

            # 傳送音訊資料給伺服端，伺服端會自動判斷段落就回應
            await connection.input_audio_buffer.append(
                audio=base64.b64encode(data).decode("utf-8")
            )
            await asyncio.sleep(0)
    except KeyboardInterrupt:
        pass
    except asyncio.CancelledError:
        pass
    finally:
        stream.stop()
        stream.close()


async def main():
    global tools
    tools = await load_mcp_servers()
    mic_task = asyncio.create_task(send_mic_audio())
    realtime_task = asyncio.create_task(
        handle_realtime_connection()
    )

    await connected.wait()

    is_recording = False
    while True:
        keys = getkeys()
        if len(keys) == 0:            
            await asyncio.sleep(0.1)
            continue
        key = keys.pop().lower()
        if key == "r":
            is_recording = not is_recording
            if is_recording:
                print("開始錄音")
                should_send_audio.set()
            else:
                print("停止錄音")
                should_send_audio.clear()
        elif key == "q":
            print("結束程式")
            break

    mic_task.cancel()
    realtime_task.cancel()
    await asyncio.gather(mic_task, realtime_task)
    await unload_mcp_servers()

if __name__ == "__main__":
    asyncio.run(main())
