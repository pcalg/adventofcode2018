# -*- coding: utf-8 -*-
"""
Solution for adventofcode 2018 day 22 second part.

This solution uses A* to find the answer.

@author: pcalg
"""

import collections
import heapq
from timeit import default_timer as timer

# set up the lookup tables
regions = {0: 'rocky', 1: 'wet', 2: 'narrow'}

tools = {0: 'neither', 1: 'climbing gear', 2: 'torch'}


region_tools = {0: {1, 2},
                1: {0, 1},
                2: {0, 2}
                }
  
class Game:
    
    def __init__(self, positions, target_y, target_x):
        self.positions = positions
        self.target_y = target_y
        self.target_x = target_x
        self.target = ((target_y, target_x), 2)


    def distance_heuristic(self, player) -> int:
        """
        Calculate the Manhattan distance on a square grid
        """
        pos, _ = player
        y, x = pos
        
        return abs(x - self.target_x) + abs(y - self.target_y)

    
    def get_movement_region(self, current_player):
        """
        Get all the possible regions to move to, with the new time as well
        So we have to either move (1 minute) or change tool and stay put (7 minutes)
        """

        def get_neighbours(pos):
            """
            Select all the neighbours of the player. Negative x and y values are not allowed.
            """ 
            
            deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            
            cur_y, cur_x = pos
            
            neighbours = [(cur_y + dy, cur_x + dx) for dy, dx in deltas if cur_y + dy >= 0 and cur_x + dx >= 0]
    
            return neighbours


        tools_lookup = {(0, 1): 2, (0, 2): 1,
                        (1, 0): 1, (1, 1): 0,
                        (2, 0): 2, (2, 2): 0}

        
        pos, tool = current_player
        
        positions = self.positions
        
        # First, see if we can change our tool for a cost of 7
        yield 7, (pos, tools_lookup[(positions[pos], tool)])
        
        
        # Now check neighbours without changing the tool
        neighbours = get_neighbours(pos)
    
        for neighbour in neighbours:            
            # Only move is the tool the player has now on him is allowed on the neighbouring position
            if tool in region_tools[positions[neighbour]]:
                yield 1, (neighbour, tool)
    
    
    def find_target(self):
        """
        Find the target using A* algorithm using a priority queue (heapq)
        """                
        frontier = list()
        
        # add the first player
        start_player = ((0, 0), 2) # 2 = torch

        heapq.heappush(frontier, (0, start_player))
        
        cost_so_far = dict()        
        cost_so_far[start_player] = 0
            
        while len(frontier) > 0:
            _, current_player = heapq.heappop(frontier)
            
            pos, tool = current_player
            
            if self.positions[pos] < 0:
                raise Exception('At a border')
            
            if current_player == self.target:
                print("found")
                print("time spent: {0} player: {1}".format(cost_so_far[current_player], current_player))
                return cost_so_far[current_player]
    
            time_spent = cost_so_far[current_player]
            
            moves = self.get_movement_region(current_player)
            
            for movement_time, moved_player in moves:

                # check if we need to investigate this node.
                next_time_spent = time_spent + movement_time
                                
                if moved_player not in cost_so_far or next_time_spent < cost_so_far[moved_player]:
                    cost_so_far[moved_player] = next_time_spent
                                        
                    # a* algorithm
                    priority = next_time_spent + self.distance_heuristic(moved_player)
                    # priority equals here next_time_spent
                    heapq.heappush(frontier, (priority, moved_player))
    
        print("exiting: no solution")
        return 0


def geologic_index(depth, target, padding=1):
    
    geo_index = collections.defaultdict(int)
    erosion_level = collections.defaultdict(lambda: -1)
    result = collections.defaultdict(lambda: -1)
    
    max_x, max_y = target
    
    for y in range(max_y+padding):
        for x in range(max_x+padding):
            if x == 0 and y == 0:
                geo_index[(y, x)] = 0
            elif x == max_x and y == max_y:
                geo_index[(y, x)] = 0
            elif y == 0:
                geo_index[(y, x)] = x * 16807
            elif x == 0:
                geo_index[(y, x)] = y * 48271
            else:
                geo_index[(y, x)] = erosion_level[(y-1, x)] * erosion_level[(y, x-1)]
            erosion_level[(y, x)] = (geo_index[(y, x)] + depth) % 20183
            result[(y, x)] = erosion_level[(y, x)] % 3
    return result


def print_grid(g_erosion, target, padding=1, max_size=1000):
    
    max_x, max_y = target
    
    cave_type = {0:'.', 1:'=', 2: '|'}
    
    
    for y in range(min(max_y + padding, max_size)):
        for x in range(min(max_x + padding, max_size)):
            if y == 0 and x == 0:
                print("M", end="")
            elif y == max_y and x == max_x:
                print("T", end="")
            else:
                print(cave_type[g_erosion[(y, x)]], end="")
        print("")



def main():    
    # puzzle input
    depth = 5913
    target = 8, 701
    
    target_x, target_y = target
    
    g_erosion = geologic_index(depth, target, 130)
    
    start = timer()
    
    game = Game(g_erosion, target_y, target_x)
    
    target = game.find_target()
    
    end = timer()
    
    print(f"The answer is: {target}")
    # answer should be: 973
    
    print(end-start)

if __name__ == "__main__":
    main()