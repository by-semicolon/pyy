import sys, os
from . import Pyy

Pyy = Pyy(sys.argv[1])
compiled: str | None = Pyy.compile()
if compiled:
    exec(compiled, {"__file__": os.path.abspath(sys.argv[1]), "__pyy__": Pyy})