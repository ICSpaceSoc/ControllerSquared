# ICSS Kepler Flow Control Software

This repository hosts all software related to the ICSS (Imperial College Space Society) Kepler Engine Fuel Flow Control System. The main components are
- `onboard`: Python-based software intended for a PI-variant on the engine itself, which autonomously controls the fuel flow based on various sensor input (e.g., pressure, temperature). It has a built-in failsafe, but also connects to
- `failsafe`: An analogue custom-PCB which automatically shuts off all flow if a keep-alive signal from `onboard` dies.
- `base`: A simple GUI for monitoring and controlling the engine remotely, along with various data analytic tools.

During development, each of the components have their own directory, and are treated independently. When in doubt, such as when dealing with relative directories, treat each component as a separate project.

## Onboard

TODO: Docs

## Todo list

- Central algorithm
    - Throw around ideas for the algo [*] [all ]
    - Ensure input/output to algo works properly
- Valve control
    - Test if module can receieve commands from Algorithm 
- Comms
    - (not much to be done here yet)
- Sensor input and preprocessing
    - Send spoof input via GPIO ports, ensure can be read
    - 
- Custom PCB
    - Design analog killswitch [*]
- Hardware
    - Research and buy valves and sensors [*]
    - Compile datasheet info (ie: sensor output format) into readable format for future ref.
    - Start designing sensor + valve modules once we settle on sensor + valve specs
- Server-side
    - Set up comms framework (https?) [*]
    - GUI
        - Throw around GUI design ideas [*]
    - Database
        - Test database works
- Others
    - Design data format/systems needed [*]
      - Do this now 
(tasks with a * are ones that can be tackled immediately)

## For next meeting
- Check current todo list
- Assign tasks
