from vector import Vec2, Vec4


class Pixel:
    def __init__(self, pos: Vec2, color: Vec4):
        self.pos = pos.copy()
        self.color = color.copy()
    
    def copy(self):
        return Pixel(self.pos, self.color)
    
    def __repr__(self):
       return f"Pixel({self.pos.__repr__()}, {self.color.__repr__()})"
