class Airplane:
    def __init__(self,head_x,head_y,orientation):
        self.head=(head_x,head_y)
        self.orientation=orientation
        self.coords=self.calculate_shape()
        self.destroyed=False
    def calculate_shape(self):
        hx,hy=self.head
        coords={}
        if self.orientation==0:
            coords = {
                "head": (hx, hy),
                "body": [
                    (hx - 1, hy + 1), (hx, hy + 1), (hx + 1, hy + 1),
                    (hx, hy + 2),
                    (hx - 1, hy + 3), (hx, hy + 3), (hx + 1, hy + 3)
                ]
            }
        elif self.orientation==1:
            coords={
                "head": (hx, hy),
                "body": [
                    (hx - 1, hy - 1), (hx, hy - 1), (hx + 1, hy - 1),
                    (hx,hy-2),
                    (hx - 1, hy - 3), (hx, hy - 3), (hx + 1, hy - 3)
                ]
            }
        elif self.orientation == 2:
            coords = {
                "head": (hx, hy),
                "body": [
                    (hx-1, hy-1),(hx-1,hy),(hx-1,hy+1),
                    (hx-2,hy),
                    (hx-3,hy-1),(hx-3,hy),(hx-3,hy+1)
                ]
            }
        elif self.orientation == 3:
            coords = {
                "head": (hx, hy),
                "body": [
                    (hx + 1, hy - 1), (hx + 1, hy), (hx + 1, hy + 1),
                    (hx + 2, hy),
                    (hx + 3, hy - 1), (hx + 3, hy), (hx + 3, hy + 1)
                ]
            }
        coords["all"]=[coords["head"]]+coords["body"]
        return coords

