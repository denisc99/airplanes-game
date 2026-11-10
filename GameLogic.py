from board import Board
from server import Server
from airplane import Airplane
NUM_PLANES=1
class GameLogic:
    def __init__(self, srv,cs1,cs2):
        self.boards={1: Board(), 2: Board()}
        self.srv=srv
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
    def parse_shot(self, parts):
        if len(parts) != 3 or parts[0] != "SHOT":
            return None
        try:
            return int(parts[1]), int(parts[2])
        except ValueError:
            return None
    def send_boards(self):
        for p in (1, 2):
            e = 2 if p == 1 else 1
            cs = self.conns[p]
            self.srv.send_to_client(cs, "BOARD OWN " + self.boards[p].to_string())
            self.srv.send_to_client(cs, "BOARD ENEMY " + self.boards[e].to_string(hide_ships=True))
    def game_loop(self):
        if not (self.place_planes(1) and self.place_planes(2)):
            return
        current = 1
        self.send_boards()
        while True:
            enemy = 2 if current == 1 else 1
            cs, ecs = self.conns[current], self.conns[enemy]
            self.srv.send_to_client(cs, "YOUR_TURN")
            self.srv.send_to_client(ecs, "OPP_TURN")

            while True:                                   
                parts = self.srv.read_from_client(cs)
                if parts is None:                         
                    self.srv.send_to_client(ecs, "GAME_OVER WIN")
                    return
                shot = self.parse_shot(parts)
                if shot is None:
                    self.srv.send_to_client(cs, "RESULT INVALID")
                    self.srv.send_to_client(cs, "YOUR_TURN")
                    continue
                x, y = shot
                result = self.boards[enemy].receive_shot(x, y)
                if result in ("OUT_OF_BOUNDS", "INVALID", "ALREADY_SHOT"):
                    self.srv.send_to_client(cs, f"RESULT {result}")
                    self.srv.send_to_client(cs, "YOUR_TURN")
                    continue
                break       
                
            self.send_boards()
            self.srv.send_to_client(cs, f"RESULT {result}")
            self.srv.send_to_client(ecs, f"OPP_SHOT {x} {y} {result}")
            if result == "PLANE_DESTROYED":
                self.srv.send_to_client(cs, "GAME_OVER WIN")
                self.srv.send_to_client(ecs, "GAME_OVER LOSE")
                return
            current = enemy
        
        
