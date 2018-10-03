import os
import argparse
import shutil


def copy_dir(src, dst):
    _, d_name = os.path.split(src)
    dist = os.path.join(dst, d_name)
    os.mkdir(dist)
    for file in os.listdir(src):
        source = os.path.join(src, file)
        shutil.copy(source, dist)


def run(args):
    if args.operation == 'copy':
        for from_dir in args.from_dir:
            if os.path.isdir(from_dir):
                copy_dir(from_dir, args.to)
            elif os.path.isfile(from_dir):
                shutil.copy(from_dir, args.to)
    elif args.operation == 'move':
        for from_dir in args.from_dir:
            shutil.move(from_dir, args.to)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--operation', type=str, choices=['move', 'copy'], help='some verbosity')
    parser.add_argument('-f', '--from', dest='from_dir', type=str, help='some verbosity', nargs='*')
    parser.add_argument('-t', '--to', type=str, help='some verbosity')
    parser.add_argument('--threads', type=int, help='')
    parser.set_defaults(func=run)
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
