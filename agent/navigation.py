"""
Gugu FarmMind Grid Navigation & Spatial Pathfinding
Coordinates farm hand movement, tile targeting, and action execution.
"""

class NavigationEngine:
    def __init__(self):
        self.current_tile = (0, 0)

    def find_nearest_empty_tile(self, state):
        """Returns target coordinates (x, y) for planting or building"""
        # Grid dimensions based on land tiles
        tiles = state.land_tiles
        grid_width = int(tiles ** 0.5)
        return (self.current_tile[0] % max(1, grid_width), self.current_tile[1] // max(1, grid_width))

    def calculate_travel_cost(self, from_pos, to_pos):
        return abs(from_pos[0] - to_pos[0]) + abs(from_pos[1] - to_pos[1])
