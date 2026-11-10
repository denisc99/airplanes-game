from board import Board
from server import Server
from airplane import Airplane
from GameLogic import GameLogic
import threading

def run_match(srv, cs1, cs2):
    try:
        GameLogic(srv, cs1, cs2).game_loop()
    except (ConnectionError, OSError):
        pass                              
    finally:
        for cs in (cs1, cs2):
            srv.buffers.pop(cs, None)
            try:
                cs.close()
            except OSError:
                pass

def main():
    srv = Server()
    srv.start_server()
    while True:
        cs1 = srv.accept_client()         
        cs2 = srv.accept_client()         
        threading.Thread(target=run_match, args=(srv, cs1, cs2), daemon=True).start()

if __name__ == "__main__":
    main()
