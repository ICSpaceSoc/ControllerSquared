# Onboard

This subproject is what will be run on a _Pi_-Variant on the engine FCU itself. Broadly, this means that `Onboard` will continuously:
- **Retrieve sensor input** from pressure transducers, thermometers, and valve actuation states, then store them in buffers after applying smoothing algorithms.
- **Act on sensor input** by running **Dynamic DQN Parameterised PID** to achieve preset targets, and then sending valve actuation commands.
- **Relay information** to base by sending all raw and processed data, along with calculation steps, to the [Base](Base.md) computer.

## Basic Facts

| What   | What About It  |
|--------|----------------|
| Python | 3.11.x         |

## Contributing

See [Contributing to Onboard](../Contributing.md)

<seealso>

<!--List any additional resources, such as tutorials or guides, that can help users understand and use the API effectively.-->

</seealso>
