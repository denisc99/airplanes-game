from board import Board
from server import Server
from airplane import Airplane
from GameLogic import GameLogic
def main():
  srv=Server()
  game=GameLogic(srv)
  ok1 = game.place_planes(1)
  print("player 1 placed:", ok1)
  ok2 = game.place_planes(2)
  print("player 2 placed:", ok2)
  game.boards[1].display()
  game.boards[2].display()
  

if __name__=="__main__":
    main()
