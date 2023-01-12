from operator import itemgetter
from typing import List
from collections import namedtuple
import time
import math


class Point(namedtuple("Point", "x y")):
    def __repr__(self) -> str:
        return f'Point{tuple(self)!r}'


class Rectangle(namedtuple("Rectangle", "lower upper")):
    def __repr__(self) -> str:
        return f'Rectangle{tuple(self)!r}'

    def is_contains(self, p: Point) -> bool:
        return self.lower.x <= p.x <= self.upper.x and self.lower.y <= p.y <= self.upper.y


class Node(namedtuple("Node", "location left right")):
    """
    location: Point
    left: Node
    right: Node
    """

    def __repr__(self):
        return f'{tuple(self)!r}'


class KDTree:
    """k-d tree"""

    def __init__(self):
        self._root = None
        self._n = 0

    def insert(self, p: List[Point]):
        """insert a list of points"""
        def _create(list:List[Point]):
            if not list:
                return None
            if self._n == 0:
                cur_h = 0
            else:
                cur_h = math.floor(math.log2(self._n))
            if cur_h % 2 == 0:
                list.sort(key=itemgetter(0))
                mid = len(list) // 2
                self._n = self._n +1
                return Node(location=list[mid],left=_create(list[:mid]),right=_create(list[mid+1:]))
            else:
                list.sort(key=itemgetter(1))
                mid = len(list) // 2
                self._n = self._n +1
                return Node(location=list[mid],left=_create(list[:mid]),right=_create(list[mid+1:]))
        self._root = _create(p)




    def range(self, rectangle: Rectangle) -> List[Point]:
        """range query"""
        list = []
        def _search(rect: Rectangle, n: Node):
            if n is None:
                return
            
            if n.location.x < rect.lower.x and n.location.y < rect.lower.y:
                _search(rect, n.right)
            elif n.location.x > rect.upper.x and n.location.y > rect.upper.y:
                _search(rect, n.left)
            else :
                _search(rect, n.left)
                if rect.is_contains(n.location):
                    list.append(n.location)
                _search(rect, n.right)
        _search(rectangle,self._root)
        return list


                

def range_test():
    points = [Point(7, 2), Point(5, 4), Point(9, 6), Point(4, 7), Point(8, 1), Point(2, 3)]
    kd = KDTree()
    kd.insert(points)
    result = kd.range(Rectangle(Point(0, 0), Point(6, 6)))
    print (result)
    #assert sorted(result) == sorted([Point(2, 3), Point(5, 4)])


def performance_test():
    points = [Point(x, y) for x in range(1000) for y in range(1000)]

    lower = Point(500, 500)
    upper = Point(504, 504)
    rectangle = Rectangle(lower, upper)
    #  naive method
    start = int(round(time.time() * 1000))
    result1 = [p for p in points if rectangle.is_contains(p)]
    end = int(round(time.time() * 1000))
    print(f'Naive method: {end - start}ms')

    kd = KDTree()
    kd.insert(points)
    # k-d tree
    start = int(round(time.time() * 1000))
    result2 = kd.range(rectangle)
    end = int(round(time.time() * 1000))
    print(f'K-D tree: {end - start}ms')

    assert sorted(result1) == sorted(result2)


if __name__ == '__main__':
    range_test()
    performance_test()