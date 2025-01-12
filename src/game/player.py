from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.core.board import Board

from collections import OrderedDict

from src.core.letters import Letter
from src.constants import *

class Player():
    def __init__(self, board: Board):
        self.board = board
        self.state = self.board.state
        self.word = []
        self.score = 0
    
    def codebreaker(self):
        #TRIAL ONLY FOR WHEN TURN = PLAYER and MODE = CODEBREAKER
        self.board.spell = self.state.can_spell_guess()  #if current board state allows for spelling

        letter: Letter
        for letter in self.board.letter_pool:         #for letters in the pool
            if not letter.clicked and letter not in self.board.letter_used:
                if letter.click(self.board.spell and self.board.click):
                    #State update
                    #Gets the index of the letter clicked from pool
                    attempted_index = self.board.letter_pool.sprites().index(letter)        
                    #Gets the FIRST empty slot from self.state.guesses[self.attempt]
                    attempted_index = self.state.spell_guess(attempted_index, letter.letter)
                    #Translate the position of the letter to the empty slot
                    letter.translate(vec2(tilesize.x*attempted_index, 100+(self.state.attempt*tilesize.y)))
                    self.board.letter_used.add(letter)   
                    self.board.click = False
                    break
                    # letter.emulated_click()
                
        for letter in self.board.letter_used:         #for letters used
            if not letter.clicked:
                if letter.click(self.board.click):
                    #State update
                    attempted_index = self.board.letter_pool.sprites().index(letter)
                    letter.translate(vec2(tilesize.x*attempted_index, 25))
                    self.state.undo_guess(attempted_index, letter.letter)
                    self.board.letter_used.remove(letter) 
                    self.board.click = False
                    break
        
        self.win()
        self.lose()
    def get_hints(self):
        ##THIS IS FOR FORCED HINT USAGE!
        letter: Letter
        for letter in self.board.letter_pool:         #for letters in the pool
            if not letter.clicked and letter not in self.board.letter_used:
                hints = OrderedDict(sorted(self.state.hints.items()))
                for index, hint in hints.items():
                    if hint and self.state.attempt < 6:
                        if (letter.letter == hint and 
                            self.state.guesses[self.state.attempt][index] == ' '):
                            self.state.guesses[self.state.attempt][index] = {self.board.letter_pool.sprites().index(letter) : hint}
                            letter.transition_speed = letter.transition_speed//4
                            letter.transition_snap = letter.transition_snap//4
                            letter.emulated_click()
                            letter.translate(vec2(tilesize.x*index, 100+(self.state.attempt*tilesize.y)))
                            # letter.lock = True
                            self.board.letter_used.add(letter)   
                            self.board.letter_hints.add(letter)
                            self.board.click = False
                            break
    def win(self):
        if self.state.win:
            print("Congratulations")
            self.score += WORD_GUESSED_REWARD
            self.score += self.state.get_guess_attempts() * ATTEMPTS_REWARD
            self.board.ai.score -= WORD_GUESSED_PENALTY
            self.end()

    def lose(self):
        if self.state.get_guess_attempts() == 0 and not self.state.win:
            print(f'YOU LOSE! word is {self.state.code_string}')
            self.score -= NO_GUESS_PENALTY
            self.board.ai.score += NO_GUESS_REWARD
            self.board.display_correct_word()
            self.end()

    def giveup(self):
        if self.board.turn and self.board.mode:
            print(f'YOU LOSE! word is {self.state.code_string}')
            self.score -= NO_GUESS_REWARD
            self.board.ai.score += NO_GUESS_REWARD
            self.board.display_correct_word()
            self.end()

    def end(self):
        self.board.update_turn()
        self.board.ai.word = ""
        self.board.change_turn(turns.PMM)
        self.board.phase += 1
        self.state.reset()
        print("Begin! now Player Mastermind")

    def mastermind(self):
        self.board.spell = self.state.can_spell_code() 
        # letter: Letter
        # for letter in self.board.letter_pool:         #for letters in the pool
        #     if not letter.clicked and letter not in self.board.letter_used:
        #         if letter.click(self.board.spell and self.board.click):
        #             #State update
        #             #Gets the index of the letter clicked from pool
        #             attempted_index = self.board.letter_pool.sprites().index(letter)        
        #             #Gets the FIRST empty slot from self.state.guesses[self.attempt]
        #             attempted_index = self.state.spell_code(attempted_index, letter.letter)
        #             #Translate the position of the letter to the empty slot
        #             letter.translate(vec2(tilesize.x*attempted_index, 100+(self.state.attempt*tilesize.y)))
        #             self.board.letter_used.add(letter)   
        #             self.board.click = False
        #             break
        #             # letter.emulated_click()

        # for letter in self.board.letter_used:         #for letters used
        #     if not letter.clicked:
        #         if letter.click(self.board.click):
        #             #State update
        #             attempted_index = self.board.letter_pool.sprites().index(letter)
        #             letter.translate(vec2(tilesize.x*attempted_index, 25))
        #             self.state.undo_code(attempted_index, letter.letter)
        #             self.board.letter_used.remove(letter) 
        #             self.board.click = False
        #             break
        