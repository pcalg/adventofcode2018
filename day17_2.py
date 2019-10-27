# -*- coding: utf-8 -*-
"""
Solution to adventofcode 2018 day 17 part 2

https://adventofcode.com/2018/day/17

Created on Mon Jan 21 17:28:53 2019

@author: pcalg
"""

import collections
from PIL import Image, ImageColor


# cases:
# |
# .
# -> move down
#
#    |
#   .#. -> check left, check right for walls. if hole found: add to pos list
#
#
#  #..|  #
#  ####### -> fill 
# prev always y-1? no

class Drop:
    def __init__(self):
        pass


class Grid:
    def __init__(self):
                
        self.locations = collections.defaultdict(lambda: ".")
        self.clear()
    
    def __repr__(self):
        return "x range: ({0}, {1}) y range: ({2}, {3}) locations: {4}".\
            format(self.min_x, self.max_x, self.min_y, self.max_y, len(self.locations))
    
    def clear(self):
        self.locations.clear()
        self.min_x = 500
        self.min_y = 0
        self.max_x = 500
        self.max_y = 0

    def show(self):
        for y in range(self.min_y, self.max_y+1):
            for x in range(self.min_x-5, self.max_x+5):
                if (y, x) in self.locations:
                    print(self.locations[(y, x)], end="")
                else:
                    print(".", end="")
            print("")
    
    def show_lines(self):
        for y in range(self.min_y, self.max_y+1):
            line = ""
            
            for x in range(self.min_x-5, self.max_x+5):
                if (y, x) in self.locations:
                    line += self.locations[(y, x)]
                else:
                    line += '.'
            yield line


    def count_water(self):
        cnt = 0
        for y in range(self.min_y, self.max_y+1):
            for x in range(self.min_x-1, self.max_x+1):
                if self.locations[(y, x)] in ['~']:
                    cnt += 1
        return cnt
        
        
    def valid_pos(self, pos):
        y, x = pos
        return y >= self.min_y and y <= self.max_y and x >= (self.min_x -1000) and x <= (self.max_x+1000)
    
    def can_move_vertical(self, dy, pos):
        y, x = pos
        new_pos = y+dy, x
        return self.locations[new_pos] == '.' and self.valid_pos(new_pos)
    
    
    def fixed_pos(self, pos):
        return self.locations[pos] in ['#', '~']
    
    def can_move_horizontal(self, dx, pos):
        y, x = pos
        new_pos = y, x+dx
        
        return self.locations[new_pos] == '.' and self.valid_pos(new_pos) and self.fixed_pos((y+1, x))
 
    def wall_horiz(self, dx, pos):
        y, x = pos
        while self.valid_pos((y, x)):
            y, x = y, x+dx
            if self.locations[(y+1, x)] not in ['#', '~']:
                return None
            
            if self.locations[(y, x)] == "#":
                return y, x
    
    def set_fixed_water(self, pos_left, pos_right):
        y_start, x_start = pos_left
        _, x_end =  pos_right
        
        # no holes and walls on either side
        for x in range(x_start+1, x_end):
            self.locations[(y_start, x)] = '~'
            
    def move(self, pos):
        # down
        if self.can_move_vertical(1, pos):
            y, x = pos
            self.locations[(y+1,x)] = '|'
            return y+1, x
        
        # check fill
        pos_left = self.wall_horiz(-1, pos)
        pos_right = self.wall_horiz(1, pos)
        if pos_left is not None and pos_right is not None:
            self.set_fixed_water(pos_left, pos_right)
            return
        
        # else see if can move left
        if self.can_move_horizontal(-1, pos):
            #print('horiz')
            y, x = pos
            self.locations[(y,x-1)] = '|'
            return y, x-1
    
        # otherwise to the right    
        if self.can_move_horizontal(1, pos):
            y, x = pos
            self.locations[(y,x+1)] = '|'
            return y, x+1

    
    def set_grid(self, lines):
        
        def parse_line(line):
            parts = [line_part.strip().split('=') for line_part in line.split(',')]
            
            lookup=dict()
            
            for part in parts:
                lookup[part[0]] = [int(ch) for ch in part[1].split('..')]
        
            return lookup
                
        self.clear()
    
        # pos of the water source
        self.locations[(0, 500)] = '+'
        
        for line in lines:
            line_info = parse_line(line)
            
            self.min_x = min(self.min_x, line_info['x'][0]) 
            self.max_x = max(self.max_x, line_info['x'][-1])
            
            for x in range(line_info['x'][0], line_info['x'][-1]+1):
                for y in range(line_info['y'][0], line_info['y'][-1]+1):
                    self.min_y = min(self.min_y, line_info['y'][0]) 
                    self.max_y = max(self.max_y, line_info['y'][-1])
                    
                    self.locations[(y, x)] = '#'


class Game():
    def __init__(self, grid):
        self.grid = grid
        self.drop_pos = [(0, 500)]
            
    def move(self):
        # get first pos
        
        if len(self.drop_pos) == 0:
            return False
        
        pos = self.drop_pos.pop()
        
        new_pos = self.grid.move(pos)
        
        if new_pos is not None:
            self.drop_pos.append(pos)
            self.drop_pos.append(new_pos)
        
        return True
        
    def show(self):
        self.grid.show()

def count_water(locations):
    cnt = 0
    for key in locations:
        if locations[key] in ['|', '~']:
            cnt +=1
    return cnt


def read_file(fn):
    with open(fn) as f:
        content = f.readlines()
    return [c.strip('\n').strip('\t') for c in content]


def save_output(fn, lines):
    with open(fn, 'w') as f:
        f.write('\n'.join(lines) + '\n')


def create_img(grid, x_offset):
    """
    visualize grid with an img
    """
    img = Image.new('RGB', (grid.max_x+1-x_offset, grid.max_y+1), color='white')
    pixels = img.load()
    
    for y in range(grid.min_y, grid.max_y+1):
    
        
        for x in range(grid.min_x-5, grid.max_x+1):
            val = grid.locations[(y, x)]
            if val == "#":
                pixels[x-x_offset, y] = ImageColor.getrgb('red')
            if val == '|':
                pixels[x-x_offset, y] = ImageColor.getrgb('aquamarine')
            if val == '~':
                pixels[x-x_offset, y] = ImageColor.getrgb('blue')

    return img


def main():
    
    puzzle_input = read_file(r'input_day17.txt')
    
    grid = Grid()
    grid.set_grid(puzzle_input)
    
    g = Game(grid)
    
    for _ in range(25000):
        res = g.move()
        if not res:
            print("breaking")
            break
        
    print(f"solution: {grid.count_water()}")
    
    save_output(r'output.txt', grid.show_lines())
    
    img = create_img(grid, 250)
    img.show()

if __name__ == "__main__":
    main()
