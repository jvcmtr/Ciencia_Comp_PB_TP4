import os
import pandas as pd
import requests

# Feito com auxilio de IA
# Prompt utilizado:
# """
#   I want a python script that does the following: 
#   pt_br_word_usage.py 
#   init() -> util function. checks if the file exists, or else, downloads it and save it as is in a csv format 
#   _download_file() -> util function for download from a public API or repository 
#   _delete_file() -> util function that deletes the file 
#   get_most_used(x) -> returns the x most used words
#   get_valid_chars(x) -> returns a list of unique characters in the first x words
# """

# Output da IA com alterações do aluno:

URL = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/pt_br/pt_br_50k.txt"
FILE_PATH = "q2_pt_br_50k.csv"


def _download_file(path: str = FILE_PATH):
    print("Downloading PT-BR frequency list...")

    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    with open(path, "w", encoding="utf-8") as f:
        f.write(response.text)

    print(f"Saved to {path}")


def _delete_file(path: str = FILE_PATH) -> None:
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted {path}")
    else:
        print(f"File '{path}' does not exist.")


def init(path: str = FILE_PATH) -> None:
    if not os.path.exists(path):
        _download_file(path)
    # else:
    #     print(f"'{path}' - File already exists.")


def _load_data(path: str = FILE_PATH) -> pd.DataFrame:
    return pd.read_csv(
        path,
        sep=r"\s+",
        header=None,
        names=["word", "count"],
        engine="python",
    )


def get_most_used(x: int = 1000, path: str = FILE_PATH) -> list[str]:
    if not os.path.exists(path):
        init(path)

    df = _load_data(path)
    return df.head(x)["word"].tolist()

def get_valid_chars(x: int = 50000, path: str = FILE_PATH) -> list[str]:
    """
    Returns a list of unique characters found in the first X most used words.
    """
    if not os.path.exists(path):
        init(path)

    df = _load_data(path)
    words = df.head(x)["word"].dropna().astype(str).tolist()

    chars = set()
    for word in words:
        chars.update(word)

    return sorted(chars)

init()