class Node:

    def __init__(self, value=None, prev=None, next=None):
        self.prev = prev
        self.value = value
        self.next = next


class DoubleLinkedList:

    def __init__(self):
        self.head = None
        self.tail = None
        self.len = 0

    def __str__(self):
        if self.head != None:
            current = self.head
            out = '[%s' % current.value
            while current.next != None:
                current = current.next
                out += ', %s' % current.value
            return out + ']'
        return '[]'

    def clear(self):
        self.__init__()

    def add(self, x):
        self.len += 1
        if self.head == None:
            self.head = self.tail = Node(x, None, None)
        else:
            self.tail.next = self.tail = Node(x, self.tail, None)

    def find(self, x):
        current = self.head
        while current.next:
            if current.value == x:
                return current.value
            else:
                current = current.next
        return None


if __name__ == '__main__':
    dlist = DoubleLinkedList()
    dlist.add(1)
    dlist.add(2)
    dlist.add(3)
    dlist.add(4)
    print(dlist)
    print(dlist.find(3))
    print(dlist.find(6))
