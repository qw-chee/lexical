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

class WordEntry:
    '''
    Class which contains the data for each processed word.
    Boolean flags signal whether word entry already has different types of neighbours.
    self.output contains the output list of strings to be printed to output.
    '''
    def __init__(self):
        self.orth_word = None
        self.orth_tokenised = None
        self.phon_word = None
        self.phon_tokenised = None

        self.phon_neighbours_sub = None
        self.phon_neighbours_sub_spelling = None
        self.phon_neighbours_sad = None
        self.phon_neighbours_sad_spelling = None

        self.orth_neighbours_sub = None
        self.orth_neighbours_sub_ipa = None
        self.orth_neighbours_sad = None
        self.orth_neighbours_sad_ipa = None

        self.pg_orth_neighbours_sub = None
        self.pg_phon_neighbours_sub = None
        self.pg_orth_neighbours_sad = None
        self.pg_phon_neighbours_sad = None

        self.PLD20_neighbours = []
        self.OLD_neighbours = []
        self.output = []

        self.orth_is_printed = False
        self.phon_is_printed = False

    def get_pg_word(self):
        return (self.phon_word, self.orth_word)

    def get_pg_word_tokenised(self):
        return (self.orth_tokenised, self.phon_tokenised)

    def init_orth(self, word, tokenised, print_init):
        if self.orth_is_printed:
            return
        self.orth_word = word
        self.orth_tokenised = tokenised
        if print_init:
            self.output.append(word)
        self.orth_is_printed = True

    def init_phon(self, word, tokenised, print_init):
        if self.phon_is_printed:
            return
        self.phon_word = word
        self.phon_tokenised = tokenised
        if print_init:
            self.output.append(word)
        self.phon_is_printed = True

    def init_pg(self, orth_word, phon_word):
        if not self.orth_is_printed:
            self.output.append(orth_word)
        if not self.phon_is_printed:
            self.output.append(phon_word)

    def append(self, data):
        self.output.append(data)

    def add(self, data):
        self.output += data

    def set_phon_neighbours(self, neighbours, neighbours_with_spelling, sub_only):
        if sub_only:
            self.phon_neighbours_sub = neighbours
            self.phon_neighbours_sub_spelling = neighbours_with_spelling
        else:
            self.phon_neighbours_sad = neighbours
            self.phon_neighbours_sad_spelling = neighbours_with_spelling

    def print_phon_neighbours(self, sub_only):
        if sub_only:
            neighbours = self.phon_neighbours_sub
            neighbours_spelling = self.phon_neighbours_sub_spelling
        else:
            neighbours = self.phon_neighbours_sad
            neighbours_spelling = self.phon_neighbours_sad_spelling

        self.output.append(self.print_neighbours(neighbours_spelling))
        self.output.append(self.print_neighbours(neighbours))

    def set_orth_neighbours(self, neighbours, neighbours_with_ipa, sub_only):
        if sub_only:
            self.orth_neighbours_sub = neighbours
            self.orth_neighbours_sub_ipa = neighbours_with_ipa
        else:
            self.orth_neighbours_sad = neighbours
            self.orth_neighbours_sad_ipa = neighbours_with_ipa

    def print_orth_neighbours(self, sub_only):
        if sub_only:
            self.output.append(self.print_neighbours(self.orth_neighbours_sub))
        else:
            self.output.append(self.print_neighbours(self.orth_neighbours_sad))

    def add_PLD20_neighbours(self, neighbours):
        self.PLD20_neighbours = neighbours

    def add_OLD20_neighbours(self, neighbours):
        self.OLD_neighbours = neighbours

    def set_pg_phon_neighbours(self, neighbours, sub_only):
        if sub_only:
            self.pg_phon_neighbours_sub = neighbours
        else:
            self.pg_phon_neighbours_sad = neighbours

    def set_pg_orth_neighbours(self, neighbours, sub_only):
        if sub_only:
            self.pg_orth_neighbours_sub = neighbours
        else:
            self.pg_orth_neighbours_sad = neighbours

    def print_pg_phon_neighbours(self, sub_only):
        if sub_only:
            self.output.append(self.print_neighbours(self.pg_phon_neighbours_sub))
        else:
            self.output.append(self.print_neighbours(self.pg_phon_neighbours_sad))

    def print_pg_orth_neighbours(self, sub_only):
        if sub_only:
            self.output.append(self.print_neighbours(self.pg_orth_neighbours_sub))
        else:
            self.output.append(self.print_neighbours(self.pg_orth_neighbours_sad))

    def get_pg_neighbours(self, spelling, sub_only):
        if sub_only:
            if spelling:
                return self.pg_orth_neighbours_sub
            else:
                return self.pg_phon_neighbours_sub
        else:
            if spelling:
                return self.pg_orth_neighbours_sad
            else:
                return self.pg_phon_neighbours_sad

    def print_neighbours(self, neighbours):
        if not neighbours:
            return "NULL"
        string = "["
        for n in neighbours:
            string += n
            string += ", "
        string = string[:-2] + "]"
        return string

    def print(self):
        return self.output
