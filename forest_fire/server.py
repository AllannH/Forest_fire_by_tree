from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import ForestFire

COLORS = {"Fine": "#00AA00", "On Fire": "#880000", "Burned Out": "#000000"}

TREES = {
    "Abies_lasiocarpa": "#01ff00",
    "Tsuga_heterophylla": "#01c33c",
    "Tsuga_mertensiana": "#007a85",
    "Picea_engelmannii": "#0053ac",
    "Thuja_plicata": "#0031ce",
    "Pinus_monticola": "#0000ff",
    "Pinus_contorta": "#2600d9",
    "Abies_grandis": "#4c00b3",
    "Pseudotsuga_menziesii": "#8f0071",
    "Pinus_ponderosa": "#c5003b",
    "Larix_occidentalis": "#ff0001"
    }

CLUSTER = {"Clusters": "#00AA00"}

def forest_fire_portrayal(tree):
    if tree is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = tree.pos
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[tree.condition]
    return portrayal


canvas_element = CanvasGrid(forest_fire_portrayal, 100, 100, 500, 500)
forest_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
forest_pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)
tree_pie_chart = PieChartModule(
    [{"Label": label, "Color": color} for (label, color) in TREES.items()]
)
cluster_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in CLUSTER.items()]
)

model_params = {
    "height": 100,
    "width": 100,
    "density": UserSettableParameter("slider", "Tree density", 0.65, 0.01, 1.0, 0.01),
    "log_strength": UserSettableParameter("slider", "Log strength", 3.0, 1.0, 10.0, 1.0),
    "fire_power": UserSettableParameter("slider", "Fire power", 40.0, 1.0, 100.0, 1.0)
}
server = ModularServer(
    ForestFire, [canvas_element, forest_chart, forest_pie_chart, tree_pie_chart, cluster_chart], "Forest Fire", model_params
)
