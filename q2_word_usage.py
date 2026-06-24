import os
import pandas as pd
import requests


# ===================================================================================
#
#   Dado que o enunciado não indicou sinal verde, amarelo ou vermelho para uso de IA,
#   Foi tomada a liberdade por parte do aluno de usar a inteligencia artificial SOMENTE PARA 
#   OS CODIGOS QUE NÃO SE RELACIONAM A COMPETENCIAS DA DISCIPLINA. O uso da IA neste trabalho 
#   tem somente o objetivo de agregar ao produto final e não de suplementar o conhecimento do 
#   aluno a respeito da materia. 
#
#   Os prompts que geraram os codigos estão devidamente apontados no decorrer deste arquivo. 
#   Nota-se que nestes casos A SOLUÇÃO FOI PROJETADA PELO ALUNO e a IA teve somente o papel de
#   implementar o codigo. Nota-se também que "Feito com auxilio de IA" implica a presença de 
#   alterações do aluno sobre os codigos inicialmente gerados por IA (não foi realizado 
#   simplesmente Ctr+C Ctrl+V). 
# 
# ===================================================================================


URL = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/pt_br/pt_br_50k.txt"
FILE_PATH = "q2_pt_br_50k.csv"



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