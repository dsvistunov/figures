import os
import argparse
import shutil
from threading import Thread


class Operation(Thread):

    def __init__(self, opr, frm, to):
        super(Operation, self).__init__()
        self.opr = opr
        self.frm = frm
        self.to = to

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
        if self.opr == 'copy':
            if os.path.isdir(self.frm):
                self.copy_dir(self.frm, self.to)
            else:
                self.copy(self.frm, self.to)
        elif self.opr == 'move':
            self.move(self.frm, self.to)


def main(args):
    if len(args.from_dir) > 1:
        for src in args.from_dir:
            threard = Operation(args.operation, src, args.to)
            threard.start()
    else:
        src = args.from_dir[0]
        threard = Operation(args.operation, src, args.to)
        threard.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--operation', type=str,
                        choices=['move', 'copy'], help='some verbosity')
    parser.add_argument('-f', '--from', dest='from_dir', type=str,
                        help='some verbosity', nargs='*')
    parser.add_argument('-t', '--to', type=str, help='some verbosity')
    parser.add_argument('--threads', type=int, help='')
    args = parser.parse_args()
    main(args)
