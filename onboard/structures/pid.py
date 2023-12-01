import numpy as np
import scipy as sp

class PID:

    def __init__(self, setpoint, buffer, kp, ki, kd):        
        """_summary_

        Args:
            setpoint (_type_): _description_
            buffer (_type_): _description_
            kp (_type_): _description_
            ki (_type_): _description_
            kd (_type_): _description_
        """
        self.setpoint = setpoint  
        self.buffer = buffer
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral = 0
        self.most_recent_timestep_cached = 0 # the most recent timstep included in the integral.

    def update(self, current_time) -> float:
        """_summary_

        Args:
            current_time (_type_): _description_

        Returns:
            float: _description_
        """

        y = self.buffer[current_time, "timestamp"] #current value. TODO: adjust this to access the buffer properly
        e = self.setpoint - y
        data = self.buffer[self.most_recent_timestep_cached: current_time, "timestamp"]

        # data = [
        #     (value, smoothvalue, self.most_recent_timestep_cached)
        #     (value, smoothvalue, t)
        #     ...
        #     (value, smoothvalue, current_time)
        # ]

        for i in range(len(data)-1): 
            time_diff = data[i+1][2]-data[i][2]
            value_sum = data[i+1][1]-data[i][1]
            self.integral += time_diff*0.5*value_sum
        

        P = self.kp * e
        I = self.ki *  self.self.integral
        D = self.self.kd * (data[-1][1]-data[-2][1])/(data[-1][2]-data[-2][2])
        # we can always change how this grad is computed (ie: number of points to lookback)
        u = P + I + D
        return u


def test():
    from .buffer import Buffer
    import matplotlib.pyplot as plt
    import datetime as dt

    buff = Buffer(10)
    for i in range(15):
        buffer += (i, i, 0.1 * i)

    pid = PID(5, buff, 1, 2, 3)
    print(pid.update(dt.datetime.now()))


if __name__ == "__main__":  # only runs when this file is run directly in terminal; if imported to somewhere else this doesn't run
    test()

    