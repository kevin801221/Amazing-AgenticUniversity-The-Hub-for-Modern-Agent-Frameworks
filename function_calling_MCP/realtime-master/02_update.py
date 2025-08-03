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
                print(f'指示: {event.session.instructions}')                
                await connection.session.update(
                    session={'instructions': '使用繁體中文',}
                )
            elif event.type == 'session.updated':
                print(f'指示: {event.session.instructions}')

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print("結束程式")