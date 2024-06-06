from __future__ import annotations
from dataclasses import dataclass
from math import sqrt


@dataclass
class Point:
    x: float
    y: float

    def __add__(self, other: Point) -> Point:
        return Point(x=self.x + other.x, y=self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(x=self.x - other.x, y=self.y - other.y)

    def __rmul__(self, other):
        return self.__mul__(other=other)

    def __mul__(self, other):
        if isinstance(other, Point):
            return self.x * other.x + self.y * other.y
        else:
            return Point(x=self.x * other, y=self.y * other)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise ValueError("A Point only has two elements")

    def value(
        self,
    ) -> int:
        return sqrt(self.x * self.x + self.y * self.y)


if __name__ == "__main__":
    print(Point(x=1.2, y=2.0)[0])
    print(Point(x=1.2, y=2.0)[1])
