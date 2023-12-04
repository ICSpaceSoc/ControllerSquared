import numpy as np

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
        self.most_recent_index_cached = 0 # the most recent timstep included in the integral.

    def update(self, current_time) -> float:
        """_summary_

        Args:
            current_time (_type_): current time in index

        Returns:
            float: _description_
        """

        y = self.buffer[current_time, 'timestamp']['corr_value'] #current value. TODO: adjust this to access the buffer properly
        y = self.buffer[current_time][1] #current value. TODO: adjust this to access the buffer properly
        print(y)
        e = self.setpoint - y
        data = self.buffer[self.most_recent_index_cached: current_time]

        # data = [
        #     (value, smoothvalue, self.most_recent_index_cached)
        #     (value, smoothvalue, t)
        #     ...
        #     (value, smoothvalue, current_time)
        # ]

        for i in range(len(data)-1): 
            time_diff = (data[i+1][2]-data[i][2]).total_seconds()
            
            value_sum = data[i+1][1]-data[i][1]
            self.integral += time_diff*0.5*value_sum
        

        P = self.kp * e
        I = self.ki *  self.integral
        D = self.kd * (data[-1][1]-data[-2][1])/(data[-1][2]-data[-2][2]).total_seconds()
        # we can always change how this grad is computed (ie: number of points to lookback)
        u = P + I + D
        
        return u


def test():
    from Buffer import Buffer
    from Buffer import Buffer
    import datetime as dt
    import matplotlib.pyplot as plt
    import time
    
    BUFF_MAX = 100
    
    
    buff = Buffer(BUFF_MAX, [('value', np.float64), ('corr_value', np.float64), ('timestamp', dt.datetime)])
    for i in range(BUFF_MAX):
        time.sleep(0.1)
        buff += (i, i, dt.datetime.now())
        
        

    pid = PID(5, buff, 1, 2, 3)
    print(pid.update(BUFF_MAX - 1))


if __name__ == "__main__":  # only runs when this file is run directly in terminal; if imported to somewhere else this doesn't run
    test()

    