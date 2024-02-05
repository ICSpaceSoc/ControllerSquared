from copy import deepcopy
from hmac import new
import numpy as np
from icecream import ic
from pyparsing import deque
from datetime import datetime as dt
from itertools import pairwise

from Reading import Reading

def dequefilter(deck, condition):
    deck = deepcopy(deck)
    for _ in range(len(deck)):
        item = deck.popleft()
        if condition(item):
            deck.append(item)
    return deck

def timestamp_range_search(l: deque, low: float, high: float) -> list:
    """return a sublist with timestamps within a given range"""
    return dequefilter(l, lambda x: low <= x.timestamp <= high)

class PID:

    def __init__(self, setpoint: float, buffer: deque, kp: float, ki: float, kd: float):        
        """_summary_

        Args:
            setpoint (_type_): _description_
            buffer (_type_): _description_
            kp (_type_): _description_
            ki (_type_): _description_
            kd (_type_): _description_
        """
        self.setpoint = setpoint # setpoint can be changed by reassigning the variable directly
        self.buffer = buffer
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self._lastTime = 0.0 # the most recent timestamp included in the integral.

    def calcProportional(self):
        return self.kp * (self.setpoint - self.buffer[-1].filt)
    
    def calcIntegral(self, newTime):
        # TODO: Use new [Buffer] class to implement this
        data = timestamp_range_search(self.buffer, self._lastTime, newTime)

        for pair in pairwise(data): 
            timeDiff = (pair[1].timestamp - pair[0].timestamp)
            valSum = pair[1].filt - pair[0].filt
            self.integral += timeDiff * 0.5 * valSum

        I = self.ki * self.integral

    def calcDerivative(self):
        # TODO: calculate better derivative
        return self.kd * (self.buffer[-1].filt-self.buffer[-2].filt)/(self.buffer[-1].timestamp-self.buffer[-2].timestamp)

    def update(self) -> float:
        """Returns a new control value based on the current setpoint and system state."""

        newTime = self.buffer[-1].timestamp
        U = self.calcProportional() + self.calcIntegral(newTime) + self.calcDerivative()
        self._lastTime = newTime

        return U

def test():    
    BUFF_MAX = 10

    buff = deque()
    for i in range(BUFF_MAX):
        buff.append(Reading("test", None, i, dt.now().timestamp()))

    pid = PID(5, buff, 1, 2, 3)
    for i in range(10):
        for j in range(10):
            buff.append(Reading("test", None, j, dt.now().timestamp()))
        ic(pid.update())

if __name__ == "__main__":
    test()
