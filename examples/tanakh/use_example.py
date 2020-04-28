"""
example of tanakh use
"""

from generate import TextGenerator


def keep_only_words(word: str) -> str:
    """
    clean the word
    :param word: the word to fix
    :return: only hebrew chars (no ;,. and so on)
    """
    return_str = ""
    for char in word:
        if 1488 <= ord(char) <= 1514:
            return_str += char
    return return_str


def main():
    text_class = TextGenerator.read_data("all tanakh.txt", keep_only_words)

    while True:
        start_word = input("enter input: ")
        # console need to support hebrew
        print(text_class.generate_text(20, start_word))


if __name__ == '__main__':
    main()
