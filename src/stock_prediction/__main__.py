from importlib import resources

from stock_prediction.config import config


def main():
    print("Sample application")
    filepath = str(
        resources.files("stock_prediction.submodule.assets").joinpath("submodule_file.txt")
    )

    with open(filepath, "r") as file:
        content = file.read()

    print(content)
    print(config.ENVVAR)


if __name__ == "__main__":
    main()
