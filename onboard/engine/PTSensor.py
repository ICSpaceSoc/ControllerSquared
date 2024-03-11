import asyncio
from collections import deque
from datetime import datetime
import numpy as np
from random import random

from util.Constants import BUFFER_SIZE, SAMPLE_RATE
from data.Reading import Reading

class PTSensor:
    """
    A pressure transducer sensor.
    """
    def __init__(self, name):
        self._name = name
        self._active = False

        self.buffer = deque(maxlen=BUFFER_SIZE)

    # === Physical ===
    async def read_sensor(self) -> float:
        """Reads sensor input from physical GPIO pins."""

        # TODO: Implement GPIO reading
        return np.sin(datetime.now().timestamp()) + 0.2 * random()

    # === Main Loop ===
    def toggle(self, state: bool):
        self._active = state

        if state:
            loop = asyncio.get_running_loop()
            loop.create_task(self.loop())

    async def loop(self):
        while self._active:
            raw = await self.read_sensor()

            self.buffer.append(
                Reading(
                    self._name,
                    raw,
                    datetime.now().timestamp()
                )
            )

            await asyncio.sleep(1 / SAMPLE_RATE)
