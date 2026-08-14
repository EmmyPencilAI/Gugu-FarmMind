"""
Grid Navigation, Pathfinding, Farmhand Worker Routing and Distance Optimization.
"""

from typing import Tuple, List, Dict
import math

class NavigationEngine:
    def __init__(self, grid_size: int = 10):
        self.grid_size: int = grid_size

    def manhattan_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Calculates Manhattan grid distance between two coordinates."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def find_nearest_tile(self, origin: Tuple[int, int], candidates: List[Tuple[int, int]]) -> Tuple[Tuple[int, int], int]:
        """Finds closest coordinate among candidates from an origin point."""
        if not candidates:
            return origin, 0
            
        best_pos = candidates[0]
        min_dist = self.manhattan_distance(origin, best_pos)
        
        for pos in candidates[1:]:
            dist = self.manhattan_distance(origin, pos)
            if dist < min_dist:
                min_dist = dist
                best_pos = pos
                
        return best_pos, min_dist

    def optimize_farmhand_tasks(
        self,
        farmhand_positions: List[Tuple[int, int]],
        task_locations: List[Tuple[int, int]]
    ) -> List[Dict[str, Any]]:
        """Greedily assigns tasks to farmhands to minimize total travel time."""
        assignments = []
        unassigned_tasks = list(task_locations)
        
        for idx, worker_pos in enumerate(farmhand_positions):
            if not unassigned_tasks:
                break
            target, dist = self.find_nearest_tile(worker_pos, unassigned_tasks)
            assignments.append({
                "worker_id": idx,
                "origin": worker_pos,
                "target": target,
                "distance": dist
            })
            unassigned_tasks.remove(target)
            
        return assignments
