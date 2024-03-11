import asyncio
from datetime import datetime

from engine.Controller import Controller
from engine.PID import visualDebug

async def main():
    cont = Controller()
    cont.toggle(True)

    while True:
        await asyncio.sleep(1)
        print(f"It is: {datetime.now().timestamp()}")
        print(f"PT1 {cont.PT1.buffer[-1]}")
        print(f"PT2 {cont.PT2.buffer[-1]}")
        print(f"VT1 {cont.VT1.buffer[-1]}")

if __name__ == "__main__":
    # eventLoop = asyncio.new_event_loop()
    # eventLoop.create_task(main())
    # eventLoop.run_forever()

    visualDebug()
    
