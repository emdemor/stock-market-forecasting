from importlib import resources


def main():
    print("Sample application")
    filepath = str(resources.files("anothermodule").joinpath("text.txt"))

    with open(filepath, "r") as file:
        content = file.read()

    print(content)
