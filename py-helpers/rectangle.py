from __future__ import annotations
from dataclasses import dataclass
from typing import Union

if __package__ is None or __package__ == '':  
    from point import Point
else: 
    from .point import Point


@dataclass
class Rectangle:
    anchor: Point
    height: float
    width: float
    top_left: Point
    bottom_left: Point
    top_right: Point
    bottom_right: Point

    def __str__(self) -> str:
        return f"Rectangle{self.to_bbox()}"

    def to_bbox(
        self,
    ) -> Union[int, int, int, int]:
        return (
            self.top_left.x,
            self.top_left.y,
            self.bottom_right.x,
            self.bottom_right.y,
        )

    def get_middle(
        self,
    ) -> Point:
        return Point(
            x=int(self.anchor.x + 0.5 * self.width),
            y=int(self.anchor.y + 0.5 * self.height),
        )

    def copy(
        self,
    ) -> Rectangle:
        return Rectangle.from_anchor(
            anchor=Point(self.anchor.x, self.anchor.y),
            height=self.height,
            width=self.width,
        )

    def inContext(self, context: Rectangle) -> Rectangle:
        return Rectangle.from_anchor(
            anchor=context.anchor + self.anchor, height=self.height, width=self.width
        )

    def getEdgeIfOutside(self, p: Point) -> Point:
        ret: Point = Point(x=p.x, y=p.x)
        if ret.x > self.top_right.x:
            ret.x = self.top_right.x
        elif ret.x < self.top_left.x:
            ret.x = self.top_left.x

        if ret.y > self.bottom_right.y:
            ret.y = self.bottom_right.y
        elif ret.y < self.top_left.y:
            ret.y = self.top_left.y

        return ret
    
    def isInside(self, p: Point) -> bool: 
        if p.x > self.top_right.x: return False
        elif p.x < self.top_left.x: return False

        if p.y > self.bottom_right.y: return False
        elif p.y < self.top_left.y: return False

        return True
    
    def hasCrossSection(self, other: Rectangle) -> bool: 
        if self.isInside(p=other.bottom_left): return True
        if self.isInside(p=other.top_left): return True
        if self.isInside(p=other.top_right): return True
        if self.isInside(p=other.bottom_right): return True

        if other.isInside(p=self.bottom_left): return True
        if other.isInside(p=self.top_left): return True
        if other.isInside(p=self.top_right): return True
        if other.isInside(p=self.bottom_right): return True

        return False
    
    def get_size(self, ) -> float: 
        return 2*(self.top_left + ((-1)*self.bottom_right)).value()

    @classmethod
    def from_points(cls, p1: Point, p2: Point, p3: Point, p4: Point) -> Rectangle:
        # Sorting points to determine corners; simple example assuming rectangular alignment
        points = sorted([p1, p2, p3, p4], key=lambda p: (p.y, p.x))
        top_left = points[0]
        bottom_left = points[1]
        top_right = points[2]
        bottom_right = points[3]
        anchor = top_left
        height = abs(top_left.y - bottom_left.y)
        width = abs(top_left.x - top_right.x)
        return cls(
            anchor, height, width, top_left, bottom_left, top_right, bottom_right
        )

    @classmethod
    def from_anchor(cls, anchor: Point, height: int, width: int) -> Rectangle:
        top_left = anchor
        bottom_left = Point(anchor.x, anchor.y + height)
        top_right = Point(anchor.x + width, anchor.y)
        bottom_right = Point(anchor.x + width, anchor.y + height)
        return cls(
            anchor, height, width, top_left, bottom_left, top_right, bottom_right
        )
    
    @classmethod
    def from_bbox(cls, x_min: int, y_min: int, x_max: int, y_max: int) -> Rectangle: 
        return cls.from_anchor(anchor=Point(x_min, y_min), height=y_max-y_min, width=x_max-x_min)

    