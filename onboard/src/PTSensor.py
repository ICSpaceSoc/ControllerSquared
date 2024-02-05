import asyncio
from collections import deque
from datetime import datetime
import numpy as np
from random import random

from .Constants import BUFFER_SIZE, SAMPLE_RATE
from .Reading import Reading

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

    # === Smoothing ===
    def filter_reading(self, raw: float) -> float:
        """Smoothes raw sensor input based on historical data."""

        # TODO: Implement smoothing algorithm

        # 1. Savitzky-Golay Filter - interpolating polynomials
        # 2. Moving Averages (simple and triangular)
        
        return raw

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
                    self.filter_reading(raw),
                    datetime.now().timestamp()
                )
            )

            await asyncio.sleep(1 / SAMPLE_RATE)
