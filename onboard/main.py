import asyncio

from structures import Controller

async def main():
    cont = Controller()
    cont.toggle(True)

    while True:
        await asyncio.sleep(1)
        print(f"PT1 {cont.PT1.buffer[-1]}")
        print(f"PT2 {cont.PT2.buffer[-1]}")

    await asyncio.sleep(1)
    await cont.toggle(False)

if __name__ == "__main__":
    eventLoop = asyncio.new_event_loop()
    eventLoop.create_task(main())
    eventLoop.run_forever()
    