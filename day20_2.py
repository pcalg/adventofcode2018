# -*- coding: utf-8 -*-
"""
Solution for adventofcode 2018, day 20 second part.

@author: pcalg
"""

import collections
from pathlib import Path

file_location = Path(r"")



def read_file(file_location, file_name):
    fn = file_location / file_name

    with open(fn) as f:
        content = f.readlines()
    return [c.strip('\n').strip('\t') for c in content]


def save_output(file_name, lines):
    fn = file_location / file_name
    with open(fn, 'w') as f:
        f.write('\n'.join(lines) + '\n')


def get_positions(puzzle_input):
    
    def set_min_max(left_top, right_down, location):
        y, x = location
        
        y_lt, x_lt = left_top
        y_rd, x_rd = right_down
        
        return (min(y_lt, y), min(x_lt, x)), (max(y_rd, y), max(x_rd, x))
    
    deltas = {'W': (0, -1, '|'), 'N': (-1, 0, '-'), 'S': (1, 0, '-'), 'E': (0, 1, '|')}
        
    locations = collections.defaultdict(lambda: '#')
    
                                        
    current_location = (0, 0)
    left_top = current_location
    right_down = current_location

    locations[(0,0)] = '.'
                            
    branch_locations = [current_location]    
            
    for ch in puzzle_input[1:-1]:
        
        # states
        if ch == '(':
            branch_locations.append(current_location)
        
        # reset location to last stored
        elif ch == '|':
            current_location = branch_locations[-1]
        
        # back to the stored location (discard the current one)
        elif ch == ')':
            branch_locations.pop()
        
        else:
            # now move
            y, x = current_location
            dy, dx, door = deltas[ch]
            
            locations[y+dy, x+dx] = door
            locations[y+dy+dy, x+dx+dx] = '.'
            current_location = y + dy + dy, x + dx + dx
            
            left_top,right_down = set_min_max(left_top, right_down, current_location)
            
    return locations, left_top, right_down



def draw_grid(positions, left_top, right_down):
    y_min, x_min = left_top
    y_max, x_max = right_down
    
    for y in range(y_min-1, y_max + 2):
        for x in range(x_min-1, x_max + 2):
            if y == 0 and x == 0:
                print("X", end="")
            else:    
                print(positions[y, x], end="")
        print("")


def grid_lines(positions, left_top, right_down):
    y_min, x_min = left_top
    y_max, x_max = right_down
    
    result = list()
    
    for y in range(y_min-1, y_max + 2):
        line = ""
        for x in range(x_min-1, x_max + 2):
            if y == 0 and x == 0:
                line += "X"
            else:
                line += positions[y, x]
        result.append(line)
    return result




def find_max_distance(positions):
    """
    Use BFS to find the shortest distances to all of the rooms
    """
    
    def neighbours(positions, current_location):
        doors = ['-', '|']
        
        y, x = current_location
        
        deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        # rooms are two deltas away
        next_room_pos = [(y+dy+dy, x+dx+dx) for dy, dx in deltas if positions[y+dy, x+dx] in doors]
        
        return next_room_pos
    
        
    start_pos = (0, 0)
    
    q = collections.deque([(start_pos, 0)])
    
    distances = dict()
    
    visited = set([start_pos])
    
    while len(q) > 0:
        cur_location, dist = q.popleft()
        
        distances[cur_location] = dist
    
        neighbour_locations = neighbours(positions, cur_location)
        
        for neighbour in neighbour_locations:
            if neighbour not in visited:
                visited.add(neighbour)
                q.append((neighbour, dist+1))
    
    return distances


def main():
    puzzle_input = read_file(file_location, r'input_day20.txt')[0]
    
    positions, left_top, right_down = get_positions(puzzle_input)
    
    output_lines = grid_lines(positions, left_top, right_down)
    
    distances = find_max_distance(positions)  
    
    print(max(distances.values()))
    
    # find values that have at least 1000 doors
    print(len([val for val in distances.values() if val >= 1000]))

    # save the grid as text file
    save_output('output_day20.txt', output_lines)

if __name__ == "__main__":
    main()
