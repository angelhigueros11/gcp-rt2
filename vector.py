# Angel Higueros
# 20460
# RT2

class V3(object):

    def __init__(self, x, y, z, w = 0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def round(self):
        self.x = round(self.x)
        self.y = round(self.y)
        self.z = round(self.z)

    def __add__(self, other):
        return V3(
            self.x + other.x,
            self.y + other.y,
            self.z + other.z,
        )

    def __sub__(self, other):
        return V3(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )

    def __mul__(self, other):
        if type(other) in [int, float]:
            return V3((other * self.x), (other * self.y), (other * self.z))
        else:
            return V3(
                ((self.y * other.z) - (self.z * other.y)),
                ((self.z * other.x) - (self.x * other.z)),
                ((self.x * other.y) - (self.y * other.x))
            )

    def __matmul__(self, other):
        return ((self.x * other.x) + (self.y * other.y) + (self.z * other.z))

    def __len__(self):
        return (((self.x ** 2) + (self.y ** 2) + (self.z ** 2)) ** 0.5)

    def __repr__(self):
        return f"V3({self.x}, {self.y}, {self.z})"

    def length(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def norm(self):
        try:
            return (self * (1 / self.__len__()))
        except Exception:
            return (self * 0)