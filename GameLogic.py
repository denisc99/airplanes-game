from board import Board
from server import Server
from airplane import Airplane
NUM_PLANES=1
class GameLogic:
    def __init__(self, srv):
        self.boards={1: Board(), 2: Board()}
        self.srv=srv
        s=self.srv.start_server()
        cs1=self.srv.accept_client(s)
        cs2=self.srv.accept_client(s)
        self.conns={1:cs1, 2:cs2}
    
    def place_planes(self, player):
        cs, board = self.conns[player], self.boards[player]
        placed = 0
        while placed < NUM_PLANES:
            self.srv.send_to_client(cs, f"PLACE_PLANE {placed + 1}")
            parts = self.srv.read_from_client(cs)
            if parts is None:
                return False                       
            if len(parts) != 4 or parts[0] != "PLACE":
                self.srv.send_to_client(cs, "PLACE_FAIL")
                continue
            try:
                x, y, o = int(parts[1]), int(parts[2]), int(parts[3])
            except ValueError:
                self.srv.send_to_client(cs, "PLACE_FAIL")
                continue
            if o in (0, 1, 2, 3) and board.add_airplane(Airplane(x, y, o)):
                placed += 1
                self.srv.send_to_client(cs, "PLACE_OK")
            else:
                self.srv.send_to_client(cs, "PLACE_FAIL")
        return True
    def game_loop():
        self.place_planes(1)
        self.place_planes(2)
        
        
