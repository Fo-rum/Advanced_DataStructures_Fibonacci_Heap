# explanations for member functions are provided in requirements.py
from __future__ import annotations

import math


class FibNodeLazy:
    def __init__(self, val: int):
        self.val = val
        self.parent = None
        self.children = []
        self.flag = False
        self.vacant = False
        self.degree = 0

    def get_value_in_node(self):
        return self.val

    def get_children(self):
        return self.children

    def get_flag(self):
        return self.flag

    def __eq__(self, other: FibNodeLazy):
        return self.val == other.val


class FibHeapLazy:
    def __init__(self):
        # you may define any additional member variables you need
        self.roots = []
        self.min = FibNodeLazy(math.inf)
        self.n = 0

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNodeLazy:
        new = FibNodeLazy(val)
        self.roots.append(new)

        if new.val < self.min.val:
            self.min = new

        self.n += 1
        return new

    def delete_min_lazy(self) -> None:
        if self.min is not None and self.min.vacant == True:
            self.min = self.find_min_lazy()

        self.min.vacant = True
        self.min.val = -math.inf
        return

    def find_min_lazy(self) -> FibNodeLazy:
        if self.min is not None and self.min.vacant:
            self.roots.remove(self.min)
            self.cut(self.min)
            self.consolidate()

            self.min = self.roots[0]

            for r in range(1, len(self.roots)):
                if self.roots[r].val < self.min.val:
                    self.min = self.roots[r]

        return self.min

    def decrease_priority(self, node: FibNodeLazy, new_val: int) -> None:
        if new_val > node.val:
            return

        node.val = new_val
        parent = node.parent

        if parent is not None and node.val < parent.val:
            parent.children.remove(node)
            node.flag = False
            node.parent = None
            self.roots.append(node)
            self.cascading_cut(parent)

        if node.val < self.min.val:
            self.min = node

    def consolidate(self):
        temp = [None] * (2 * self.n)

        for root in self.roots[:]:
            x = root
            x_degree = x.degree
            while temp[x_degree] is not None:
                y = temp[x_degree]
                if x.val > y.val:
                    x, y = y, x

                y.parent = x
                y.flag = False
                x.children.append(y)
                temp[x_degree] = None
                self.roots.remove(y)
                x.degree += 1
                x_degree += 1
            temp[x_degree] = x

        return

    def cascading_cut(self, node: FibNodeLazy) -> None:
        parent = node.parent

        if parent is not None:
            if parent.flag is False:
                parent.flag = True
            else:
                parent.children.remove(node)
                parent.degree -= 1
                node.flag = False
                node.parent = None
                self.roots.append(node)
                self.cascading_cut(parent)

    def cut(self, node: FibNodeLazy) -> None:
        if node is not None and not node.vacant:
            node.parent = None
            self.roots.append(node)
        elif node is not None and node.vacant:
            for children in node.children:
                self.cut(children)

    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define
