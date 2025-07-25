"""Solara based visualization for Mesa models.

.. note::
    SolaraViz is experimental and still in active development in Mesa 3.x. While we attempt to minimize them, there might be API breaking changes in minor releases.

"""

from mesa.visualization.mpl_space_drawing import (
    draw_space,
)

from .command_console import CommandConsole
from .components import make_plot_component, make_space_component
from .components.altair_components import make_space_altair
from .solara_viz import JupyterViz, SolaraViz
from .space_renderer import SpaceRenderer
from .user_param import Slider

__all__ = [
    "CommandConsole",
    "JupyterViz",
    "Slider",
    "SolaraViz",
    "SpaceRenderer",
    "draw_space",
    "make_plot_component",
    "make_space_altair",
    "make_space_component",
]
