import socket
def read_from_client():
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1",5000))
    s.listen(5)
    cs,addr=s.accept()
    b=cs.recv(10)
    cs.send(b"Hello")
    cs.close()
    return b
