# write the code to import namedtuple
from collections import namedtuple
from urllib.request import urlopen


URL = 'http://zeus.cs.pacificu.edu/chadd/cs160/dictionary.txt'


# define the namedtuple word to contain: 
# the word, the number of syllables, the last syllable
Word = namedtuple('word', 'Word NumSyllables LastSyllable')


# Write the function countSyllables that will
# take a List of phonemes and return the number
# of syllables in the phonemes.
def countSyllables(phonemes):
    syllablesCount = 0

    for phoneme in phonemes:
        if phoneme[-1].isdigit():
            syllablesCount += 1

    return syllablesCount


# Write the function findLastSyllable that will
# take a List of phonemes and return the last
# syllable.  For example:
# [‘R’, ‘AO1’, ‘NG’] would return AONG
def findLastSyllable(phonemes):
    #pass

    lastSyllablePosition = -1
    for i in range(len(phonemes) -1, - 1, - 1):
        if phonemes[i][-1].isdigit():
            lastSyllablePosition = i
            break
            
    if lastSyllablePosition == -1:
        return ""
    

    endSyllable = ""
    for i in range (lastSyllablePosition, len(phonemes)):
        phoneme = phonemes[i]

        if phoneme[-1].isdigit():
            phoneme = phoneme[:-1]
        endSyllable += phoneme
    
    return endSyllable  
  

# cleanPunctuation just returns a clean word. Did this to avoid repeated code 
def cleanPunctuation(word):
    return word.strip("',.!?:;").upper()    

# openDictionary takes in the CMU dictionary url and creates a dictionary of all the words in there (ignoring lines with ;;;)
def openDictionary(dictiornaryUrl):
    try:
        with urlopen (dictiornaryUrl) as response:
            lines = response.read().decode('UTF-8').split('\n')
            
            dictionary = {}
            for line in lines:
                if not (line.startswith(';;;')):
                    parts = line.split()
                    if parts:
                        rawWord = parts[0]
                        
                        wordKey = rawWord.split("(")[0].upper()
                        
                        phonemes = parts[1:]
                        syllables = countSyllables(phonemes)
                        endSyllable = findLastSyllable(phonemes)
                        
                        dictionary[wordKey] = Word(wordKey, syllables, endSyllable)
            return dictionary
        
    except Exception as err:
        print('ERROR LOADING URL', err)
        dictionary = {}
        return dictionary
    

# readPoem has the file name the user inputs as the parameter. 
# from there, we attempt to open the file and count how many lines is in the file.
# if it satisfies the 5 line rule, it will return a clean limerick with no punctuation    
def readPoem(fileName):
    lineCount = 0
    cleaned = []
    
    try:
        with open (fileName, 'r') as inFile:
            content = inFile.readlines()

            for line in content:
                lineCount += 1
                parts = [word.strip(",.!?'") for word in line.split()]
                cleaned.append(" ".join(parts))

            if lineCount != 5:
                print('This poem must have exactly five lines')    
                return []
            
        return cleaned

    
    except Exception as err:
        print(f'Invalid file name: {fileName}')
        cleaned = []
        return cleaned
        

# validLimerick has two parameters: the limerick being analyzed and the dictionary we created
# determines if the limerick is valid - if it breaks any limerick rules, it will return a message 
# saying what is wrong with the limerick
def validLimerick(limeRick, dictionary):
    syllablesNeeded = {0 : [8,9], 1 : [8,9], 2 : [5,6], 3 : [5,6], 4 : [8,9]}
    syllableCount = []
    lastRhymes = []
    
    syllablesInLine = 0
    #bBadSyllables = False
    bBadRhymes = False

    for line in limeRick:
        syllablesInLine = 0
        words = line.split()
        lastWord = cleanPunctuation(words[-1])

        if lastWord not in dictionary:
            print("Word was NOT found in the dictionary")
            return 'FAILED LIMERICK'
        
        for word in words:
            cleanWord = cleanPunctuation(word)
            if cleanWord in dictionary:
                syllablesInLine += dictionary[cleanWord].NumSyllables
            else:
                print(f'FAILED LIMERICK. WORD {cleanWord} was NOT in dictionary')
                return 'FAILED LIMERICK'
            
        syllableCount.append(syllablesInLine)
        lastRhymes.append(dictionary[lastWord].LastSyllable)
        print(f'{syllablesInLine} {dictionary[lastWord].LastSyllable}')
    
    print()


    bBadSyllables = False
    for i, validSyllables in syllablesNeeded.items():
        if syllableCount[i] not in validSyllables:
            bBadSyllables = True
        
    a_ok = (lastRhymes[0] == lastRhymes[1] == lastRhymes[4])
    b_ok = (lastRhymes[2] == lastRhymes[3])
    a_diff_b = (lastRhymes[0] != lastRhymes[2])
    bBadRhymes = not (a_ok and b_ok and a_diff_b)

    #if  not (lastRhymes[0] == lastRhymes[1] == lastRhymes[4] and lastRhymes[2] == lastRhymes[3]):
        #bBadRhymes = True

    if bBadRhymes and bBadSyllables:
        return 'FAILED LIMERICK - bad syllable count and bad rhyme'
    elif bBadSyllables:
        return'FAILED LIMERICK! - bad syllable count'
    elif bBadRhymes:
        return 'FAILED LIMERICK! - bad rhyme'
    else:
        return 'LIMERICK!'


dictionary = openDictionary(URL)
if dictionary:
    fileName = input('Enter the name of the file:')
    limeRick = readPoem(fileName)
    if limeRick:
        result = validLimerick(limeRick, dictionary)
        print(result)