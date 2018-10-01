class Node:

    def __init__(self, key, value, left=None, right=None, parent=None):
        self.key = key
        self.payload = value
        self.left = left
        self.right = right
        self.parent = parent

    def __str__(self):
        return str(self.payload)

    def get_childs(self):
        return '%s, %s' % (self.left, self.right)


class BinaryTree:

    def __init__(self):
        self.root = None
        self.size = 0

    def add(self, key, value):
        if self.root:
            self._add(key, value, self.root)
        else:
            self.root = Node(key, value)
        self.size += 1

    def _add(self, key, value, current):
        if key < current.key:
            if current.left:
                self._add(key, value, current.left)
            else:
                current.left = Node(key, value, parent=current)
        else:
            if current.right:
                self._add(key, value, current.right)
            else:
                current.right = Node(key, value, parent=current)

    def find(self, key):
        if self.root:
            return self._find(key, self.root)
        else:
            return None

    def _find(self, key, current):
        if not current:
            return None
        elif current.key == key:
            return current
        elif key < current.key:
            return self._find(key, current)
        else:
            return self._find(key, current)


if __name__ == '__main__':
    tree = BinaryTree()
    tree.add('key', 'value')
    print(tree.find('key'))
