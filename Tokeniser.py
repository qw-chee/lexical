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
from Exceptions import TokeniseException

class Tokeniser:
    def __init__(self, key):
        self.phoneme_list = Phonemes().get_phonemes_by_key(key)
        self.phoneme_dict = self.make_phoneme_dict() # a dictionary of phonemes by char length
        self.list_of_chars = Phonemes().get_list_of_phoneme_chars(key)
        self.key = key

    def set_recognise_stress(self):
        if self.key in Phonemes.IPA_KEYS:
            self.phoneme_list.append(Phonemes.PRIMARY_STRESS_IPA)
            self.phoneme_list.append(Phonemes.SECONDARY_STRESS_IPA)
            self.phoneme_dict = self.make_phoneme_dict()
            self.list_of_chars.append(Phonemes.PRIMARY_STRESS_IPA)
            self.list_of_chars.append(Phonemes.SECONDARY_STRESS_IPA)
        elif self.key in Phonemes.SAMPA_KEYS:
            self.phoneme_list.append(Phonemes.PRIMARY_STRESS_SAMPA)
            self.phoneme_list.append(Phonemes.SECONDARY_STRESS_SAMPA)
            self.phoneme_dict = self.make_phoneme_dict()
            self.list_of_chars.append(Phonemes.PRIMARY_STRESS_SAMPA)
            self.list_of_chars.append(Phonemes.SECONDARY_STRESS_SAMPA)
        elif self.key == Phonemes.CUSTOM_KEY and Phonemes.custom_primary_stress is not None:
            self.phoneme_list.append(Phonemes.custom_primary_stress)
            self.phoneme_dict = self.make_phoneme_dict()
            self.list_of_chars.append(Phonemes.custom_primary_stress)

    def tokenise(self, string):
        if string == "":
            return ""

        # filter unrecognised chars from list
        filtered_string = ""
        for char in string:
            if char in self.list_of_chars:
                filtered_string += char
        try:
            result = self.parse(filtered_string)
        except TokeniseException:
            raise TokeniseException(string)

        if self.key == 1:
            result = self.correct_triphthongs(result, "ɪə", "ʊ")
            result = self.correct_triphthongs(result, "ʊə", "ʊ")
        elif self.key == 7:
            result = self.correct_triphthongs(result, "I@", "U")
            result = self.correct_triphthongs(result, "U@", "U")
        elif self.key == 5:
            result = self.correct_rhotics(result, Phonemes.ipa_de_rhotics,
                                          Phonemes.ipa_de_vowels, [])
        elif self.key == 12:
            result = self.correct_rhotics(result, Phonemes.klattese_rhotics,
                                          Phonemes.klattese_vowels, [])

        if self.key in Phonemes.SAMPA_KEYS:
            result = [i for i in result if i != '.']

        if result == []:
            raise TokeniseException(string)
        return result

    def make_phoneme_dict(self):
        phoneme_dict = {}
        for phoneme in self.phoneme_list:
            if len(phoneme) not in phoneme_dict:
                phoneme_dict[len(phoneme)] = []
            phoneme_dict[len(phoneme)].append(phoneme)
        return phoneme_dict

    def parse(self, string):
        output = []
        max_phoneme_length = max(self.phoneme_dict.keys())
        while len(string) > 0:
            phoneme_length = max_phoneme_length
            length_before = len(string)
            while phoneme_length > 0:
                if phoneme_length in self.phoneme_dict and \
                        string[0:phoneme_length] in self.phoneme_dict[phoneme_length]:
                    output.append(string[0:phoneme_length])
                    string = string[phoneme_length:]
                    break
                phoneme_length -= 1
            if len(string) == length_before:
                raise TokeniseException("")
        return output

    def correct_triphthongs(self, tokens, first, second):
        '''
        Shifts the second phone of a diphthong to the following token
        For example, changes "ɪə" (first), "ʊ" (second) sequence to "ɪ", "əʊ" sequence
        '''
        if not first in tokens:
            return tokens
        else:
            for i in range(len(tokens) - 1):
                if tokens[i] == first and tokens[i+1] == second:
                    tokens[i] = tokens[i][0]
                    tokens[i+1] = first[-1] + tokens[i+1]
        return tokens

    def correct_rhotics(self, tokens, rhotics, vowels, diphthongs):
        new_output = []
        for i in range(len(tokens)):
            if tokens[i] in rhotics:
                if i < len(tokens) - 1 and tokens[i + 1] in vowels:
                    if i == 0 or tokens[i - 1] not in diphthongs:
                        new_output.append(tokens[i][0])
                        new_output.append(tokens[i][1])
                        continue
            new_output.append(tokens[i])
        return new_output

    def get_num_syllables(self, word):
        tokenised_word = self.tokenise(word)
        num_vowels = 0
        vowels = Phonemes().get_vowels_by_key(self.key)
        for token in tokenised_word:
            if token in vowels:
                num_vowels += 1
        return num_vowels

    def convert_uk_to_us_ipa(self, word):
        tokenised_word = self.tokenise(word)
        new_word = ""
        for token in tokenised_word:
            new_word += Phonemes.UK_to_US_IPA_dic[token]
        return new_word

def tokenise_tests():
    words = ["əˈbandənm(ə)nt", "əkʌltʃəˈreʃ(ə)n", "əˈkwʌɪə", "ɑːˌtɪkjʊˈleɪʃ(ə)n", "ɑːˈtɪkjuleɪtɪd", "ɪə"]
    for w in words:
        try:
            print(Tokeniser(1).tokenise(w))
        except TokeniseException as e:
            print(e.word)
    us_words = ["ədˈmaɪ(ə)rər", "ˈaldʒi"]
    for w in us_words:
        try:
            print(Tokeniser(0).tokenise(w))
        except TokeniseException as e:
            print(e.word)
    sampa_words = ['dr"O.INz', '%aUt.S"aIn', 'sOlt."Sek@`']
    for w in sampa_words:
        try:
            print(Tokeniser(6).tokenise(w))
        except TokeniseException as e:
            print(e.word)
