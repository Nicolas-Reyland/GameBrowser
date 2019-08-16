# Game Browser - main
from GameBrowser import GameBrowser
from Game import load_games
import os

LOCAL_GAME_PATH = 'games'

if __name__ == '__main__':
	games = load_games(os.path.join(os.getcwd(), LOCAL_GAME_PATH))
	gamebrowser = GameBrowser(games, LOCAL_GAME_PATH)
	gamebrowser.mainloop()
