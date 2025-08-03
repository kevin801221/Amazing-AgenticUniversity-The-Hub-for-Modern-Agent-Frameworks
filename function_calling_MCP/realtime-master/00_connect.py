import asyncio
import openai
import dotenv

dotenv.load_dotenv(override=True)

async def main():
    client = openai.AsyncOpenAI()

    async with client.beta.realtime.connect(
        model='gpt-4o-realtime-preview'
    ) as connection:
        async for event in connection:
            print(event.type)
            if event.type == 'session.created':
                print(f'模型: {event.session.model}')
                print(f'指示: {event.session.instructions}')

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print("結束程式")