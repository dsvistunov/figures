class Node:

    def __init__(self, data=None, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right

    def __str__(self):
        return str(self.data)

    def get_childs(self):
        return '%s, %s' % (self.left, self.right)


class BinaryTree:

    def __init__(self):
        self.root = None

    def add(self, data):
        return Node(data, None, None)

if __name__ == '__main__':
    left = Node('left', Node('lefts child'))
    right = Node('right', None, Node('rights child'))
    tree = Node('root', left, right)
    print(tree.get_childs())
    print(left.get_childs())
    print(right.get_childs())
