#test
from .classes import *


def play_game():
    home = Team("England", "4231")
    away = Team("United States", "433") 
    home.gen_random_team()
    away.gen_random_team()
    for i in range(1):
        game = Game(home, away)
        game.play_game()
        return game