from board import Board
from server import Server
from airplane import Airplane
def main():
    b1=Board()
    a1=Airplane(4,3,0)
    srv=Server()
    b1.add_airplane(a1)
    cs=srv.start_server()
    while True:
        
        s=srv.read_from_client(cs)
        if s is None:
            print("PLAYER_LEFT")
            break
        if len(s) != 3 or s[0] != "SHOT":
            srv.send_to_client(cs, "RESULT INVALID")
            continue
        try:
            x, y = int(s[1]), int(s[2])
        except ValueError:
            srv.send_to_client(cs, "RESULT INVALID")
            continue
        srv.send_to_client(cs,b1.receive_shot(int(s[1]), int(s[2])))
        b1.display()
    cs.close()

if __name__=="__main__":
    main()
