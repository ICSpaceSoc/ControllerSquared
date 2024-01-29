import asyncio
from collections import deque
from datetime import datetime
import numpy as np

from .Constants import BUFFER_SIZE, SAMPLE_RATE
from .Reading import Reading

class VenturiPair:
    """
    [VenturiPair] is a virtual sensor that determines the volumetric flow rate of a fluid based
    on the pressure (and cross-sectional) differential of two pressure transducers.
    """

    def __init__(self, name, sensorSmall, areaSmall, sensorBig, areaBig, density):
        self._name = name
        self._sensorSmall = sensorSmall
        self._sensorBig = sensorBig
        self._const = areaSmall * np.sqrt(2 / (density * (np.power(areaSmall / areaBig, 2) - 1)))

        self.buffer = deque(maxlen=BUFFER_SIZE)

    # === Main Loop ===
    def toggle(self, state: bool):
        self._active = state

        if state:
            loop = asyncio.get_running_loop()
            loop.create_task(self.loop())

    async def loop(self):
        while self._active:
            small = self._sensorSmall.buffer[-1]
            big = self._sensorBig.buffer[-1]
            vol_flow_rate = self._const * np.sqrt(small.filt - big.filt)

            self.buffer.append(
                Reading(
                    self._name,
                    None,
                    vol_flow_rate,
                    datetime.now().timestamp()
                )
            )

            await asyncio.sleep(SAMPLE_RATE)
