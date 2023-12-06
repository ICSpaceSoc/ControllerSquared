
import torch
import torch.nn as nn
import torch.optim as optim
import environment
import matplotlib.pyplot as plt
from icecream import ic
import numpy as np
import copy

input_size = 2  # takes in (state (len = 1), action (len = 1))
num_classes = 1  # reward is a single

gamma = 0.4 # discount factor for future rewards
timsteps_for_T_update = 10 # the number of epochs until T is updated
sample_size = 30
elipson = 0.7 # probability of exploration
experiences = 100 # number of times to "experience" per epoch
epochs = 500
lr=0.001

"""
Note: DQN only works with a discretised action space. So, we have only 2 action ie:higher, lower. 
TODO: fix thisssss
"""


class ExperienceReplay:

    def __init__(self,Network, elipson) -> None:
        """
        pass in a network class
        """
        self.buffer = [] # buffer is pushed w/ (s,a,r,s') tuples
        self.Network = Network
        self.elipson = elipson

    def experience(self,count):
        self.elipson *= 0.99 # slowly reduce elipson hahahaha 
        for i in range(count):
            
            s1 = env.p
            if np.random.random() < self.elipson: # explore
                action = np.random.randint(0,2)
            else: #exploit
                i1 = self.Network(torch.FloatTensor([env.p,0])).item()
                i2 = self.Network(torch.FloatTensor([env.p,1])).item()
                if(i1>i2):
                    action = 0
                else:
                    action = 1
            reward = env.step(action)
            self.buffer.append((s1, action, reward, env.p))


# Define the architecture of the neural network
Q = nn.Sequential(
    nn.Linear(input_size, 10),  # Input layer (10 inputs, 20 outputs)
    nn.ReLU(),            # Activation function (ReLU)
    nn.Linear(10, 10),  # Hidden layer (20 inputs, 10 outputs)
    nn.ReLU(),            # Activation function (ReLU)
    nn.Linear(10, num_classes)    # Output layer (10 inputs, 3 outputs)
)

Target = copy.deepcopy(Q)

# Define the loss function
criterion = nn.HuberLoss()

# Define the optimizer
optimizer = optim.SGD(Q.parameters(), lr=lr)


env = environment.environment(setpoint = 10)

ex = ExperienceReplay(Q,elipson)
            
"""
Note = Loss is the loss based on:
    - predicted Q, ie: max(Q(...))
    - reward + gamma*target_Q (ie: Q from target network)
"""            

losses_over_dps = []
state_over_dps = []

for epoch in range(epochs):
    ex.experience(experiences)
    state_over_dps.append(env.p)

    data = [ex.buffer[i] for i in np.random.randint(0,len(ex.buffer),sample_size)]
    _i = 0
    for dp in data:
        s1 = dp[0] # current state
        a = dp[1] # action taken
        r = dp[2] # reward
        s2 = dp[3] # next state
        q_predicted = Q(torch.FloatTensor([s1, a]))
        q_nextstate = max(Target(torch.FloatTensor([s2,0])), Target(torch.FloatTensor([s2,1]))) # max. Q for the next state as given by target net
        loss = criterion(torch.FloatTensor(q_predicted),torch.FloatTensor(q_nextstate+r))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if(_i == 0):
            losses_over_dps.append(loss.item())

    if epoch % timsteps_for_T_update == 0: # will equalise
        Target.load_state_dict(Q.state_dict()) # this is the code to equalise weights of model
        ex.buffer = ex.buffer[-100:-1] # keep only 100 dps in buffer now
    
    if epoch % 100: #every 100 epochs update plot
        if(len(losses_over_dps)<100):
            plt.plot(losses_over_dps)
        else:
            plt.clf()
            plt.plot(losses_over_dps[-100:-1])
        plt.pause(0.05)

plt.show()
