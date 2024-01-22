# ControllerSquared

`ControllerSquared` is a complete software package designed for the ICSS **Kepler** Liquid-Fuel Rocket Engine. It comprises
- `onboard`: Python-based software intended for a PI-variant on the engine itself, which autonomously controls fuel flow and other parameters during flight (or testing). The software is currently designed to only operate on the FCU (Flow Control Unit).
- `failsafe`: An custom analogue PCB which automatically shuts off all flow if a keep-alive signal from `onboard` dies.
- `base`: A simple web-GUI for monitoring and controlling the engine remotely, along with various data analytic tools.
- `docs`: Where (hopefully) comprehensive documentation is kept about design goals, philosophy, rationale, implementation, and usage.

## Architecture

Development is still in early stages, and various parts of the architecture are expected to change / evolve.

<p align="center">
    <img src="https://github.com/ICSpaceSoc/ControllerSquared/assets/75836446/d8b2c375-1e90-4860-9ec4-ce97091ac4ba">
</p>

## Authors

All authors are students at Imperial College London, and are, alphabetically,

| Who                     | Studies                      |
| ----------------------- | ---------------------------- |
| Chris Cheang            | (2YS) Mechanical Engineering |
| Nishant Kidangan-Mathew | (1YS) Mechanical Engineering |
| Lancelot Liu            | (1YS) Computing              |

TODO: Add remaining authors.
