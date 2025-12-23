import asyncio

from src.presentation.console_demo.demo import start_demo

async def main() -> None:
    print("Starting...")
    await start_demo()



if __name__ == '__main__':
    asyncio.run(main())