from pyy import is_pyy, ERROR; is_pyy(globals(), ERROR)

export def say_hello(name: str) -> None:
    print(f"hello, {name}!")

wipe say_hello