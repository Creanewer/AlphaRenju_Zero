from math import sqrt
import numpy as np


class Node:
    count = 0

    def __init__(self, prior_prob, parent, color):
        
        """Information of the edge that leads to this node"""
        self._N = 0  # Number of visits
        self._Q = 0  # Quality of the edge
        self._W = 0  # Intermediate value for Q update
        self._P = prior_prob  # Prior probability predicted by network
        self._U = 0
        
        """parent and children nodes"""
        self._parent = parent  # the parent node
        self._children = []  # Empty list since it is not explored yet

        # when it is an end leaf
        self.is_end = False
        self.value = 0

        self.color = color  # color of next player
        self.num = Node.count
        Node.count += 1

    def N(self):
        return self._N

    def Q(self):
        return self._Q

    def U(self):
        return self._U

    def parent(self):
        return self._parent

    def children(self):
        return self._children
        
    def is_root(self):
        return self._parent is None
    
    def is_leaf(self):
        return self._children == []
    
    def upper_confidence_bound(self, c_puct):
        self._U = c_puct * self._P * sqrt(self._parent.N()) / (1+self._N)
        return self._U + self._Q
    
    def select(self, c_puct, legal_vec_current):
        ucb_list = np.array([node.upper_confidence_bound(c_puct) for node in self._children])
        ind = np.argsort(ucb_list)
        for i in range(len(ind)):
            if legal_vec_current[ind[-(i+1)]] == 1:
                action = ind[-(i+1)]
                break
        next_node = self._children[action]
        return next_node, action
        
    def expand(self, prior_prob, board_size=15):
        for i in range(board_size*board_size):
            prob = prior_prob[i]
            self._children.append(Node(prob, self, -self.color))

    def backup(self, value):
        self._N += 1
        self._W += value
        self._Q = self._W / self._N
        if not self.is_root():
            self._parent.backup(-value)