class Board:
    def __init__(self,size=10):
        self.size=size
        self.grid=[['.' for _ in range(size)]for _ in range(size)]
        self.airplanes=[]
    def in_bounds(self,x,y):
        return 0<= x < self.size and 0<= y < self.size
    def can_place(self, airplane):
        for x, y in airplane.coords["all"]:
            if not self.in_bounds(x, y) or self.grid[y][x] != '.':
                return False
        return True

    def add_airplane(self, airplane):
        if self.can_place(airplane):
            hx,hy=airplane.head
            self.grid[hy][hx]='H'
            for x,y in airplane.coords["body"]:
                self.grid[y][x]='B'
            self.airplanes.append(airplane)
            return True
        return False
    def receive_shot(self, x,y):
        if not self.in_bounds(x,y):
            return "OUT_OF_BOUNDS"
        target=self.grid[y][x]
        if target=='H':
            for plane in self.airplanes:
                if plane.coords["head"]==(x,y):
                    for px,py in plane.coords["body"]:
                        self.grid[py][px]='X'
                    self.grid[y][x]='X'
                    return "PLANE_DESTROYED"
        elif target == 'B':
            self.grid[y][x] = 'X'
            return "BODY_HIT"

        elif target == '.':
            self.grid[y][x] = 'O'
            return "MISS"
        

        return "ALREADY_SHOT"
    def all_destroyed(self):
        return bool(self.airplanes) and all(p.destroyed for p in self.airplanes)
    def display(self, hide_ships=False):
        print("  " + " ".join(str(i) for i in range(self.size)))
        for y, row in enumerate(self.grid):
            display_row = []
            for cell in row:
                if hide_ships and cell in ("H", "B"):
                    display_row.append('.')
                else:
                    display_row.append(cell)
            print(f"{y} " + " ".join(display_row))



