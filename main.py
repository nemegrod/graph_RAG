import asyncio
from dotenv import load_dotenv
from lib.agent_low import run_agent

load_dotenv()

async def main():

    result = await run_agent("should i buy a new car?")
    print(result)
if __name__ == "__main__":
    asyncio.run(main())