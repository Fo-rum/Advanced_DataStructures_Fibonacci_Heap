# explanations for member functions are provided in requirements.py
from __future__ import annotations

class FibNode:
    def __init__(self, val: int):
        self.val = val
        self.parent = None
        self.children = []
        self.flag = False
        self.degree = 0

    def get_value_in_node(self):
        return self.val

    def get_children(self):
        return self.children

    def get_flag(self):
        return self.flag

    def __eq__(self, other: FibNode):
        return self.val == other.val

class FibHeap:
    def __init__(self):
        # you may define any additional member variables you need
        self.roots = []
        self.min = None
        self.n = 0
        pass

    def get_roots(self) -> list:
        return self.roots

    def insert(self, val: int) -> FibNode:
        node = FibNode(val)
        self.roots.append(node)

        if self.min is None or node.val < self.min.val:
            self.min = node
        
        self.n += 1
        return node
        
    def delete_min(self) -> None:
        if self.min is None:
            return
        
        for child in self.min.children:
            self.roots.append(child)
            child.parent = None
        
        self.roots.remove(self.min)
        
        self.consolidate()

    def consolidate(self):
        temp = [None] * (2*self.n)

        for root in self.roots[:]:
            x = root
            x_degree = x.degree
            while temp[x_degree] is not None:
                y = temp[x_degree]
                if x.val > y.val:
                    x,y = y,x
                self.make_heap_link(y,x)
                temp[x_degree] = None
                x_degree += 1
            temp[x_degree] = x
        
        self.roots = []
        self.min = None
        for node in temp:
            if node is not None:
                self.roots.append(node)
                if self.min is None or node.val < self.min.val:
                    self.min = node

        """
        for i in range(0,len(temp)):
                if temp[i] is not None:
                    if temp[i].val < self.min.val:
                        self.min = temp[i]
                        """

    def make_heap_link(self, y: FibNode, x: FibNode) -> None:
        self.roots.remove(y)
        x.children.append(y)
        y.parent = x
        x.degree += 1
        y.flag = False

    def find_min(self) -> FibNode:
        return self.min
    
    def decrease_priority(self, node: FibNode, new_val: int) -> None:
        if new_val >= node.val:
            raise ValueError("Value of the newnode should be smaller than the current node value")
        node.val = new_val
        parent = node.parent

        if parent is not None and node.val < parent.val:
            self.cut(node,parent)
            self.cascading_cut(parent)
        
        if node.val < self.min.val:
            self.min = node


    def cut(self, node: FibNode, parent: FibNode) -> None:
        parent.children.remove(node)
        parent.degree -= 1
        node.parent = None
        self.roots.append(node)
        node.flag = False
    
    def cascading_cut(self, node: FibNode):
        parent = node.parent
        if parent is not None:
            if node.flag is False:
                node.flag = True
            else:
                self.cut(node, parent)
                self.cascading_cut(parent)


    # feel free to define new methods in addition to the above
    # fill in the definitions of each required member function (above),
    # and for any additional member functions you define
