import numpy as np
import time
def create_training_data(num_dps, input_size, output_size):
    """
    this is used to make testing data
    """
    inputL = []
    outputL = []
    for i in range(num_dps):
        output = np.random.choice([i for i in range(output_size)])
        outputs = np.zeros(3)
        outputs[output] = 1
        inputs = list(np.random.normal(output, 1, input_size))
        inputL.append(inputs)
        outputL.append(outputs)
    return inputL,outputL

class environment:
    '''
    Has the following specs:
    - inputs an action variable (float)
    - has a variable p (float)
    - for every action taken:
        p += np.rand.norm(action)*0.01
        why? IDFK! just random choice
    - state = p
    - reward = -abs(p-setpoint)
    '''
    def __init__(self, setpoint) -> None:
        self.setpoint = setpoint
        self.p = np.random.random()*10
        self._start = time.perf_counter()
        self.steps = 1
    
    def step(self, action) -> float:
        """
        action [0,1) returns reward (float)
        """

        if(action > 0.5):
            a = 1
        else:
            a = -1
        
        self.p += np.random.normal(a)*0.01
        self.steps+=1
        
        return -abs(self.p-self.setpoint) # returns (s,r) pair
