import os, sys, inspect

class Pyy:
    def __init__(self, filename: str) -> None:
        self.filename: str = filename
        with open(filename) as file:
            self.content: str = file.read()
    def compile(self) -> str | None:
        compiled: str = "from pyy import export as __pyyexport\nfrom pyy import wipe as __pyywipe"
        for line in self.content.split("\n"):
            indentation: int = len(line) - len(line.lstrip())
            if line.strip().removeprefix("#").strip() == "pyy=false":
                if "--force" in sys.argv:
                    exec(self.content)
                    return None
                raise PermissionError("pyy does not have permission to run that file, rerun with --force to use base python instead when this error is raised. (pyy=false comment found)")
            elif line.lstrip().startswith("public def") or line.lstrip().startswith("public class") or line.lstrip().startswith("public async def"):
                public_Pyy = Pyy(f"{line.lstrip().removeprefix('public def ').removeprefix('public class ').removeprefix('public async def ').split('(')[0].split(':')[0]}.pyy")
                compiled += f"\n{' '*indentation}{line.lstrip().removeprefix('public ').removesuffix(':')}:\n{'\n'.join([' '*(indentation+4)+line2 for line2 in ['...']+public_Pyy.compile().split('\n')])}"
            elif line.lstrip().startswith("public post def") or line.lstrip().startswith("public post class") or line.lstrip().startswith("public post async def"):
                public_Pyy = Pyy(f"{line.lstrip().removeprefix('public post def ').removeprefix('public post class ').removeprefix('public post async def ').split('(')[0].split(':')[0]}.pyy")
                compiled += f"\n{' '*indentation}{line.lstrip().removeprefix('public post ').removesuffix(':')}:\n{' '*(indentation+4)}def post():\n{'\n'.join([' '*(indentation+8)+line2 for line2 in ['...']+public_Pyy.compile().split('\n')])}"
            else:
                compiled += f"\n{line}"
        return compiled
    def __str__(self) -> str:
        return f"pyy=true"

NOTHING: int = 1
WARNING: int = 2
ERROR: int = 3

def is_pyy(__globals: dict, level: int = 1) -> bool:
    pyy: bool = "__pyy__" in __globals
    if level == 2 and not pyy:
        print("\033[92;1mwarning!\033[0m this script works better when run with pyy. learn more: https://github.com/by-semicolon/pyy")
        return pyy
    elif level == 3 and not pyy:
        raise RuntimeError("this script depends on and must be run with pyy. learn more: https://github.com/by-semicolon/pyy")
    else:
        return pyy