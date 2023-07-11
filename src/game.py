from time import sleep
from os import get_terminal_size, system
from random import randint
from colors import *
from sys import stdout
from math import floor

PURPLE_BLOCK = f'{BG_PURPLE}  {RESET}'
RED_BLOCK = f'{BG_RED}  {RESET}'
YELLOW_BLOCK = f'{BG_YELLOW}  {RESET}'
GREEN_BLOCK = f'{BG_GREEN}  {RESET}'
EMPTY = f'  '

size = get_terminal_size()

# Divide the width by 2 to account for the fact that a block is 2 characters wide
width = int(size.columns / 2) 
height = int(size.lines)


def print_at(x, y, value):
    if x >= width or y > height or x < 1 or y < 1:
        return
    print(f"\033[{y};{x * 2}H{value}", end="")

class Bird():
    # The bird looks like this in the terminal
    #   
    #      #
    #     ###
    #

    # The x and y coordinates of the bird are the coordinates of the center block of the bird (O)
    #
    #      #
    #     #O#
    # 
    def __init__(self):
        self._y = None
        self.y = height / 2
        self.delta = 0
        self.gravity = 0.3
        self.x = int(width / 2)

    def jump(self):
        self.delta = -2
    
    def update(self):
        self.delta += self.gravity
        self.y += self.delta
        # If the bird y is 2 it touches the top of the screen with the top block
        self.y = max(2, self.y)
        self.y = min(height, self.y)

    def draw(self):
        as_int = int(self.y)
        if not self._y is None:
            _as_int = int(self._y)
            # Erase previous position
            print_at(self.x, _as_int, EMPTY)
            print_at(self.x - 1, _as_int, EMPTY)
            print_at(self.x + 1, _as_int, EMPTY)
            print_at(self.x, _as_int - 1, EMPTY)

        # Draw new position
        print_at(self.x, as_int, YELLOW_BLOCK)
        print_at(self.x - 1, as_int, YELLOW_BLOCK)
        print_at(self.x + 1, as_int, RED_BLOCK)
        print_at(self.x, as_int - 1, YELLOW_BLOCK)

        self._y = self.y


class PipePair():
    def __init__(self):
        self.x = width + 1
        self._x = None
        self.gap = randint(10, 15)
        self.width = 4
        # From the top of the screen (1)
        self.gap_position = randint(int(height / 2) - 10 - int(self.gap / 2), int(height / 2) + 10 - int(self.gap / 2))

    def draw(self):
        # Erase previous position
        if not self._x is None and self._x != self.x:
            for y in range(1, height):
                for i in range(self.width):
                    if y < self.gap_position or y > self.gap_position + self.gap:
                        print_at(self._x + i, y, EMPTY)
                
        # Draw new position
        for y in range(1, height):
            for i in range(self.width):
                if y < self.gap_position or y > self.gap_position + self.gap:
                    print_at(self.x + i, y, GREEN_BLOCK)

        self._x = self.x


    def update(self, updates):
        if updates % 5 == 0:
            self.x -= 1

    def collides(self, bird):
        if bird.x + 1 >= self.x - 1 and bird.x - 1 <= self.x + self.width:
            if bird.y > self.gap_position + self.gap or bird.y - 1 <= self.gap_position:
                return True
        return False


class Game():
    def __init__(self):
        # Clear terminal
        print("\x1b[1;1H\x1b[2J", end="")

        self.STATES = {
            "MAIN": 0,
            "PLAYING": 1,
            "GAME_OVER": 2
        }
        self.state = self.STATES["MAIN"]
        self.bird = Bird()
        self.pipe_pairs = []
        self.updates = 0
        self.score = 0
        
        
    def draw(self):
        for pipe_pair in self.pipe_pairs:
            pipe_pair.draw()

        self.bird.draw()
        print_at(1, 1, f"{BG_PURPLE} Score: {self.score} {RESET}")
        stdout.flush()
        
        
    
    def update(self):
        self.bird.update()

        # Check if the bird fell to the ground
        if self.bird.y == height:
            self.state = self.STATES["GAME_OVER"]
            return
        
        # Create a new pipe pair if the last one is far enough away
        if (self.updates > 5 and len(self.pipe_pairs) == 0) or (len(self.pipe_pairs) > 0 and self.pipe_pairs[-1].x + self.pipe_pairs[-1].width < width - 10):
            self.pipe_pairs.append(PipePair())

        # Update pipe pairs
        for pipe_pair in self.pipe_pairs:
            pipe_pair.update(self.updates)

            # Remove pipe pairs that are off screen
            if pipe_pair.x + pipe_pair.width < 1:
                self.pipe_pairs.remove(pipe_pair)

            # Check for collisions
            if pipe_pair.collides(self.bird):
                self.state = self.STATES["GAME_OVER"]
    
        self.draw()
        self.updates += 1

        if self.updates % 10 == 0:
            self.score += 1

        if self.state == self.STATES["MAIN"]:
            sleep(1)
            self.state = self.STATES["PLAYING"]        
        
        return
    
