#!/usr/bin/env python3

import pynput
from os import system
from time import sleep
from game import *
import cursor
from sys import argv

# Prevent user input from being displayed on the terminal
def hide_stdin():
    system("stty -echo")
    cursor.hide()

# Allow user input to be displayed on the terminal
def show_stdin():
    system("stty echo")
    cursor.show()

VERSION = "0.1.0"
MIN_HEIGHT = 40

def main():
    ignore_height = False

    argv.pop(0)
    while len(argv) > 0:
        arg = argv.pop(0)
        match arg:
            case "-h" | "--help":
                bar = f"{PURPLE}━━━━━━━━━━━━━━━━━{RESET}"
                print()
                print(f"{BG_PURPLE} Flappy {RESET}")
                print(bar)
                print(f"Author: {PURPLE}SkwalExe <Leopold Koprivnik>{RESET}")
                print(f"Github: {PURPLE}https://github.com/SkwalExe{RESET}")
                print(bar)
                print(f"A simple flappy bird game written in Python.")
                print(bar)
                print(f"Options:")
                print(f"\t{PURPLE}-h, --help : {YELLOW}Show this help message and exit")
                print(f"\t{PURPLE}-v, --version : {YELLOW}Show the version number and exit")
                print(f"\t{PURPLE}-c, --cursor : {YELLOW}If you left the game with Ctrl+C (you should use ESC instead), this option will show make the cursor visible again and exit")
                print(f"\t{PURPLE}-I, --ignore-height : {YELLOW}Ignore terminal height warning")
                print(bar)
                print(f"Controls:")
                print(f"\t{PURPLE}Esc : {YELLOW}Quit the game")
                print(f"\t{PURPLE}Space : {YELLOW}Make the bird jump")
                print(f"\t{PURPLE}Enter : {YELLOW}Pause/resume the game")
                print(bar)
                print(f"Additional information:")
                print(f"\t{PURPLE}If you want to keep your cursor and stdin visible after the game, exit with ESC instead of Ctrl+C (also, see -c option){RESET}")
                print(f"\t{PURPLE}If you encounter any bugs, please report them on the Github repository or at koprivnik@skwal.net{RESET}")
                print()
                
                quit(0)

            case "-v" | "--version":
                print(f"{BG_PURPLE} Flappy {RESET}")
                print(f"Version: {PURPLE}{VERSION}{RESET}")
                quit(0)
            case "-c" | "--cursor":
                show_stdin()
                quit(0)
            case "-I" | "--ignore-height":
                ignore_height = True
            case _:
                print(f"{RED}Error: {YELLOW}Unknown argument : {PURPLE}{arg}{RESET}")
                quit(1)

    if height < MIN_HEIGHT and not ignore_height:
        print(f"{RED}Error: {YELLOW}It is recommended to play in a terminal with a height of at least {PURPLE}{MIN_HEIGHT}{YELLOW} characters, use -I to ignore this warning.{RESET}")
        quit(1)

    hide_stdin()
    paused = False
    game = Game()
    def on_press(key):
        if key == pynput.keyboard.Key.space:
            game.bird.jump()
        elif key == pynput.keyboard.Key.esc:
            game.state = game.STATES["GAME_OVER"]
        elif key == pynput.keyboard.Key.enter:
            nonlocal paused
            paused = not paused
            print_at(int(width / 2) - 1, int(height / 2), f"{BG_RED} Paused {RESET}" if paused else "        ")
            stdout.flush()
        

    with pynput.keyboard.Listener(on_press=on_press) as listener:
        while not game.state == game.STATES["GAME_OVER"]:
            if not paused:
                game.update()
            sleep(0.05)
        print_at(1, height, "\nGame Over!\n")
        print(f"{BG_PURPLE} Score: {game.score} {RESET}")
        print()
        show_stdin()

if __name__ == "__main__":
    main()