import mesa
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from .scf import SB110Model

# Class for agent design on grid
def agent_portrayal(agent):
    portrayal = {
        "Shape": "circle",
        "Filled": "true",
        "Layer": 0,
        "Color": "red",
        "r": 0.5,
        "text": agent.unique_id,
    }
    return portrayal

model_params = {
    "gc_threshold": UserSettableParameter(
        "slider",
        "General Contractor payment success threshold",
        0.5,  # default
        0,  # min
        1,  # max
        0.05,  # step
        description="Choose the GC's success",
    ),
    "tech_threshold": UserSettableParameter(
        "slider",
        "Technician asseveration success threshold",
        0.5,  # default
        0,  # min
        1,  # max
        0.05,  # step
        description="Choose the Tech's success",
    ),
    "open_amount": UserSettableParameter(
        "slider",
        "Settlement percentage of Open state",
        0.1,  # default
        0,  # min
        1,  # max
        0.05,  # step
        description="Choose the Open percentage",
    ),
    "ant_amount": UserSettableParameter(
        "slider",
        "Settlement percentage of Anticipation state",
        0.1,  # default
        0,  # min
        1,  # max
        0.05,  # step
        description="Choose the Anticipation percentage",
    ),
    "sal1_amount": UserSettableParameter(
        "slider",
        "Settlement percentage of Sal1 state",
        0.2,  # default
        0,  # min
        1,  # max
        0.05,  # step
        description="Choose the Sal1 percentage",
    ),
    "sal2_amount": UserSettableParameter(
        "slider",
        "Settlement percentage of Sal2 state",
        0.2,  # default
        0,  # min
        1,  # max
        0.05,  # step
        description="Choose the Sal2 percentage",
    ),
    "eow_amount": UserSettableParameter(
        "slider",
        "Settlement percentage of EoW state",
        0.4,  # default
        0,  # min
        1,  # max
        0.05,  # step
        description="Choose the Eow percentage",
    ),
    "tech_amount": UserSettableParameter(
        "slider",
        "Percentage to be paid for technical asseveration",
        0.20,  # default
        0,  # min
        0.25,  # max
        0.05,  # step
        description="Choose the Technician asseveration percentage",
    ),
}

grid = CanvasGrid(agent_portrayal, 15, 6, 500, 500)
chart = ChartModule(
    [{"Label": "GC_Wealth", "Color": "Black"}, {"Label": "Wealth", "Color": "Red"}],
    data_collector_name="datacollector",
)
server = mesa.visualization.ModularServer(
    SB110Model, [grid, chart], "SuperBonus 110 Model", model_params
)  # "N":10, "width":10, "height":10

server.port = 8521  # The default port
