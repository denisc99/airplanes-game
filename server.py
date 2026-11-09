import socket
class Server:
    def start_server(self):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("127.0.0.1", 5000))
        s.listen(5)
        cs,addr=s.accept()
        return cs
    def read_from_client(self,cs):
        b=cs.recv(10)
        return b
    def send_to_client(self,cs, string):
        cs.sendall((string+"\n").encode())

