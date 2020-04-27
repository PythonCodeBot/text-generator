from __future__ import annotations
import random

from typing import Dict
from collections import defaultdict
from collections import OrderedDict

from randomdict import RandomDict


class Word:
    """save the word and the next words"""

    next_words: Dict[Word, int]

    def __init__(self, word: str) -> None:
        """
        init the class
        :param word: which word is it
        """
        self.word: str = word
        self.total_words: int = 0
        self.next_words = defaultdict(int)

    def add_next_word(self, next_word: Word) -> None:
        """
        add word to data
        :param next_word: what to next word to come
        """
        self.next_words[next_word] += 1
        self.total_words += 1

    def finish_adding(self) -> None:
        """
        close the adding. sort the next words for random choosing by chance
        """
        orig_dict = self.next_words
        sorted_dict = {k: v for k, v in sorted(orig_dict.items(), key=lambda item: item[1])}
        self.next_words = OrderedDict(sorted_dict)

    def get_rand_word(self) -> Word:
        """
        get random word
        :return: the word as class or none if don't have any
        """
        random_num = random.random()

        for word in self.next_words.keys():
            chance = self.next_words[word] / self.total_words
            chance = 1 - chance
            if chance <= random_num:
                return word
        return None


class TextGenerator:
    """where the words data be store"""

    def __init__(self):
        """
        init the class
        """
        self.words_dict: RandomDict[str, Word] = RandomDict()

    @classmethod
    def read_data(cls, file_path: str, word_func) -> TextGenerator:
        """
        read data from file
        :param file_path: the file path
        :param word_func: word fixing func. get str, the word
         and return str, the fixed word. for example: make the word only english chars.
        :return: new load with data class
        """
        return_class = cls()

        with open(file_path, 'r') as file:
            # remove all next lines
            data = file.read().replace('\n', ' ')

        # remove empty spaces
        data = data.replace("  ", " ")

        words = data.split()

        for i, word in enumerate(words[:-1]):
            new_word = word_func(word)
            return_class.add_connection(new_word, word_func(words[i+1]))

        return_class.finish_adding()

        return return_class

    # @classmethod
    # def open_class(cls, file_path) -> TextGenerator:
    #     fileObject = open(file_path, 'r')
    #     # load the object from the file into var b
    #     this_class = pickle.load(fileObject)
    #     return this_class

    # def save_class(self, file_path) -> None:
    #     fileObject = open(file_path, 'wb')
    #     pickle.dump(self ,fileObject)
    #     fileObject.close()

    def generate_text(self, text_len: int, start_word: str=None) -> str:
        """
        generate new 'random' text
        :param text_len: how much words
        :param start_word: the start of the text
        :return: the new text
        """
        return_str = ""

        if start_word is None:
            start_word = self.get_random_word()
        elif start_word not in self.words_dict.keys:
            start_word = Word(start_word)
        else:
            start_word = self.words_dict[start_word]

        word_before: Word = start_word
        for _ in range(text_len):
            return_str += word_before.word + " "
            word_before = word_before.get_rand_word()

            if word_before is None:
                word_before = self.get_random_word()

        return return_str

    def get_random_word(self) -> Word:
        """
        :return random word from the enter data
        :return: random word
        """
        return self.words_dict.random_value()

    def do_word_exist(self, word) -> bool:
        """
        check if word exist
        :param word: which word to search
        :return: if exist
        """
        return word in self.words_dict.keys

    def add_word(self, word: str) -> None:
        """
        add new word to data if not exist
        :param word: which word to check and add
        """
        if not self.do_word_exist(word):
            self.words_dict[word] = Word(word)

    def get_word(self, word: str) -> Word:
        """
        get word class from the data
        :param word: which word to get
        :return: the word as class 'Word'
        """
        # add if not exist
        self.add_word(word)
        return self.words_dict[word]

    def add_connection(self, before: str, word: str) -> None:
        """
        add data.
        :param before: the origin word
        :param word: the word after
        """
        next_word = self.get_word(word)
        self.get_word(before).add_next_word(next_word)

    def finish_adding(self) -> None:
        """
        tell to all the words to sort. this is how it make random by changes
        """
        for value, key in self.words_dict.values:
            key.finish_adding()

    def print_data(self) -> None:
        """
        print all the words and the next words times
        """
        for key, value in self.words_dict.values:
            print(key, ":")
            for next_word in value.next_words.keys():
                times = value.next_words[next_word]
                print(next_word.word, ":", times)
