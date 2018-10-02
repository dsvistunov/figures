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

    def delete(self, key):
        if self.size > 1:
            node = self._find(key, self.root)
            if node:
                self.remove(node)
                self.size -= 1
            else:
                raise KeyError('Key not in tree')
        elif self.size == 1 and self.root.key == key:
            self.root = None
            self.size -= 1
        else:
            raise KeyError('Key not in tree')

    def findSuccessor(self):
        succ = None
        if self.right:
            succ = self.right.findMin()
        else:
            if self.parent:
                if self.parent and self.parent.left == self:
                    succ = self.parent
                else:
                    self.parent.right = None
                    succ = self.parent.findSuccessor()
                    self.parent.right = self
        return succ

    def findMin(self):
        current = self
        while current.left:
            current = current.left
        return current

    def remove(self, current):
        if current.left:
            if current == current.parent.left:
                current.parent.left = None
            else:
                current.parent.right = None
        elif current.left and current.right:
            succ = current.findSuccessor()
            succ.spliceOut()
            current.key = succ.key
            current.payload = succ.payload
        else:
            if current.left:
                if current.parent and current.parent.left == current:
                    current.left.parent = current.parent
                    current.parent.left = current.left
                elif current.parent and current.parent.right == current:
                    current.left.parent = current.parent
                    current.parent.right = current.left
                else:
                    current.key = current.left.key
                    current.payload = current.left.payload
                    current.left = current.left.left
                    current.right = current.left.right
            else:
                if current.parent and current.parent.left == current:
                    current.left.parent = current.parent
                    current.parent.left = current.right
                elif current.parent and current.parent.right == current:
                    current.left.parent = current.parent
                    current.parent.right = current.right
                else:
                    current.key = current.right.key
                    current.payload = current.right.payload
                    current.left = current.right.left
                    current.right = current.right.right




if __name__ == '__main__':
    tree = BinaryTree()
    tree.add('key', 'value')
    print(tree.find('key'))
    tree.delete('key')
    print(tree.find('key'))
