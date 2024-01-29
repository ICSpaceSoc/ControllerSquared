import asyncio

from src import Controller

async def main():
    cont = Controller()
    cont.toggle(True)

    while True:
        await asyncio.sleep(1)
        print(f"It is: datetime.now().timestamp()")
        print(f"PT1 {cont.PT1.buffer[0]}")
        print(f"PT2 {cont.PT2.buffer[0]}")
        print(f"VT1 {cont.VT1.buffer[0]}")

if __name__ == "__main__":
    eventLoop = asyncio.new_event_loop()
    eventLoop.create_task(main())
    eventLoop.run_forever()
