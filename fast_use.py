"""
fast text generate with file dialog
"""

from tkinter import filedialog
from generate import TextGenerator

#root = tk.Tk()
#root.withdraw()
def return_word(word: str) -> str:
    """
    not changing the word
    :param word: what to return
    :return: the input
    """
    return word

def main():
    print("enter path of text data:")
    file_path = filedialog.askopenfilename()
    print("loading...")
    text_generator = TextGenerator.read_data(file_path, return_word)
    while True:
        start_word = input("enter start word (empty for random start word): ")
        enter_len = input("enter number of words: ")
        generated_text = text_generator.generate_text(int(enter_len), start_word)
        print(generated_text)

if __name__ == '__main__':
    main()
