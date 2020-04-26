import csv
import random
import pickle


songLen = 8
trainNum = 1000*10

#filePlace = 'C:/Users/User/Desktop/a/abcnews-date-text.csv'
#rowName = 'headline_text'

#fileOpen = False

#filePlace.replace("\\", "/")

class saveClass:
    def __init__(self, save):
        self.save = save

class remeber:
    def __init__(self, word):
        self.word = word
        self.nextWords = {}

    def __eq__(self, word):
        return self.word == word

    def addWord(self, word):
        if word not in self.nextWords:
            self.nextWords[word] = 0
        self.nextWords[word] += 1

    def __repr__(self):
        return self.word + " : " + str(self.nextWords)

classList = []
def deletJunk(str):
    str = str.lower()
    str = ''.join(x for x in str if x.isalpha() or x == "\n" or x == " ")

    if (str != "\n"):
        str = str.replace("\n", "")

    return ' '.join(str.split())


def newClass(str):
    index = 0
    for x in classList:
        if (x == str):
            return index
        index += 1
    classList.append(remeber(str))
    return index

def generateWord(word):
    numberOfWords = 0
    for oneClass in classList:
        if oneClass == word:

            if (len(oneClass.nextWords) == 0):
                return random.choice(classList).word


            numberOfWords = sum(oneClass.nextWords.values())

            last = len(oneClass.nextWords)

            for index, (key, value) in enumerate(sorted(oneClass.nextWords.items())):
                #if last
                if (last == index):
                    return key

                probability = value / numberOfWords
                if random.random() <= probability:
                    return key

def read_train_data(filePlace):
    with open(filePlace, mode='r', encoding='utf-8', errors='ignore') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for songIndex, row in enumerate(csv_reader):

            if (songIndex > trainNum):
                break

            song = deletJunk((row[rowName]))
            print(song)


            wordsList = song.split(" ")

            print(len(wordsList))
            for index, word in enumerate(wordsList):
                if word == "":
                    continue
                newIndex = newClass(word)



                try:
                    tempWord = wordsList[index + 1]
                    if tempWord == '':
                        continue
                    classList[newIndex].addWord(tempWord)
                except:
                    pass

        #print(classList)

    file_Name = "/".join(filePlace.split("/")[:-1]) + "/" + str(trainNum) + " " + filePlace.split("/")[-1].replace(".csv", "")
    # open the file for writing
    fileObject = open(file_Name,'wb')
    pickle.dump(classList ,fileObject)
    fileObject.close()

def open_class(fle_place):
    fileObject = open(fle_place, 'r')
    # load the object from the file into var b
    classList = pickle.load(fileObject)

    return classList

def main():
    while True:
        nextWord = (input("\nenter start word: "))

        print("your song: ")
        for x in range(songLen):
            print(nextWord, end= " ")
            nextWord = generateWord(nextWord)

            if nextWord == None:
                nextWord =  random.choice(classList).word

if __name__ == '__main__':
    main()

