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

from Neighbours import *
from Metrics import Metrics
from OrthMetrics import OrthMetrics
from PhonMetrics import PhonMetrics
from Phonograph import *
from Tokeniser import Tokeniser
from Exceptions import TokeniseException

class PGMetrics(Metrics):
    def __init__(self, key, words, corpus, output):
        super().__init__(key, output, corpus)
        self.tokeniser = Tokeniser(key)
        self.orth_words = list(map(lambda x: x[0], words))
        self.phon_words = list(map(lambda x: x[1], words))
        for word_index in range(len(words)):
            word = words[word_index]
            orth_word = word[0]
            phon_word = word[1]
            self.output.init_pg_at_index(word_index, orth_word, phon_word)
        self.neighbour_calc = Neighbours(self.create_word_to_freq_dic(corpus))
        self.orth_to_phon_dic = self.create_phon_to_orth_dic(corpus)
        self.word_to_tokens_dic = None
        self.orth_metric = OrthMetrics(self.orth_words, self.corpus, self.output, print_init=False)
        self.phon_metric = PhonMetrics(self.key, self.phon_words, self.corpus, self.output, print_init=False)

    def set_word(self, word, output):
        '''
        Overwrites existing word and output to a single word entry
        '''
        self.output = output
        orth_word = word.orth
        phon_word = word.phon
        self.orth_words = [orth_word]
        self.phon_words = [phon_word]
        self.output.init_pg_at_index(0, orth_word, phon_word)
        self.orth_metric.set_word(orth_word, self.output)
        self.phon_metric.set_word(phon_word, self.output)

    def create_word_to_freq_dic(self, data):
        '''
        Returns a dictionary mapping orthographic words as string to frequency.
        '''
        freq_dic = {}
        for i in data:
            freq_dic[i[0]] = i[2]
        return freq_dic

    def create_phon_to_orth_dic(self, data):
        '''
        Returns a dictionary of orthographic word as key, phonological word as value.
        '''
        dic = {}
        for row in data:
            dic[row[0]] = row[1]
        return dic

    def create_word_to_tokens_dic(self, data):
        '''
        Returns a dictionary mapping (orth word, phon word) tuples to (tokenised orth, tokenised phon) tuples.
        '''
        corpus = {}
        for row in data:
            orth = row[0]
            phon = row[1]
            orth_tokenised = self.tokenise_orth(orth)
            phon_tokenised = self.tokenise_phon(phon)
            corpus[(orth, phon)] = (orth_tokenised, phon_tokenised)
        return corpus

    def tokenise_orth(self, word):
        return list(word)

    def tokenise_phon(self, word):
        try:
            return self.tokeniser.tokenise(word)
        except TokeniseException as e:
            raise e

    def find_pg_neighbours(self, sub_only=False):
        if sub_only:
            if self.output.has_pg_sub_neighbours:
                return
        else:
            if self.output.has_pg_sad_neighbours:
                return

        self.find_phon_neighbours(sub_only)
        self.find_orth_neighbours(sub_only)
        # get intersection of orth neighbours and spelling of phon neighbours
        for word_entry in self.output.word_entries:
            if sub_only:
                phon_neighbours = word_entry.phon_neighbours_sub
                orth_neighbours = word_entry.orth_neighbours_sub
            else:
                phon_neighbours = word_entry.phon_neighbours_sad
                orth_neighbours = word_entry.orth_neighbours_sad
            orth_pg_neighbours = self.get_intersection(orth_neighbours, phon_neighbours)

            phon_pg_neighbours = list(map(lambda w: self.orth_to_phon_dic[w], orth_pg_neighbours))
            word_entry.set_pg_phon_neighbours(phon_pg_neighbours, sub_only)
            word_entry.set_pg_orth_neighbours(orth_pg_neighbours, sub_only)

        if sub_only:
            self.output.has_pg_sub_neighbours = True
        else:
            self.output.has_pg_sad_neighbours = True

    def find_orth_neighbours(self, sub_only):
        '''
        Populates the orthographic neighbours if they have not yet been found.
        '''
        if sub_only:
            has_orth_neighbours = self.output.has_orth_sub_neighbours
        else:
            has_orth_neighbours = self.output.has_orth_sad_neighbours
        if not has_orth_neighbours:
            self.orth_metric.find_neighbours(sub_only)
            self.output = self.orth_metric.get_output()

    def find_phon_neighbours(self, sub_only):
        '''
        Populates the phonological neighbours if they have not yet been found.
        '''
        if sub_only:
            has_phon_neighbours = self.output.has_phon_sub_neighbours
        else:
            has_phon_neighbours = self.output.has_phon_sad_neighbours
        if not has_phon_neighbours:
            self.phon_metric.find_neighbours(sub_only)
            self.output = self.phon_metric.get_output()

    def get_intersection(self, orth_words, phon_words):
        result = []
        for w in orth_words:
            if self.orth_to_phon_dic[w] in phon_words:
                result.append(w)
        return result

    def n_density(self, sub_only=False):
        for word_entry in self.output.word_entries:
            neighbours = word_entry.get_pg_neighbours(True, sub_only)
            word_entry.append(self.neighbour_calc.n_density(neighbours))
            word_entry.print_pg_orth_neighbours(sub_only)
            word_entry.print_pg_phon_neighbours(sub_only)

    def n_freq(self, sub_only=False):
        for word_entry in self.output.word_entries:
            neighbours = word_entry.get_pg_neighbours(True, sub_only)
            result = self.neighbour_calc.n_freq(neighbours)
            mean = self.neighbour_calc.n_freq_mean(result)
            sd = self.neighbour_calc.n_freq_sd(result)
            word_entry.add([mean, sd])

    def get_tokenised_pg_neighbour_tuple(self, word_entry, sub_only):
        '''
        Returns list of phonographic neighbours where each entry is a tuple of the form (tokenised_orth, tokenised_phon)
        '''
        orth_neighbours = list(map(lambda w: self.tokenise_orth(w), word_entry.get_pg_neighbours(True, sub_only)))
        phon_neighbours = list(map(lambda w: self.tokenise_phon(w), word_entry.get_pg_neighbours(False, sub_only)))
        return list(zip(orth_neighbours, phon_neighbours))

    def ccoeff(self):
        self.find_pg_neighbours(sub_only=False)
        for word_entry in self.output.word_entries:
            neighbours = self.get_tokenised_pg_neighbour_tuple(word_entry, False)
            result = ccoeff_pg(neighbours)
            word_entry.append(result)

    def PGLD20(self):
        if not self.word_to_tokens_dic:
            self.word_to_tokens_dic = self.create_word_to_tokens_dic(self.corpus)
        for word_entry in self.output.word_entries:
            word = word_entry.get_pg_word_tokenised()
            result = find_PGLD_20(word, self.word_to_tokens_dic)
            word_entry.add(result)
