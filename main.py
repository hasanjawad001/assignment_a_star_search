"""
    Implementation of A* search with 2 heuristics.
    author: Jawad Chowdhury.
"""

import math

class Node:
    """
    This class creates Node object based on each state.
    Keeps additional info of a state
    """
    def __init__(self, state=None, depth=None, f=None, parent=None):
        self.state = state
        self.depth = depth
        self.f = f
        self.parent = parent

    def print_state(self):
        l=len(self.state)
        c=0
        for row in self.state:
            for col in row:
                print(col, end=" ")
            if c!= l-1:
                print()
            c+=1
        return ""


class Puzzle:
    """
    The main class of an n-puzzle problem.
    Here according to the assignment no_tiles = 8 has been used.
    """
    def __init__(self, no_tiles=8):
        self.n = int(math.sqrt(no_tiles+1))
        self.frontier = []
        self.explored = []

    def get_state(self, state_name='', file_name=''):
        """
        Forms states and nodes based on the user input (from file with the provided file name)
        :param state_name: which state to form i.e. 'initial' or 'goal'
        :param file_name: file to take the user input from
        :return:
        """
        lines = []
        with open(file_name) as f:
            lines = f.readlines()
            state = [line.strip('\n').split(' ') for line in lines]
        if state_name=='initial':
            self.initial_state = state
            self.initial_node = Node(self.initial_state, 0, None, None)
        elif state_name=='goal':
            self.goal_state = state
            self.goal_node = Node(self.goal_state, None, None, None)

    def get_g_score(self, source, dest):
        """
        A measure to reach the source node from the initial.
        :param source: Node which g(n) value to measure
        :param dest: UNUSED
        :return: g(n) where n is the source node
        """
        return source.depth

    def get_h_score(self, source, dest):
        """
        A measure of heuristic value from the source node to goal/dest node.
        :param source: Node which h(n) value is to be measured
        :param dest: Goal Node
        :return: h(n) where n is the source node
        """
        h_score = 0
        if self.heuristic == 1:
            for i in range(self.n):
                for j in range(self.n):
                    if source.state[i][j] != '0' and source.state[i][j] != dest.state[i][j]:
                        h_score += 1
        if self.heuristic == 2:
            for i in range(self.n):
                for j in range(self.n):
                    if source.state[i][j] != '0' and source.state[i][j] != dest.state[i][j]:
                        dest_i, dest_j = self.get_location(dest.state, source.state[i][j])
                        h_score += abs(dest_i-i) + abs(dest_j-j)
        return h_score

    def get_f_score(self, source, dest):
        return self.get_g_score(source, dest) + self.get_h_score(source, dest)

    def get_location(self, state, elem):
        """
        To Find the row and column of the element in the state
        :param state: A list of list representing the state
        :param elem: value for which row and column index needs to be found
        :return: row and column index of elem in state
        """
        for r in range(self.n):
            for c in range(self.n):
                if state[r][c] == elem:
                    return r,c

    def swap_elem(self, state, r1, c1, r2, c2):
        new_state = []
        for row in state:
            new_row = []
            for col in row:
                new_row.append(col)
            new_state.append(new_row)
        temp = new_state[r1][c1]
        new_state[r1][c1] = new_state[r2][c2]
        new_state[r2][c2] = temp
        return new_state

    def expand(self, current_node):
        """
        Expands the current node to generate the child nodes
        :param current_node: node which needs to be expanded
        :return: list of child
        """
        r_blank, c_blank = self.get_location(current_node.state, '0')
        possible_options = [[r_blank, c_blank+1], [r_blank-1, c_blank], [r_blank, c_blank-1], [r_blank+1, c_blank]]
        possible_children = []
        for opt in possible_options:
            r = opt[0]
            c = opt[1]
            if r >= 0 and c >= 0 and r <= self.n-1 and c <= self.n-1:
                possible_children.append(opt)
        children = []
        for pc in possible_children:
            child_state = self.swap_elem(current_node.state, r_blank, c_blank, pc[0], pc[1])
            child_node = Node(child_state, current_node.depth+1, None, current_node)
            children.append(child_node)
        return children

    def run(self, heuristic=1):
        no_node_generated = 1
        no_node_expanded = 0
        self.heuristic = heuristic
        self.initial_node.f = self.get_f_score(self.initial_node, self.goal_node)
        self.frontier.append(self.initial_node)
        while len(self.frontier) != 0:
            current_node = self.frontier[0]
            self.frontier.remove(current_node)
            no_node_expanded += 1
            # print(current_node.print_state())
            # print(
            #     'g=%s, h=%s, f=%s'%(
            #     self.get_g_score(current_node, self.goal_node),
            #     self.get_h_score(current_node, self.goal_node),
            #     self.get_f_score(current_node, self.goal_node)
            # ))
            # print()
            if self.is_goal(current_node):
                print('Goal State Reached!!!')
                '''
                    printing path.
                '''
                print('===   PATH   ===')
                path = []
                cnode = current_node
                path.append(cnode)
                while cnode.parent != None:
                    path.append(cnode.parent)
                    cnode = cnode.parent
                path.reverse()
                for node in path:
                    print(node.print_state())
                    print()
                print('No of Nodes Generated : %s'%(no_node_generated,))
                print('No of Nodes Expanded : %s'%(no_node_expanded,))
                print('=====================')
                print()
                return
            children = self.expand(current_node)
            for child in children:
                no_node_generated += 1
                child.f = self.get_f_score(child, self.goal_node)
                self.frontier.append(child)
            self.frontier.sort(key=lambda x: x.f, reverse=False)
            self.explored.append(current_node)

    def is_goal(self, node):
        """
        Goal testing of a node
        :param node: node which needs to be checked
        :return: Boolean whether the node is the goal or not
        """
        if self.get_h_score(node, self.goal_node) == 0:
            return True
        else:
            return False

if __name__=="__main__":
    """
    This program takes user input from files.
    So updating the input file and using that file name in the following code should do the work.
    """

    print('Using heuristic 1: (Miss-placed Tiles)')
    p = Puzzle(no_tiles=8)
    p.get_state(state_name='initial', file_name='initial_state_6.txt')
    p.get_state(state_name='goal', file_name='goal_state_6.txt')
    p.run(heuristic=1)

    print('Using heuristic 2: (Manhattan Distance)')
    p = Puzzle(no_tiles=8)
    p.get_state(state_name='initial', file_name='initial_state_6.txt')
    p.get_state(state_name='goal', file_name='goal_state_6.txt')
    p.run(heuristic=2)