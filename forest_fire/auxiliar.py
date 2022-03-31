from scipy.ndimage import measurements

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

def tree_type(model, tree_type):
    """
    Helper method to count trees in a given condition in a given model.
    """
    count = 0
    for tree in model.schedule.agents:
        if tree.tree_type == tree_type:
            count += 1

    return count