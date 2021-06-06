import inspect
import itertools
import nmigen_boards
import pkgutil
import os
import sys

from nmigen import *
from nmigen.cli import main
from nmigen.build import ResourceError
from nmigen_boards.test.blinky import Blinky

import hashlib


"""
Calculates a SHA-256 checksum for the given file.
"""
def sha256sum(path):
    h = hashlib.sha256()
    b = bytearray(128 * 1024)
    mv = memoryview(b)

    with open(path, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])

    return h.hexdigest()


"""
Reads a list of paths to the various toolchains from toolchains.txt to set in the PATH environment
variable. In addition, this function expands the HOME variable and checks whether the path exists.
"""
def read_toolchains():
    with open('toolchains.txt') as f:
        for line in f.readlines():
            if line.startswith('#'):
                continue

            line = line.replace('$HOME', os.environ['HOME'])
            line = line.strip()

            if not os.path.exists(line):
                continue

            yield line


"""
Imports all modules in nmigen_boards and returns 3-tuples with for each Platform class defined in
nmigen_boards the path of the Python file defining it, the name of the class and the class itself.
"""
def iter_platforms():
    for module in pkgutil.iter_modules(nmigen_boards.__path__):
        if module.name in ['extensions', 'resources']:
            continue

        module_name = 'nmigen_boards.' + module.name

        module = __import__(module_name)

        path = sys.modules[module_name].__file__

        for (name, clazz) in inspect.getmembers(sys.modules[module_name], inspect.isclass):
            if name.startswith('_'):
                continue

            if not name.endswith('Platform'):
                continue

            if clazz.__module__ != module_name:
                continue


            yield (path, name, clazz)


"""
Reads tested boards from boards.txt and returns a dictionary that maps the board name to the path,
the checksum and the toolchain.
"""
def read_boards():
    boards = {}

    try:
        with open('boards.txt', 'r') as f:
            for line in f.readlines():
                entry = line.split()

                boards[entry[0]] = tuple(entry[1:])
    except:
        pass

    return boards


"""
Reads in the tested boards and toolchains, then iterates over the Platform classes in nmigen_boards
and tries to build blinky for each platform using every toolchain possible until it builds or until
all possible toolchains failed to build blinky. On success, it writes the path and class name, the
checksum of the file and the toolchain to boards.txt to prevent rebuilding blinky if it has already
been built and the checksum hasn't changed. Finally, it prints the names of every platform that did
not succeed building.
"""
def main():
    toolchains = [''] + list(read_toolchains())
    boards = read_boards()
    failed = []

    for path, name, clazz in iter_platforms():
        checksum = sha256sum(path)

        if checksum == boards.get(path + ':' + name, (0,))[0]:
            continue

        env = dict(os.environ)
        built = False

        for toolchain in toolchains:
            try:
                if toolchain:
                    os.environ.update({'PATH': env['PATH'] + ':' + toolchain})

                clazz().build(Blinky(), do_program=False)

                with open('boards.txt', 'a') as f:
                    f.write('{}:{} {} {}\n'.format(path, name, checksum, toolchain))

                built = True

                break
            except:
                pass
            finally:
                os.environ.clear()
                os.environ.update(env)

        if not built:
            failed.append(name)

    print(failed)


if __name__ == '__main__':
    main()
