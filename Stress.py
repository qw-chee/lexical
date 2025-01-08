'''
LexiCAL is a calculator for psycholinguistic variables.
Copyright (C) 2019 Chee, Q.W., Chow, K.J., Goh, W.D., & Yap, M.J.; National University of Singapore.

LeixCAL is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

LexiCAL is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from Phonemes import Phonemes
from Tokeniser import Tokeniser

class Stress:
    '''
    Class for computing stress/surface metrics including stress code and stress typicality.
    '''
    def __init__(self, key, *words):
        self.key = key
        self.set_primary_stress()
        self.set_secondary_stress()
        self.tokeniser = Tokeniser(key)
        self.tokeniser.set_recognise_stress()
        if words:
            self.stress_typicality_dic = self.make_stress_typicality_dic(words[0])

    def set_primary_stress(self):
        if self.key in Phonemes.SAMPA_KEYS:
            self.primary_stress = Phonemes.PRIMARY_STRESS_SAMPA
        elif self.key in Phonemes.IPA_KEYS:
            self.primary_stress = Phonemes.PRIMARY_STRESS_IPA
        elif self.key == Phonemes.CUSTOM_KEY and Phonemes.custom_primary_stress is not None:
            self.primary_stress = Phonemes.custom_primary_stress

    def set_secondary_stress(self):
        if self.key in Phonemes.SAMPA_KEYS:
            self.secondary_stress = Phonemes.SECONDARY_STRESS_SAMPA
        elif self.key in Phonemes.IPA_KEYS:
            self.secondary_stress = Phonemes.SECONDARY_STRESS_IPA

    def make_stress_typicality_dic(self, words):
        '''
        Creates a dictionary with keys = number of syllables and values = dictionary
        of stress-code to frequency mappings.
        :param words: list of words in string format.
        '''
        freq_dic = {}
        for word in words:
            num_syllables = self.tokeniser.get_num_syllables(word)
            stress_code = self.get_primary_stress_code(word)
            if num_syllables not in freq_dic:
                freq_dic[num_syllables] = {}
            if stress_code not in freq_dic[num_syllables]:
                freq_dic[num_syllables][stress_code] = 0
            freq_dic[num_syllables][stress_code] += 1

        stress_typicality_dic = {}
        for n_syllable in freq_dic:
            num_words_with_n_syllables = sum(freq_dic[n_syllable].values())
            if n_syllable not in stress_typicality_dic:
                stress_typicality_dic[n_syllable] = {}
            for stress_code in freq_dic[n_syllable]:
                stress_typicality = freq_dic[n_syllable][stress_code] / num_words_with_n_syllables
                stress_typicality_dic[n_syllable][stress_code] = stress_typicality
        return stress_typicality_dic

    def get_stress_typicality(self, word):
        '''
        Computes the stress typicality of the word using the stress typicality dict.
        :param word: word in string format.
        '''
        num_syllables = self.tokeniser.get_num_syllables(word)
        stress_code = self.get_primary_stress_code(word)
        if num_syllables < 2:
            return "NULL"
        if num_syllables not in self.stress_typicality_dic or \
                stress_code not in self.stress_typicality_dic[num_syllables]:
            return 0
        stress_typicality = self.stress_typicality_dic[num_syllables][stress_code]
        return stress_typicality

    def get_primary_stress_code(self, word):
        '''
        Gets the primary stress based on the primary stress symbol and the number of vowels.
        :param word: word in string format.
        '''
        tokenised_word = self.tokeniser.tokenise(word)
        num_vowels = 0
        vowels = Phonemes().get_vowels_by_key(self.key)
        if self.primary_stress not in tokenised_word:
            return 0
        for token in tokenised_word:
            if token in vowels:
                num_vowels += 1
            if token == self.primary_stress:
                return num_vowels + 1
        return 0

    def get_secondary_stress_code(self, word):
        '''
        Gets the secondary stress based on the secondary stress symbol and the number of vowels.
        :param word: word in string format.
        '''
        tokenised_word = self.tokeniser.tokenise(word)
        num_vowels = 0
        vowels = Phonemes().get_vowels_by_key(self.key)
        if self.secondary_stress not in tokenised_word:
            return 0
        for token in tokenised_word:
            if token in vowels:
                num_vowels += 1
            if token == self.secondary_stress:
                return num_vowels + 1
        return 0

