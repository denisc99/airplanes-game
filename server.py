import socket
class Server:
    def __init__(self):
        self.buffers = {}

    def start_server(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(("0.0.0.0", 5000))
        self.s.listen(5)

    def accept_client(self):
        cs, addr = self.s.accept()
        print("client connected from", addr)
        return cs

    def read_from_client(self, cs):
        buf = self.buffers.get(cs, b"")
        while b"\n" not in buf:
            data = cs.recv(100)
            if not data:
                self.buffers.pop(cs, None)
                return None
            buf += data
        line, buf = buf.split(b"\n", 1)
        self.buffers[cs] = buf
        return line.decode().strip().split()

    def send_to_client(self, cs, string):
        cs.sendall((string + "\n").encode())
