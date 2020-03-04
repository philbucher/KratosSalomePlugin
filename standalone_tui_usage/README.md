This folder contains scripts and examples for using the functionalities of the plugin standalone, without using the Salome GUI. In Salome terms this is called the **TUI** mode.

Dump Study

### List of examples:
- **WIP** [Cantilever beam](examples/cantilever): modeled with solid elements. This is a simple example demonstrating the basic stnadalone usage for creating a structural model.
- **WIP** [Wind turbine blade](examples/wind_turbine_blade): Advanced structural model of a wind turbine blade discretized with shell elements. Shows how to work with multiple meshes and submeshes.
- **WIP** [Tower](examples/tower): Structural Model of a tower, taken from the [salome website](https://www.salome-platform.org/user-section/tui-examples). More complex structural model.
- **WIP** [Flow around cylinder](examples/flow_cylinder): Flow around a cylinder in 2D. Shows how to do mesh refinements and write multiple mdpa files.
- **WIP** [Flowe over cross with chimera](examples/flow_cross_chimera): Flow over a cross, modelled with overlappig domains using chimera. One domain is the background, the other is the patch containing the cross. The domains are overlapping.
- **WIP** [Mok FSI](examples/mok_fsi): The Mok FSI benachmark as defined in the dissertation of [Daniel Mok, chapter 7.3](http://dx.doi.org/10.18419/opus-147). This includes two domains, fluid and structure.
- **WIP** [Balls against barrier](examples/balls_barrier): Balls modeled with discrete elements interact with a rigid wall
- **WIP** [Rock falling into cablenet](examples/rock_cablenet): Demonstrating the usage of using discrete elements together with finite elements