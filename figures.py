class Figure:

    def get_area(self):
        pass


class Rectangle(Figure):

    def __init__(self, hight, width):
        self.hight = hight
        self.width = width

    def get_area(self):
        return self.hight * self.width


class Square(Rectangle):

    def __init__(self, side):
        self.hight = side
        self.width = side


class Triangle(Figure):

    def __init__(self, side1, side2, side3):
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3

    def get_area(self):
        s = (self.side1 + self.side2 + self.side3) / 2
        return s * (s - self.side1) * (s - self.side2) * (s - self.side3)


class Circle(Figure):

    def __init__(self, radius):
        self.radius = radius
        self.pi = 3.14

    def get_area(self):
        return self.pi * (self.radius**2)


def main():

    rectan = Rectangle(23, 37)
    square = Square(33)
    triang = Triangle(24, 32, 18)
    circle = Circle(48)
    figures = [rectan, square, triang, circle]
    for figure in figures:
        print(figure.get_area())


if __name__ == '__main__':
    main()
