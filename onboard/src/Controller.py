"""
Controller class for the onboard computer.

This class is responsible for the main loop of the onboard computer.
"""

import asyncio

from .PTSensor import PTSensor
from .VenturiPair import VenturiPair

class Controller:
    """
    Singleton class for controller.
    """

    _instance = None

    def __new__(cls):
        # It turns out that singletons in __init__.py are not recommended...?
        if cls._instance is None:
            cls._instance = super(Controller, cls).__new__(cls)
            cls._instance.__init__()
        return cls._instance

    PT1 = PTSensor('PT1')
    PT2 = PTSensor('PT2')
    VT1 = VenturiPair('VT1', PT1, 0.0001, PT2, 0.0002, 1000)

    def __init__(self):
        self._active = False

    def toggle(self, state: bool):
        """Toggles the controller on or off.

        Args:
            state (bool): `True` to turn the controller on, `False` to turn it off.
        """
        loop = asyncio.get_running_loop()

        self._active = state
        loop.create_task(self.loop())

        # Toggle Sensors
        self.PT1.toggle(state)
        self.PT2.toggle(state)
        self.VT1.toggle(state)

    async def loop(self):
        """
        Main loop for the Controller. Will execute until `self._active` is set to
        `False`, and repeats every `self._sample_rate` seconds.
        """
        while self._active:
            await asyncio.sleep(2)
            # Do controller stuff here
