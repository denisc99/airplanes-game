from board import Board
from server import Server
from airplane import Airplane
def main():
    b1=Board()
    a1=Airplane(4,3,0)
    srv=Server()
    b1.add_airplane(a1)
    cs=srv.start_server()
    s=srv.read_from_client(cs)
    
    shot= s.decode()
    parts=shot.split()
    srv.send_to_client(cs,b1.receive_shot(int(parts[1]), int(parts[2])))
    b1.display()
    cs.close()

if __name__=="__main__":
    main()
