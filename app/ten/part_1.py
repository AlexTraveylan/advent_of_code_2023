""" Jour 10 part 1 de l'Avent de code 2023."""
from collections import deque
import time
import xlsxwriter
from typing import Dict, Literal, NamedTuple, Optional

from app.template import get_example, get_input, submit, ints

TypeNode = Literal["S", "|", "-", "L", "J", "7", "F", "."]
Coord = NamedTuple("COORD", [("x", int), ("y", int)])


class Node:
    """A node in the map"""

    def __init__(self, coord: Coord, node_type: TypeNode):
        self.coord = coord
        self.node_type = node_type
        self.neighbors = []

    def __repr__(self):
        return f"Node({self.coord}, {self.node_type}), {self.neighbors})"

    def connexion_possibles(self, max_x: int, max_y: int) -> list[Coord] | None:
        """Return the possible connexions of the node"""

        next_coord_x = self.coord.x + 1 if self.coord.x + 1 < max_x else 0
        next_coord_y = self.coord.y + 1 if self.coord.y + 1 < max_y else 0
        previous_coord_x = self.coord.x - 1 if self.coord.x - 1 >= 0 else max_x - 1
        previous_coord_y = self.coord.y - 1 if self.coord.y - 1 >= 0 else max_y - 1

        if self.node_type in "F":
            connexions = [
                Coord(next_coord_x, self.coord.y),
                Coord(self.coord.x, next_coord_y),
            ]

        elif self.node_type in "|":
            connexions = [
                Coord(self.coord.x, next_coord_y),
                Coord(self.coord.x, previous_coord_y),
            ]

        elif self.node_type in "-":
            connexions = [
                Coord(next_coord_x, self.coord.y),
                Coord(previous_coord_x, self.coord.y),
            ]

        elif self.node_type in "L":
            connexions = [
                Coord(next_coord_x, self.coord.y),
                Coord(self.coord.x, previous_coord_y),
            ]

        elif self.node_type in "J":
            connexions = [
                Coord(previous_coord_x, self.coord.y),
                Coord(self.coord.x, previous_coord_y),
            ]

        elif self.node_type in "7":
            connexions = [
                Coord(previous_coord_x, self.coord.y),
                Coord(self.coord.x, next_coord_y),
            ]

        else:
            return None

        return connexions


def parse_to_node(lines: list[str]) -> dict[Coord, Node]:
    """Parse the input to a dict of nodes"""

    nodes_dict = {}

    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == ".":
                continue

            coord = Coord(x, y)
            nodes_dict[coord] = Node(coord, char)

    return nodes_dict


def bfs(start: Node, nodes: dict[Coord, Node]):
    """Function to do BFS of the graph starting from node 'start' and return the node that is the farthest from 'start'"""

    level: Dict[Node, int] = {
        start: 0
    }  # Dictionary to keep track of visited nodes and their levels
    queue = deque([start])  # Create a queue for BFS

    while queue:
        node = queue.popleft()  # Dequeue a node from front of queue

        for neighbor_coord in node.neighbors:
            neighbor = nodes.get(neighbor_coord)
            if neighbor not in level:
                # If node has not been visited before, enqueue the neighbor
                queue.append(neighbor)
                # Set the level of neighbor as level of node + 1
                level[neighbor] = level[node] + 1

    # After BFS, the node with maximum level is the farthest node
    farthest_node = max(level, key=level.get)

    return farthest_node, level[farthest_node]


def print_grid_with_values(level: Dict[Node, int], max_x: int, max_y: int):
    """Print the grid with the values of the nodes"""
    init_grid = [["." for _ in range(max_x)] for _ in range(max_y)]

    for node, value in level.items():
        init_grid[node.coord.y][node.coord.x] = str(value)

    return init_grid


def export_grid_to_excel(grid: list[list[str]], filename: str):
    """Export the grid to an excel file"""

    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    for row_num, row_data in enumerate(grid):
        worksheet.write_row(row_num, 0, row_data)

    workbook.close()


def detect_start_node_type(start_node: Node, nodes: dict[Coord, Node]):
    """Detect the type of the start node"""

    up_node = nodes.get(Coord(start_node.coord.x, start_node.coord.y - 1))
    down_node = nodes.get(Coord(start_node.coord.x, start_node.coord.y + 1))
    left_node = nodes.get(Coord(start_node.coord.x - 1, start_node.coord.y))
    right_node = nodes.get(Coord(start_node.coord.x + 1, start_node.coord.y))

    is_connexion_with_up = (
        up_node.node_type in ["|", "7", "F"] if up_node is not None else False
    )
    is_connexion_with_down = (
        down_node.node_type in ["|", "J", "L"] if down_node is not None else False
    )
    is_connexion_with_left = (
        left_node.node_type in ["-", "F", "L"] if left_node is not None else False
    )
    is_connexion_with_right = (
        right_node.node_type in ["-", "J", "7"] if right_node is not None else False
    )

    if is_connexion_with_up and is_connexion_with_down:
        start_node.node_type = "|"
    elif is_connexion_with_left and is_connexion_with_right:
        start_node.node_type = "-"
    elif is_connexion_with_up and is_connexion_with_right:
        start_node.node_type = "L"
    elif is_connexion_with_up and is_connexion_with_left:
        start_node.node_type = "J"
    elif is_connexion_with_down and is_connexion_with_right:
        start_node.node_type = "F"
    elif is_connexion_with_down and is_connexion_with_left:
        start_node.node_type = "7"
    else:
        raise ValueError("Start node is not a connexion")


def make_connexion(nodes: dict[Coord, Node], max_x: int, max_y: int, start_node: Node):
    """Make the connexions between the nodes"""

    detect_start_node_type(start_node, nodes)

    for node in nodes.values():
        connexions = node.connexion_possibles(max_x, max_y)

        if connexions is None:
            continue

        neighbours_possible = []
        for neighbour_coord in connexions:
            neighbour = nodes.get(neighbour_coord)
            if neighbour is None:
                continue
            neighbour_connexions = neighbour.connexion_possibles(max_x, max_y)

            if node.coord in neighbour_connexions:
                neighbours_possible.append(neighbour_coord)

        node.neighbors = neighbours_possible


if __name__ == "__main__":
    DAY = 10
    PART = 1
    exemple_or_real = int(input("Exemple 1 ou exemple 2 ou exemple 3 ou Réel 5 ? "))

    if exemple_or_real == 1:
        s = get_example(DAY, offset=1).replace("<em>", "").replace("</em>", "").strip()
    elif exemple_or_real == 2:
        s = get_example(DAY, offset=3).strip()
    elif exemple_or_real == 3:
        s = get_example(DAY, offset=4).strip()
    else:
        s = get_input(DAY).strip()

    # Your code here
    begin_time = time.perf_counter()

    max_x = len(s.splitlines()[0])
    max_y = len(s.splitlines())
    nodes = parse_to_node(s.splitlines())

    start_node = next((node for node in nodes.values() if node.node_type == "S"), None)
    make_connexion(nodes, max_x, max_y, start_node)

    farthest_node, ans = bfs(start_node, nodes)
    print(f"node le plus loin : {farthest_node}, distance : {ans}")

    # fin du code
    end_time = time.perf_counter()
    print(f"Temps d'exécution : {end_time - begin_time:.2f} secondes")
    if exemple_or_real == 5:
        submit(DAY, PART, ans)
    else:
        print(ans)
