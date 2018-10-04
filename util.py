import os
import argparse
import shutil
from threading import Thread
from math import ceil
from queue import Queue


class Operation(Thread):

    def __init__(self, opr, queue, to, count):
        super(Operation, self).__init__()
        self.opr = opr
        self.queue = queue
        self.to = to
        self.count = count

    def copy_dir(self, src, dst):
        _, d_name = os.path.split(src)
        dist = os.path.join(dst, d_name)
        os.mkdir(dist) # FileExistsError
        for file in os.listdir(src):
            source = os.path.join(src, file)
            if os.path.isdir(source):
                print(source)
                self.copy_dir(source, dist)
            else:
                shutil.copy(source, dist)

    def copy(self, frm, dst):
        shutil.copy(frm, dst)

    def move(self, frm, dst):
        _, f_name = os.path.split(frm)
        dst = os.path.join(dst, f_name)
        shutil.move(frm, dst)

    def run(self):
        print('***')
        for _ in range(self.count):
            path = self.queue.get()
            if self.opr == 'copy':
                if os.path.isdir(path):
                    self.copy_dir(path, self.to)
                else:
                    self.copy(path, self.to)
            elif self.opr == 'move':
                self.move(path, self.to)
            self.queue.task_done()


def main(args):
    queue = Queue()

    if len(args.from_dir) > 1:
        threads = ceil(len(args.from_dir) / args.count)

        for _ in range(threads):
            thread = Operation(args.operation, queue, args.to, args.count)
            thread.setDaemon(True)
            thread.start()
    else:
        thread = Operation(args.operation, queue, args.to, args.count)
        thread.start()

    for path in args.from_dir:
        queue.put(path)
    queue.join()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--operation', type=str,
                        choices=['move', 'copy'], help='some verbosity')
    parser.add_argument('-f', '--from', dest='from_dir', type=str,
                        help='some verbosity', nargs='*')
    parser.add_argument('-t', '--to', type=str, help='some verbosity')
    parser.add_argument('--threads', dest='count', type=int, help='', default=1)
    args = parser.parse_args()
    main(args)
