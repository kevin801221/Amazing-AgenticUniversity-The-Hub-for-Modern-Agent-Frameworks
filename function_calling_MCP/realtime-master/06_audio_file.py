from audio_util import audio_to_pcm16_base64
from audio_util import AudioPlayerAsync
from openai import AsyncOpenAI
import asyncio
import base64
import dotenv

dotenv.load_dotenv(override=True)

audio_player: AudioPlayerAsync = AudioPlayerAsync()

audio_file = open("ask.mp3", "rb")
audio = audio_file.read()
audio_file.close()
audio = audio_to_pcm16_base64(audio)

async def main():
    client = AsyncOpenAI()

    async with client.beta.realtime.connect(
        model="gpt-4o-realtime-preview",
    ) as connection:
        async for event in connection:
            print(event.type)
            if event.type == "session.created":
                await connection.session.update(
                    session={
                        'instructions': '使用繁體中文',
                        'voice': 'echo',
                    }
                )
            elif event.type == 'session.updated':
                await connection.conversation.item.create(
                    item={
                        "type": "message",
                        "role": "user",
                        "content": [{
                            "type": "input_audio", 
                            "audio": audio
                        }],
                    }
                )
                await connection.response.create()
            elif event.type == "response.audio.delta":
                bytes_data = base64.b64decode(event.delta)
                audio_player.add_data(bytes_data)
            elif event.type == 'response.audio_transcript.done':
                print(event.transcript)

try:
    asyncio.run(main())
except KeyboardInterrupt as e:
    print("結束程式")