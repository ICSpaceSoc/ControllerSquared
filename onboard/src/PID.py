"""
A generica [PID] controller class. This class is designed to reach a setpoint using PID control
when only given a data buffer of past data. It does not change its PID coefficients.

To use, initialise with [name], [setpoint], [dataBuffer], and four coefficients [kp], [ki], [kd],
and [k] which is the gain of the controller. Then, call [U] to get the control signal.

When [U] is called, all data in the buffer that is between the last time [U] was called and the 
current time is processed to give the new result.
"""

from dataclasses import dataclass
from pyparsing import deque
from itertools import pairwise

from Reading import Reading
from Constants import BUFFER_SIZE
from Helpers import stamp

@dataclass
class PID:
    name: str
    setpoint: float
    dataBuffer: deque[Reading]

    k: float
    kp: float
    ki: float
    kd: float

    def __post_init__(self):
        self._buffer: deque[Reading] = deque(maxlen = BUFFER_SIZE)
        self._currTime: float = 0.0
        self._lastTime: float = 0.0

    @property
    def error(self) -> float:
        return self.setpoint - self.dataBuffer[-1].filt

    @property
    def P(self) -> float:
        return self.kp * self.error
    
    @property
    def I(self) -> float:
        data = list(filter(
            lambda x: self._lastTime <= x.timestamp <= self._currTime,
            self.dataBuffer
        ))

        integral = 0
        for (prev, curr) in pairwise(data): 
            timeDiff = (curr.timestamp - prev.timestamp)
            valSum = curr.filt - prev.filt
            integral += timeDiff * 0.5 * valSum

        return self.ki * integral

    @property
    def D(self) -> float:
        # TODO: calculate better derivative
        return self.kd * (self.dataBuffer[-1].filt-self.dataBuffer[-2].filt)/(self.dataBuffer[-1].timestamp-self.dataBuffer[-2].timestamp)

    def U(self) -> float:
        # [U] is not marked as [@property] since it updates the internal buffer.
        self._currTime, self._lastTime = self.dataBuffer[-1].timestamp, self._currTime
        U = self.k * (self.P + self.I + self.D)

        self._buffer.append(Reading(self.name, None, U, self._currTime))
        return U

## Visual Debug ##
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import numpy as np

    buffer = deque(maxlen = BUFFER_SIZE)
    buffer.append(Reading("PIDExpt", None, 0, stamp()))

    iPID = PID("PIDExpt", setpoint = 0, dataBuffer = buffer, k = 1, kp = 0.8, ki = 0.1, kd = 0)
    realStart = stamp()

    # Selection of Target Functions
    stepFunc = lambda t: int((t - realStart) > 2)
    sineFunc = lambda t: 10 * (1 + np.sin(2 * np.pi * t))

    target, x = 0, 0
    pltTarget = []
    pltX = []

    while True:
        buffer.append(Reading("PIDExpt", None, x, stamp()))

        pltX.append(x)
        target = sineFunc(stamp())
        pltTarget.append(target)
        iPID.setpoint = target

        U = iPID.U()
        x += U

        plt.clf()
        plt.plot(pltTarget, label = "Target")
        plt.plot(pltX, label = "Real")
        plt.title("[PIDTest] Target and Real")
        plt.pause(0.05)
