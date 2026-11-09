from board import Board
from server import read_from_client
from airplane import Airplane
def main():
    b1=Board()
    a1=Airplane(4,3,0)
    b1.add_airplane(a1)
    s=read_from_client()
    shot= s.decode()
    parts=shot.split()
    b1.receive_shot(int(parts[1]), int(parts[2]))
    b1.display()

if __name__=="__main__":
    main()
