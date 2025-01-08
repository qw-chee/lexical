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

from ReadWrite import read_csv

class Phonemes:
    ipa_us_cons = ['b', 'd', 'dʒ', 'ð', 'f', 'ɡ', 'h', 'j', 'k', 'l', 'm', 'n', 'ŋ', 'p', 'r', 's', 'ʃ', 't', 'tʃ', 'θ',
                   'v', 'w', 'z', 'ʒ', 'ʍ', 'x', 'ʔ']
    ipa_us_vowels = ['ɪ', 'i', 'ɛ', 'æ', 'ɑ', 'ɔ', 'ʊ', 'u', 'ə', 'eɪ', 'aɪ', 'aʊ', 'oʊ', 'ɔɪ']
    ipa_us_diphthongs = ['eɪ', 'aɪ', 'aʊ', 'oʊ', 'ɔɪ']
    ipa_us_phonemes = ipa_us_vowels + ipa_us_cons

    ipa_uk_cons = ['b', 'd', 'dʒ', 'ð', 'f', 'ɡ', 'h', 'j', 'k', 'l', 'm', 'n', 'ŋ', 'p', 'r', 's', 'ʃ', 't', 'tʃ', 'θ',
                   'v', 'w', 'z', 'ʒ', 'ʍ', 'x', 'ʔ']
    ipa_uk_vowels = ['ɪ', 'iː', 'i', 'ɛ', 'a', 'ɑː', 'ɒ', 'ɔː', 'ʊ', 'uː', 'ʌ', 'ə', 'əː', 'ɪə', 'ɛː', 'ʊə', 'eɪ', 'aʊ',
                     'ʌɪ', 'əʊ', 'ɔɪ']
    ipa_uk_phonemes = ipa_uk_cons + ipa_uk_vowels

    ipa_fr_cons = ['b', 'd', 'f', 'ɡ', 'k', 'l', 'm', 'n', 'ɲ', 'ŋ', 'p', 'ʀ', 's', 'ʃ', 't', 'v', 'z', 'ʒ', 'j',
                   'w', 'ɥ']
    ipa_fr_vowels = ['a', 'ɑ', 'e', 'ɛ', 'ɛː', 'ə', 'i', 'œ', 'ø', 'o', 'ɔ', 'u', 'y', 'ɑ̃', 'ɛ̃', 'œ̃', 'ɔ̃']
    ipa_fr_phonemes = ipa_fr_cons + ipa_fr_vowels

    ipa_es_cons = ['b', 'β', 'd', 'ð', 'f', 'ɡ', 'ɣ', 'ʝ', 'k', 'l', 'ʎ', 'm', 'n', 'ɲ', 'ŋ', 'p', 'r', 'ɾ', 's', 'θ',
                   't', 'tʃ', 'v', 'x', 'z', 'ʃ', 'j', 'w']
    ipa_es_vowels = ['a', 'i', 'o', 'e', 'u']
    ipa_es_phonemes = ipa_es_cons + ipa_es_vowels

    ipa_nl_cons = ['b', 'd', 'f', 'ɣ', 'h', 'j', 'k', 'l', 'm', 'n', 'ŋ', 'p', 'r', 's', 't', 'v', 'ʋ', 'x', 'z',
                   'ɡ', 'c', 'ɲ', 'ʃ', 'ʒ']
    ipa_nl_vowels = ['ɑ', 'ɛ', 'ɪ', 'ɔ', 'ʏ', 'ə', 'aː', 'eː', 'i', 'oː', 'y', 'øː', 'u', 'ɛi', 'œy', 'ɑu', 'ɑi', 'ɔi',
                   'iu', 'yu', 'ui', 'aːi', 'eːu', 'oːi', 'iː', 'yː', 'uː', 'ɔː', 'ɛː', 'œː', 'ɑː', 'ɑ̃', 'ɛ̃', 'ɔ̃', 'œ̃']
    ipa_nl_phonemes = ipa_nl_cons + ipa_nl_vowels

    ipa_de_cons = ['b', 'ç', 'd', 'f', 'ɡ', 'h', 'j', 'k', 'l', 'm', 'n', 'ŋ', 'p', 'pf', 'r', 's', 'ʃ', 't', 'ts',
                   'v', 'x', 'z', 'ʔ', 'tʃ', 'dʒ', 'ʒ', 'i̯', 'u̯']
    ipa_de_vowels = ['a', 'aː', 'ɛ', 'ɛː', 'eː', 'ɪ', 'iː', 'ɔ', 'oː', 'œ', 'øː', 'ʊ', 'uː', 'ʏ', 'yː', 'ə', 'aɪ',
                     'aʊ', 'ɔʏ', 'uɪ', 'ɐ', 'l̩', 'm̩', 'n̩']
    ipa_de_rhotics = ['iːr', 'ɪr', 'yːr', 'ʏr', 'eːr', 'ɛr', 'ɛːr', 'øːr', 'œr', 'aːr', 'ar', 'uːr', 'ʊr', 'oːr', 'ɔr']
    ipa_de_phonemes = ipa_de_cons + ipa_de_vowels

    klattese_vowels = ['I', 'i', 'E', '@', 'a', 'c', 'U', 'u', '^', 'x', '|', 'e', 'Y', 'W', 'o', 'O', 'R', 'X',
                       'N', 'M', 'L']
    klattese_cons = ['b', 'd', 'J', 'D', 'f', 'g', 'h', 'y', 'k', 'l', 'm', 'n', 'G', 'p', 'r', 's', 'S', 't', 'C', 'T',
                     'v', 'w', 'z', 'Z']
    klattese_rhotics = ['ar', 'cr', 'or', 'Ir', 'Er', '@r', 'Ur', 'Yr', 'Wr']
    klattese_phonemes = klattese_cons + klattese_vowels

    sampa_us_vowels = ['I', 'i', 'E', 'a', 'A', 'O', 'U', 'u', '@', 'e', 'V', 'aI', 'aU', 'o', 'OI', '3`', '@`',
                       'm=', 'n=', 'l=']
    sampa_us_cons = ['b', 'd', 'dZ', 'D', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'N', 'p', 'r', 's', 'S', 't', 'tS',
                     'T', 'v', 'w', 'z', 'Z', 'W', 'x', '?', '4']
    sampa_us_phonemes = sampa_us_cons + sampa_us_vowels + ['.']

    sampa_uk_vowels = ['I', 'i:', 'i', 'E', 'a', 'A:', 'Q', 'O:', 'U', 'u:', 'V', '@', '@:', 'I@', 'E:', 'U@', 'eI',
                       'aU', 'aI', '@U', 'OI', '=m', '=n', '=l']
    sampa_uk_cons = ['b', 'd', 'dZ', 'D', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'N', 'p', 'r', 's', 'S', 't', 'tS',
                     'T', 'v', 'w', 'z', 'Z', 'W', 'x', '?']
    sampa_uk_phonemes = sampa_uk_cons + sampa_uk_vowels + ['.']

    sampa_fr_vowels = ['a', 'A', 'e', 'E', 'E:', '@', 'i', '9', '2', 'o', 'O', 'u', 'y', 'a~', 'e~', '9~', 'o~']
    sampa_fr_cons = ['b', 'd', 'f', 'g', 'k', 'l', 'm', 'n', 'J', 'N', 'p', 'R', 's', 'S', 't', 'v', 'z',
                     'Z', 'j', 'w', 'H']
    sampa_fr_phonemes = sampa_fr_cons + sampa_fr_vowels + ['.']

    sampa_es_vowels = ['a', 'i', 'o', 'e', 'u']
    sampa_es_cons = ['b', 'B', 'd', 'D', 'f', 'g', 'G', 'jj', 'k', 'l', 'L', 'm', 'n', 'J', 'N', 'p', 'rr', 'r', 's',
                     'T', 't', 'tS', 'v', 'x', 'z', 'S', 'j', 'w']
    sampa_es_phonemes = sampa_es_cons + sampa_es_vowels + ['.']

    sampa_nl_vowels = ['A', 'E', 'I', 'O', 'Y', '@', 'a:', 'e:', 'i', 'o:', 'y', '2:', 'u', 'Ei', '9y', 'Au', 'Ai',
                       'Oi', 'iu', 'yu', 'ui', 'a:i', 'e:u', 'o:i', 'i:', 'y:', 'u:', 'O:', 'E:', '9:', 'A:', 'A~',
                       'E~:', 'O~', '9~']
    sampa_nl_cons = ['b', 'd', 'f', 'G', 'h', 'j', 'k', 'l', 'm', 'n', 'N', 'p', 'r', 's', 't', 'v', 'P', 'x', 'z',
                     'g', 'c', 'J', 'S', 'Z']
    sampa_nl_phonemes = sampa_nl_cons + sampa_nl_vowels + ['.']

    sampa_de_vowels = ['a', 'a:', 'E', 'E:', 'e:', 'I', 'i:', 'O', 'o:', '9', '2:', 'U', 'u:', 'Y', 'y:', '@', 'aI',
                       'aU', 'OY', 'uI', '6']
    sampa_de_cons = ['b', 'C', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'N', 'p', 'pf', 'R', 's', 'S', 't', 'ts',
                     'v', 'x', 'z', '?', 'tS', 'dZ', 'Z']
    sampa_de_rhotics = ['i:6', 'I6', 'y:6', 'Y6', 'e:6', 'E6', 'E:6', '2:6', '96', 'a:6', 'a6', 'u:6', 'U6', 'o:6', 'O6']
    sampa_de_phonemes = sampa_de_cons + sampa_de_vowels + ['.']

    UK_to_US_IPA_dic = {'b': 'b', 'd': 'd', 'dʒ': 'dʒ', 'ð': 'ð', 'f': 'f', 'ɡ': 'ɡ', 'h': 'h', 'j': 'j', 'k': 'k',
                        'l': 'l', 'm': 'm', 'n': 'n', 'ŋ': 'ŋ', 'p': 'p', 'r': 'r', 's': 's', 'ʃ': 'ʃ', 't': 't',
                        'tʃ': 'tʃ', 'θ': 'θ', 'v': 'v', 'w': 'w', 'z': 'z', 'ʒ': 'ʒ', 'ʍ': 'ʍ', 'x': 'x', 'ʔ': 'ʔ',
                        'ɪ': 'ɪ', 'iː': 'i', 'i': 'i', 'ɛ': 'ɛ', 'a': 'æ', 'ɑː': 'ɑr', 'ɒ': 'ɑ', 'ɔː': 'ɔr', 'ʊ': 'ʊ',
                        'uː': 'u', 'ʌ': 'ə', 'ə': 'ə', 'əː': 'ər', 'ɪə': 'ɪr', 'ɛː': 'ɛr', 'ʊə': 'ʊr', 'eɪ': 'eɪ',
                        'aʊ': 'aʊ', 'ʌɪ': 'aɪ', 'əʊ': 'oʊ', 'ɔɪ': 'ɔɪ', 'ˈ': 'ˈ', 'ˌ': 'ˌ'}

    custom_cons = []
    custom_vowels = []
    custom_phonemes = []
    custom_primary_stress = None

    PRIMARY_STRESS_IPA = "ˈ"
    SECONDARY_STRESS_IPA = "ˌ"
    PRIMARY_STRESS_SAMPA = '"'
    SECONDARY_STRESS_SAMPA = "%"

    IPA_KEYS = [0, 1, 2, 3, 4, 5]
    SAMPA_KEYS = [6, 7, 8, 9, 10, 11]
    KLATTESE_KEY = 12
    CUSTOM_KEY = 13

    def get_phonemes_by_key(self, key, *fname):
        if key == 0:
            return Phonemes.ipa_us_phonemes.copy()
        elif key == 1:
            return Phonemes.ipa_uk_phonemes.copy()
        elif key == 2:
            return Phonemes.ipa_fr_phonemes.copy()
        elif key == 3:
            return Phonemes.ipa_es_phonemes.copy()
        elif key == 4:
            return Phonemes.ipa_nl_phonemes.copy()
        elif key == 5:
            return Phonemes.ipa_de_phonemes.copy()
        elif key == 6:
            return Phonemes.sampa_us_phonemes.copy()
        elif key == 7:
            return Phonemes.sampa_uk_phonemes.copy()
        elif key == 8:
            return Phonemes.sampa_fr_phonemes.copy()
        elif key == 9:
            return Phonemes.sampa_es_phonemes.copy()
        elif key == 10:
            return Phonemes.sampa_nl_phonemes.copy()
        elif key == 11:
            return Phonemes.sampa_de_phonemes.copy()
        elif key == 12:
            return Phonemes.klattese_phonemes.copy()
        elif key == 13:
            if not Phonemes.custom_phonemes:
                self.get_custom_phonemes(fname[0])
            return Phonemes.custom_phonemes.copy()
        else:
            raise Exception("Key is invalid")

    def get_vowels_by_key(self, key, *fname):
        if key == 0:
            return Phonemes.ipa_us_vowels.copy()
        elif key == 1:
            return Phonemes.ipa_uk_vowels.copy()
        elif key == 2:
            return Phonemes.ipa_fr_vowels.copy()
        elif key == 3:
            return Phonemes.ipa_es_vowels.copy()
        elif key == 4:
            return Phonemes.ipa_nl_vowels.copy()
        elif key == 5:
            return Phonemes.ipa_de_vowels.copy()
        elif key == 6:
            return Phonemes.sampa_us_vowels.copy()
        elif key == 7:
            return Phonemes.sampa_uk_vowels.copy()
        elif key == 8:
            return Phonemes.sampa_fr_vowels.copy()
        elif key == 9:
            return Phonemes.sampa_es_vowels.copy()
        elif key == 10:
            return Phonemes.sampa_nl_vowels.copy()
        elif key == 11:
            return Phonemes.sampa_de_vowels.copy()
        elif key == 12:
            return Phonemes.klattese_vowels.copy()
        elif key == 13:
            if not Phonemes.custom_phonemes:
                self.get_custom_phonemes(fname[0])
            return Phonemes.custom_vowels.copy()
        else:
            raise Exception("Key is invalid")

    def get_custom_phonemes(self, fname):
        '''
        Parses phonetic system file into phoneme lists and returns true if both consonant and vowel lists are non-empty
        :param fname: filename of phonetic system file, with .csv extension.
        '''
        data = self.read_phonetic_system_file(fname)
        if not data:
            return False
        Phonemes.custom_cons = list(filter(lambda x: x, map(lambda x: x[0].strip(), data)))
        Phonemes.custom_vowels = list(filter(lambda x: x, map(lambda x: x[1].strip(), data)))
        Phonemes.custom_phonemes = Phonemes.custom_cons + Phonemes.custom_vowels
        if len(data[0]) > 2:
            Phonemes.custom_primary_stress = data[0][2]
        else:
            Phonemes.custom_primary_stress = None
        return Phonemes.custom_cons and Phonemes.custom_vowels

    def read_phonetic_system_file(self, fname):
        '''
        Reads phonetic system file and performs checking to ensure that number of columns is correct.
        :param fname: filename of phonetic system file, with .csv extension.
        '''
        data = read_csv(fname)
        if data[0][0][0] == '\ufeff':
            data[0][0] = data[0][0][1:]  # deletes '\ufeff' from beginning
        if len(data[0]) > 3:
            return False
        if len(data) > 2 and list(filter(lambda x: x, map(lambda x: x[2], data[1:]))):
            return False
        return data

    def get_list_of_phoneme_chars(self, key):
        '''
        Returns a list of all the characters in the phonemic inventory of the given key.
        '''
        char_list = []
        phoneme_list = self.get_phonemes_by_key(key)
        for phoneme in phoneme_list:
            for char in phoneme:
                if char not in char_list:
                    char_list.append(char)
        return char_list
