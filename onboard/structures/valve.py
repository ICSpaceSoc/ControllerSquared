import asyncio

class Valve:
    """
    Base class for all valves.
    """
    def __init__(self, name):
        self._name = name
        self._active = False
        self._value = 0

    # === Physical ===
    async def setValve(self, value: float) -> bool:
        # TODO: Implement logging
        # Physical magic
        return True