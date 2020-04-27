from generate import TextGenerator


def keep_only_words(word: str) -> str:
    return_str = ""
    for char in word:
        if 1488 <= ord(char) <= 1514:
            return_str += char
    return return_str


def main():
    text_class = TextGenerator.read_data("tool/all tanakh.txt", keep_only_words)

    while True:
        start_word = input("enter input: ")
        print(text_class.generate_text(20, start_word))


if __name__ == '__main__':
    main()
