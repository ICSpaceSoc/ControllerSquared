import numpy as np
from icecream import ic


def timestamp_range_search(l, low: float, high: float) -> list:
    """return a sublist with timestamps within a given range"""
    highindex = len(l)-1
    lowindex = 0
    for i in range(highindex,-1,-1):
        end = True
        if(l[i][2] >= high):
            highindex = i
        if(l[i][2] >= low):
            lowindex = i
            end = False
        if end:
            break
    return l[lowindex:highindex]

class PID:

    def __init__(self, setpoint: float, buffer, kp: float, ki: float, kd: float):        
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
        self.most_recent_index_cached = 0.0 # the most recent timstep included in the integral.

    def update(self) -> float:
        """_summary_

        Args:
            current_time (dt.datetime): the time as of caling the function

        Returns:
            float: _description_
        """
        y = self.buffer[-1][1] #current value. TODO: adjust this to access the buffer properly. also, make sure that the correct timstep is accessed (ie: it exists)
        current_time = self.buffer[-1][2]
        e = self.setpoint - y
        data = timestamp_range_search(self.buffer, self.most_recent_index_cached, current_time)

        # data = [
        #     (value, smoothvalue, self.most_recent_index_cached)
        #     (value, smoothvalue, t)
        #     ...
        #     (value, smoothvalue, current_time)
        # ]

        for i in range(len(data)-1): 
            time_diff = (data[i+1][2]-data[i][2])
            
            value_sum = data[i+1][1]-data[i][1]
            self.integral += time_diff*0.5*value_sum
    
        P = self.kp * e
        I = self.ki *  self.integral
        D = self.kd * (data[-1][1]-data[-2][1])/(data[-1][2]-data[-2][2])
        # we can always change how this grad is computed (ie: number of points to lookback)

        self.most_recent_index_cached = current_time;

        u = P + I + D

        return u


def test():
    import datetime as dt
    import matplotlib.pyplot as plt
    import time
    
    BUFF_MAX = 10

    buff = []
    for i in range(BUFF_MAX):
        time.sleep(0.01)
        buff.append( (i, i, dt.datetime.timestamp(dt.datetime.now())))

    pid = PID(5, buff, 1, 2, 3)
    for i in range(10):
        for j in range(10):
            time.sleep(0.01)
            buff.append( (j, j, dt.datetime.timestamp(dt.datetime.now())))
        ic(pid.update())


if __name__ == "__main__":  # only runs when this file is run directly in terminal; if imported to somewhere else this doesn't run
    test()

    