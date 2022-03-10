from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import Grid
from mesa.time import RandomActivation
from datetime import datetime
from os import sep

from .agent import TreeCell, TiposMadeira
from scipy.ndimage import measurements

class ForestFire(Model):
    """
    Simple Forest Fire model.
    """

    def __init__(self, width=100, height=100, density=0.65, log_strength=0.4, fire_power=0.4):
        """
        Create a new forest fire model.

        Args:
            width, height: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = Grid(width, height, torus=False)

        self.density = density
        self.log_strength = log_strength
        self.fire_power = fire_power


        self.datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),

                "Clusters": lambda m: self.get_cluster_numbers(m),

                "Abies_lasiocarpa": lambda m: self.tree_type(m, TiposMadeira.Abies_lasiocarpa),
                "Tsuga_heterophylla": lambda m: self.tree_type(m, TiposMadeira.Tsuga_heterophylla),
                "Tsuga_mertensiana": lambda m: self.tree_type(m, TiposMadeira.Tsuga_mertensiana),
                "Picea_engelmannii": lambda m: self.tree_type(m, TiposMadeira.Picea_engelmannii),
                "Thuja_plicata": lambda m: self.tree_type(m, TiposMadeira.Thuja_plicata),
                "Pinus_monticola": lambda m: self.tree_type(m, TiposMadeira.Pinus_monticola),
                "Pinus_contorta": lambda m: self.tree_type(m, TiposMadeira.Pinus_contorta),
                "Abies_grandis": lambda m: self.tree_type(m, TiposMadeira.Abies_grandis),
                "Pseudotsuga_menziesii": lambda m: self.tree_type(m, TiposMadeira.Pseudotsuga_menziesii),
                "Pinus_ponderosa": lambda m: self.tree_type(m, TiposMadeira.Pinus_ponderosa),
                "Larix_occidentalis": lambda m: self.tree_type(m, TiposMadeira.Larix_occidentalis)
            }
        )
        self.model_datacollector = DataCollector(
            {
                "Fine": lambda m: self.count_type(m, "Fine"),
                "On Fire": lambda m: self.count_type(m, "On Fire"),
                "Burned Out": lambda m: self.count_type(m, "Burned Out"),
                "Clusters": lambda m: self.get_cluster_numbers(m)
            }
        )

        self.agent_datacollector = DataCollector(
            {
                "Abies_lasiocarpa": lambda m: self.tree_type(m, TiposMadeira.Abies_lasiocarpa),
                "Tsuga_heterophylla": lambda m: self.tree_type(m, TiposMadeira.Tsuga_heterophylla),
                "Tsuga_mertensiana": lambda m: self.tree_type(m, TiposMadeira.Tsuga_mertensiana),
                "Picea_engelmannii": lambda m: self.tree_type(m, TiposMadeira.Picea_engelmannii),
                "Thuja_plicata": lambda m: self.tree_type(m, TiposMadeira.Thuja_plicata),
                "Pinus_monticola": lambda m: self.tree_type(m, TiposMadeira.Pinus_monticola),
                "Pinus_contorta": lambda m: self.tree_type(m, TiposMadeira.Pinus_contorta),
                "Abies_grandis": lambda m: self.tree_type(m, TiposMadeira.Abies_grandis),
                "Pseudotsuga_menziesii": lambda m: self.tree_type(m, TiposMadeira.Pseudotsuga_menziesii),
                "Pinus_ponderosa": lambda m: self.tree_type(m, TiposMadeira.Pinus_ponderosa),
                "Larix_occidentalis": lambda m: self.tree_type(m, TiposMadeira.Larix_occidentalis)
            }
        )

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                # Create a tree
                new_tree = TreeCell((x, y), self,  log_strength, fire_power)
                # Set all trees in the first column on fire.
                if x == 0:
                    new_tree.condition = "On Fire"
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        self.agent_datacollector.collect(self)
        self.model_datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "On Fire") == 0:
            self.running = False
            now = str(datetime.now()).replace(":", "-")

            model_table = self.model_datacollector.get_model_vars_dataframe()
            model_table.to_csv("spreadsheets"+ sep + "model_data dens=" + str(self.density) + " log=" + str(self.log_strength) + " fire=" + str(self.fire_power) +" " + now + ".csv")
            
            agent_table = self.agent_datacollector.get_model_vars_dataframe()
            agent_table.to_csv("spreadsheets"+ sep + "agent_data dens=" + str(self.density) + " log=" + str(self.log_strength) + " fire=" + str(self.fire_power) +" " + now + ".csv")

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count

    @staticmethod
    def tree_type(model, tree_type):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.tree_type == tree_type:
                count += 1

        return count

    @staticmethod
    def get_cluster_numbers(m):
        grid_aux = []
        for x in range(0,100):
            row = []
            for y in range(0,100):
                celula = m.grid[x,y]
                if celula and celula.condition == "Fine":
                    row.append(1)
                else:
                    row.append(0)
            grid_aux.append(row)

        _, num = measurements.label(grid_aux)
        return num

