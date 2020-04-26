from os import walk
from typing import List
import unicodedata

import html2text

FILES_DIR = r"all total"


# https://github.com/Emmeth/tools/blob/master/scripts/remove_nikkud.py
def removeNikkud(content: str) -> str:
    """
    remove all the hebrew vowels from text
    :param content: the hebrew text
    :return: hebrew text without vowels
    """

    normalized = unicodedata.normalize('NFKD', content)

    # range from 05B0-05BD, 05C0-05C2, 05C4-05C7
    result = ''.join([c for c in normalized if not unicodedata.combining(c)])
    return result


def get_files(dir_path: str) -> List[str]:
    """
    get files path from dir
    :param dir_path: the path to dir
    :return: list of paths
    """
    for (dirpath, dirnames, filenames) in walk(dir_path):
        for file_name in filenames:
            yield dir_path + '\\' + file_name


def read_data(file_path):
    """
    read and clean data from files
    :return: the words
    """

    forbidden_chars = ['*', '{', '{']

    for file_path in get_files(file_path):
    
        with open(file_path, 'rb') as f:
            raw_data = f.read().decode(encoding="ANSI")
            data_str = html2text.html2text(raw_data)
            with_no_vowels = removeNikkud(data_str)

            words = with_no_vowels.replace('-', " ")

            # skip title
            for word in words.split()[2:]:
                for forbidden_ch in forbidden_chars:
                    if forbidden_ch in word:
                        break
                else:
                    yield word


def main():
    with open("all tanakh.txt", "w") as f:
        for word in read_data(FILES_DIR):
            f.write(word)
            f.write(' ')

if __name__ == '__main__':
    main()
