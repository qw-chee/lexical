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

from WordEntry import WordEntry

class Output:
    '''
    This is an output class which stores each word entry/row of csv output as a separate WordEntry object.
    The class also stores the headers for the csv output,
    and boolean attributes indicating if different neighbour types have been initialised.
    '''
    def __init__(self, num_words):
        self.word_entries = [WordEntry() for i in range(num_words)]
        self.has_phon_sub_neighbours = False
        self.has_orth_sub_neighbours = False
        self.has_phon_sad_neighbours = False
        self.has_orth_sad_neighbours = False
        self.has_pg_sad_neighbours = False
        self.has_pg_sub_neighbours = False
        self.orth_word_is_init = False
        self.phon_word_is_init = False
        self.header = []

    def init_word_at_index(self, index, word, tokenise, isOrth, print_init):
        if isOrth:
            self.word_entries[index].init_orth(word, tokenise, print_init)
            self.orth_word_is_init = True
        else:
            self.word_entries[index].init_phon(word, tokenise, print_init)
            self.phon_word_is_init = True

    def init_pg_at_index(self, index, orth_word, phon_word):
        self.word_entries[index].init_pg(orth_word, phon_word)

    def append_header(self, *title):
        for t in title:
            self.header.append(t)

    def init_header(self, isOrth):
        if isOrth:
            self.append_header("Item (Orthography)")
        else:
            self.append_header("Item (Phonology)")

    def print(self):
        return [self.header] + [word_entry.print() for word_entry in self.word_entries]

    def add_word_entry(self, word):
        self.word_entries.append(word)