# Python-Limerick-Reader
This project analyzes a poem and determines whether it is a **limerick** based on
formal structural rules. It was written as a learning exercise to practice
string processing, dictionary lookups, and rule-based validation in Python.

The program uses the CMU Pronouncing Dictionary to compute syllable counts
and rhyme patterns.

---

## Limerick Rules Implemented

A poem is considered a limerick if it satisfies all of the following:

- Exactly 5 lines
- Rhyme scheme: AABBA
  - Lines 1, 2, and 5 rhyme
  - Lines 3 and 4 rhyme
  - The A and B rhymes must be different
- Syllable counts:
  - Lines 1, 2, 5: 8 or 9 syllables
  - Lines 3, 4: 5 or 6 syllables

Syllables and rhymes are determined using phoneme data from the CMU dictionary.

---
### Run

python limerick_checker.py
You will then be prompted to enter the file name (poem.txt)
Result in terminal!
