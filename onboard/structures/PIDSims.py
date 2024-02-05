"""
Code to test a vanilla PID controller with fixed parameters.
"""
from Buffer import Buffer
from pid import PID
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from icecream import ic

buffer = Buffer(max_size=100)

iPID = PID(setpoint=0,buffer=buffer,kp=0.1,ki=0.1,kd=0.1) # just picked some rand parameters for init

class TestSystem: # simulation env
    def __init__(self, initial_x=0, gamma=0.1) -> None:
        self.x = initial_x
        self.gamma = gamma # decay factor for PID strength (in practice we can remove this since strength of PID can be controlled by magnitudes of kp,ki,kd anyway)
        self.timestep = 0
    
    def following_function(self):
        if(self.timestep>50): # will switch after 50 timesteps
            return 1
        else:
            return 0
    
    def adjust(self, u):
        self.x += self.gamma*u
        self.timestep+=1


system = TestSystem(initial_x=0)

"""
for me to note:
(value, smoothvalue, t)
"""

# add 1 data:
print(system.x)
buffer += (system.x, system.x, dt.datetime.now())

# start the PID loop!
timesteps = 1000

following = [] # following function values
x_vals = [] # x values
u_vals = [] # u values

for i in range(timesteps):
    
    x = system.x
    x_vals.append(x)
    y = system.following_function()
    iPID.setpoint = y
    following.append(y)
    u = iPID.update()
    u_vals.append(u)
    system.adjust(u)

    plt.figure(1)
    plt.clf()
    plt.plot(following)
    plt.plot(x_vals)
    plt.title("following function and x vals")
    plt.figure(2)
    plt.clf()
    plt.plot(u_vals)
    plt.title("u values")
    plt.pause(0.05)

plt.show()

    
