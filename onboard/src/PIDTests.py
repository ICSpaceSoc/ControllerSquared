"""
Code to test a vanilla PID controller with fixed parameters.
"""

from collections import deque
from icecream import ic
from Reading import Reading
from PID import PID
import matplotlib.pyplot as plt
from datetime import datetime as dt

buffer = deque(maxlen=100000)

iPID = PID(setpoint=0,buffer=buffer,kp=0.1,ki=0.1,kd=0.1) # just picked some rand parameters for init

time_at_start = dt.now().timestamp() # just 

class TestSystem: # simulation env
    def __init__(self, initial_x=0, gamma=0.1) -> None:
        self.x = initial_x
        self.gamma = gamma # decay factor for PID strength (in practice we can remove this since strength of PID can be controlled by magnitudes of kp,ki,kd anyway)

    def following_function(self): # switches to one at time 5
        return int(dt.now().timestamp()>(time_at_start+5))

    def adjust(self, u): # this should be edited to update self.x based on u (control variable)
        self.x += self.gamma*u


system = TestSystem(initial_x=0)

# add 1 data:
print(system.x)
for i in range(100):
    buffer.append(Reading("test", None, system.x, dt.now().timestamp()))

# start the PID loop!
timesteps = 1000

following = [] # following function values
x_vals = [] # x values
u_vals = [] # u values

for i in range(timesteps):
    buffer.append(Reading("test", None, system.x, dt.now().timestamp()))
    x = system.x
    x_vals.append(x)
    y = system.following_function()
    iPID.setpoint = y
    following.append(y)
    u = iPID.update()
    u_vals.append(u)
    system.adjust(u)

    plt.clf()
    plt.plot(following)
    plt.plot(x_vals)
    plt.title("following function and x vals")
    plt.legend(["following","x"])
    plt.pause(0.05)


plt.show()
