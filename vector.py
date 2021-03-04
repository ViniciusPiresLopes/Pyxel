class Vec2:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def as_tuple(self):
        return self.x, self.y
    
    def copy(self):
        return Vec2(self.x, self.y)
    
    def __repr__(self):
        return f"Vec2({self.x}, {self.y})"


class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def as_tuple(self):
        return self.x, self.y, self.z
    
    def copy(self):
        return Vec3(self.x, self.y, self.z)
    
    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"


class Vec4:
    def __init__(self, x, y, z, w):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
    
    def as_tuple(self):
        return self.x, self.y, self.z, self.w
    
    def copy(self):
        return Vec4(self.x, self.y, self.z, self.w)
    
    def __repr__(self):
        return f"Vec4({self.x}, {self.y}, {self.z}, {self.w})"
