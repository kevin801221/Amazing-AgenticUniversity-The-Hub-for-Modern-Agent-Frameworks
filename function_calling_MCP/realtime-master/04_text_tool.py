from tool_utils import tools
from tool_utils import call_tools
from tool_utils import show_tools_info
from openai import AsyncOpenAI
import asyncio
import dotenv

dotenv.load_dotenv(override=True)

async def main():
    client = AsyncOpenAI()

    async with client.beta.realtime.connect(
        model="gpt-4o-realtime-preview"
    ) as connection:
       
        async for event in connection:
            print(event.type)
            if event.type == 'session.created':
                await connection.session.update(
                    session={
                        'modalities': ['text'],
                        'tools': tools,
                        "tool_choice": "auto"
                    }
                )
            elif event.type == 'session.updated':
                await connection.conversation.item.create(
                    item={
                        "type": "message",
                        "role": "user",
                        "content": [{
                            "type": "input_text", 
                            "text": "十二強棒球賽冠軍是哪一隊？"
                                    "2025 奧斯卡男主角又是誰？"
                        }],
                    }
                )
                await connection.response.create()          
            elif event.type == 'response.text.done':
                print(event.text)
            elif event.type == "response.done":
                msgs = call_tools(event.response.output)
                if msgs == []: continue
                show_tools_info(event.response)
                for msg in msgs:
                    await connection.conversation.item.create(
                        item=msg
                    )
                await connection.response.create()               

try:
    asyncio.run(main())
except KeyboardInterrupt as e:
    print("結束程式")