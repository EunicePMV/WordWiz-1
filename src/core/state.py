from typing import List
from collections import defaultdict

from src.constants import *
from src.utils.trie import Trie

#############################################################
# self.ai.score        self.word        self.player.score   #
#               self.guesses[attempts][5]                   #
#               self.guesses[attempts][4]                   #
#               self.guesses[attempts][3]                   #
#               self.guesses[attempts][2]                   #
#               self.guesses[attempts][1]                   #
#               self.guesses[attempts][0]                   #
#                     self.pool % 5                         #
#                     self.pool % 5         self.button     #
#############################################################

class BoardState():
    def __init__(self):
        self.pool = dict(zip((i for i in range(10)), (' ' for _ in range(10))))
        self.guesses: List[List[dict | str]] = []
        self.word = None
        self.hints = defaultdict(defaultValue)
        self.trie = Trie()
        self.win = False
        self.attempts = []
        self.attempt = 0 #row
        self.index = 0 #col
        
        for _ in range(6):
            guess = []
            for i in range(5):
                guess.append(' ')
            self.guesses.append(guess)

        self.trie.save()
        self.trie.load()

    def reset(self):
        self.pool = dict(zip((i for i in range(10)), (' ' for _ in range(10))))
        self.guesses: List[List[dict | str]] = []
        self.word = "faced"
        self.hints = defaultdict(defaultValue)
        self.win = False
        self.attempts = []
        self.attempt = 0 #row
        self.index = 0 #col
        
        for _ in range(6):
            guess = []
            for _ in range(5):
                guess.append(' ')
            self.guesses.append(guess)

    def can_spell_guess(self):
        try:
            self.index = self.guesses[self.attempt].index(' ')
            return True
        except Exception as e:
            return False

    def spell_guess(self, key, val):
        self.index = self.guesses[self.attempt].index(' ')
        self.guesses[self.attempt][self.index] = {key: val}
        self.pool[key] = ' '
        return self.index
        
    def undo_guess(self, key, val):
        index = self.guesses[self.attempt].index({key: val})
        self.guesses[self.attempt][index] = ' '
        self.pool[key] = val
        return index

    def verify_guess(self):
        return self.trie.search(self.wordify_guess())
    
    def wordify_guess(self):
        return "".join([list(x.values())[0] if type(x) == dict else '' for x in self.guesses[self.attempt]])

    def accept_guess(self):
        word_guess = self.wordify_guess()
        #check if already attempted
        if not self.verify_guess(): return False
        if word_guess in self.attempts: return False
        if word_guess == self.word: self.win = True
        self.attempts.append(word_guess)
        #check win condition
        for index in range(5):
            if self.word[index] == word_guess[index]:
                self.hints[index] = self.word[index]

        self.index = 0
        self.attempt += 1

        return True
    
    def get_guess_attempts(self):
        return 6 - self.attempt