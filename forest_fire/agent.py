from mesa import Agent
from random import randint, choices

from enum import Enum

class TiposMadeira(Enum):
    Burned = 0
    Abies_lasiocarpa = 1
    Tsuga_heterophylla = 2
    Tsuga_mertensiana = 3
    Picea_engelmannii = 4
    Thuja_plicata = 5
    Pinus_monticola = 6
    Pinus_contorta = 7
    Abies_grandis = 8
    Pseudotsuga_menziesii = 9
    Pinus_ponderosa = 10
    Larix_occidentalis = 11


class TreeCell(Agent):
    """
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "On Fire", or "Burned Out"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """

    def __init__(self, pos, model, log_strength, fire_power):
        """
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"
        self.tree_type = choices(list(TiposMadeira), weights=(0, 3, 5, 8, 11, 14, 
                                                              18, 14, 11, 8, 5, 3), k=1)[0]
        self.log_strength = log_strength * self.tree_type.value
        self.fire_power = self.set_fire_power(fire_power)

    def set_fire_power(self, x):
        return (randint(x, x + int(x/10)) if self.tree_type.value <= 5 else (randint(x - int(x/10), x)))


    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """

        if self.condition == "On Fire" and self.fire_power > self.log_strength:
            for neighbor in self.model.grid.neighbor_iter(self.pos):
                if neighbor.condition == "Fine":
                    neighbor.condition = "On Fire"
            self.condition = "Burned Out"
            self.tree_type = TiposMadeira.Burned
        elif self.condition == "On Fire" and self.fire_power <= self.log_strength:
            self.condition = "Burned Out"
            self.tree_type = TiposMadeira.Burned
