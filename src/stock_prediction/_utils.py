import requests
from loguru import logger


def download_file(url: str, path: str) -> None:
    """
    This function downloads a file from the specified URL and saves it to the specified path.
    Args:
        url (str): the URL of the file to download.
        path (str): the path to save the file to.

    Raises:
        Exception: if there is an error while downloading the file.
    """
    try:
        response = requests.get(url)
        with open(path, "wb") as file:
            file.write(response.content)

    except Exception as err:
        logger.error(err)
        raise err