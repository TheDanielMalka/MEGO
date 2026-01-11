class Point2d:

    def __init__(self,x,y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.__x += dx
        self.__y += dy
    def __str__(self):
        return f"Point2d({self.x},{self.y})"


class Point2dd:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.__x += dx
        self.__y += dy

    def __str__(self):
        return f"Point2d({self.x},{self.y})"


class Point3d(Point2d,Point2dd):
    def __init__(self,x,y,z):
        super().__init__((x,y),(x,y))
        self.z = z
    def move(self,dx,dy,dz):
        super().move(dx,dy)
        self.z += dz
    def __str__(self):
        return f"Point3d({self.x}, {self.y}, {self.z})"
