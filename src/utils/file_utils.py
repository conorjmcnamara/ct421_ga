from typing import List, Tuple


def load_tsplib(path: str) -> List[Tuple[float, float]]:
    """
    Loads the coordinates of cities from a TSPLIB file.

    Args:
        path: The path to the TSPLIB file.

    Returns:
        A list of tuples representing the coordinates (x, y) of each city.
    """
    with open(path, 'r') as file:
        lines = file.readlines()
        node_coord_section = False
        coords = []

        for line in lines:
            if "NODE_COORD_SECTION" in line:
                node_coord_section = True
                continue
            if "EOF" in line:
                break
            if node_coord_section:
                parts = line.strip().split()
                coords.append((float(parts[1]), float(parts[2])))
        return coords
