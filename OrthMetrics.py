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

from Metrics import Metrics
import Biphones
import Ccoeff
from Neighbours import Neighbours

class OrthMetrics(Metrics):
    def __init__(self, words, corpus, output, print_init=True):
        words = list(filter(lambda x: x != "", words))
        self.print_init = print_init
        super().__init__(-1, output, corpus)
        for word_index in range(len(words)):
            word = words[word_index]
            tokenised = self.tokenise(word)
            self.output.init_word_at_index(word_index, word, tokenised, isOrth=True, print_init=print_init)

        freq_dic = self.create_word_to_freq_dic(corpus)
        self.word_to_token_dic = self.create_word_to_tokens_dic(freq_dic)
        self.neighbour_calc = Neighbours(freq_dic)
        self.freq_dic = self.create_tokens_to_freq_dic(self.word_to_token_dic, freq_dic)
        self.orth_to_phon_dic = self.create_orth_to_phon_dic(corpus)
        self.bigram_base = None
        self.unique_pt_dic = None

    def set_word(self, word, output):
        self.output = output
        tokenised = self.tokenise(word)
        self.output.init_word_at_index(0, word, tokenised, isOrth=True, print_init=self.print_init)

    def create_word_to_freq_dic(self, data):
        '''
        Returns a dictionary mapping orthographic words as strings to frequency.
        '''
        freq_dic = {}
        for row in data:
            word = row[0]
            if word not in freq_dic:
                freq_dic[word] = 0
            freq_dic[word] += float(row[2])
        return freq_dic

    def create_orth_to_phon_dic(self, data):
        '''
        Returns a dictionary of orthographic word as key, phonological word as value.
        '''
        dic = {}
        for row in data:
            dic[row[0]] = row[1]
        return dic

    def create_word_to_tokens_dic(self, corpus):
        '''
        Returns a dictionary mapping words as strings to tokenised words as a list.
        '''
        new_corpus = {}
        for word in corpus:
            new_corpus[word] = self.tokenise(word)
        return new_corpus

    def create_tokens_to_freq_dic(self, words_to_tokens_dic, freq_dic):
        '''
        Returns a dictionary mapping tokenised words (tuple) to frequency.
        '''
        dic = {}
        for word in freq_dic:
            tokens = words_to_tokens_dic[word]
            dic[tuple(tokens)] = freq_dic[word]
        return dic

    def create_uniq_pt_dic(self):
        '''
        Returns a dictionary mapping the first phoneme/token of each word to the tokenised word.
        '''
        corpus = list(self.word_to_token_dic.values())  # list of tokenised words
        uniq_pt_dic = {}
        for word in corpus:
            if word == []:
                continue
            if word[0] not in uniq_pt_dic:
                uniq_pt_dic[word[0]] = []
            uniq_pt_dic[word[0]].append(word)
        return uniq_pt_dic

    def tokenise(self, word):
        return list(word)

    ####
    # Length
    ####

    def num_letters(self):
        for word_entry in self.output.word_entries:
            word_entry.append(len(word_entry.orth_tokenised))

    def quadratic_length(self):
        for word_entry in self.output.word_entries:
            length = len(word_entry.orth_tokenised) ** 2
            word_entry.append(length)

    ####
    # Neighbourhood metrics
    ####

    def find_neighbours(self, sub_only=False):
        if sub_only:
            if self.output.has_orth_sub_neighbours:
                return
        else:
            if self.output.has_orth_sad_neighbours:
                return

        for word_entry in self.output.word_entries:
            word = word_entry.orth_tokenised
            neighbours = self.neighbour_calc.find_neighbours(word, self.word_to_token_dic, sub_only)
            neighbours_in_ipa = self.get_neighbours_in_ipa(neighbours)
            word_entry.set_orth_neighbours(neighbours, neighbours_in_ipa, sub_only)

        if sub_only:
            self.output.has_orth_sub_neighbours = True
        else:
            self.output.has_orth_sad_neighbours = True

    def find_position_neighbours(self):
        for word_entry in self.output.word_entries:
            word = word_entry.orth_tokenised
            result = self.neighbour_calc.find_position_neighbours(word, self.word_to_token_dic)
            word_entry.append(result)

    def get_neighbours_in_ipa(self, neighbours):
        result = []
        for word in neighbours:
            result.append(self.orth_to_phon_dic[word])
        return result

    def n_density(self, sub_only=False):
        for word_entry in self.output.word_entries:
            if sub_only:
                neighbours = word_entry.orth_neighbours_sub
            else:
                neighbours = word_entry.orth_neighbours_sad
            word_entry.append(self.neighbour_calc.n_density(neighbours))
            word_entry.print_orth_neighbours(sub_only)

    def n_freq(self, sub_only=False):
        for word_entry in self.output.word_entries:
            if sub_only:
                neighbours = word_entry.orth_neighbours_sub
            else:
                neighbours = word_entry.orth_neighbours_sad
            result = self.neighbour_calc.n_freq(neighbours)
            mean = self.neighbour_calc.n_freq_mean(result)
            sd = self.neighbour_calc.n_freq_sd(result)
            word_entry.add([mean, sd])

    def OLD20(self, sub_only = False):
        for word_entry in self.output.word_entries:
            word = word_entry.orth_tokenised
            result = self.neighbour_calc.find_PLD_20(word, self.word_to_token_dic, sub_only)
            word_entry.add(result[1:])
            neighbours = result[0]
            word_entry.add_OLD20_neighbours(neighbours)

    ####
    # Others
    ####

    def ccoeff(self):
        for word_entry in self.output.word_entries:
            if self.output.has_orth_sad_neighbours:
                neighbours = word_entry.orth_neighbours_sad
            else:
                word = word_entry.orth_tokenised
                neighbours = self.neighbour_calc.find_neighbours(word, self.word_to_token_dic, False)
            neighbours = list(map(lambda x: self.tokenise(x), neighbours))
            result = Ccoeff.ccoeff(neighbours, False)
            word_entry.append(result)

    def orth_spread(self):
        for word_entry in self.output.word_entries:
            word = word_entry.orth_tokenised
            if self.output.has_orth_sub_neighbours:
                neighbours = word_entry.orth_neighbours_sub
            else:
                neighbours = self.neighbour_calc.find_neighbours(word, self.word_to_token_dic, True)
            neighbours = list(map(lambda x: self.tokenise(x), neighbours))
            result = Ccoeff.phon_spread(word, neighbours)
            word_entry.append(result)

    def unique_point(self):
        if not self.unique_pt_dic:
            self.unique_pt_dic = self.create_uniq_pt_dic()
        for word_entry in self.output.word_entries:
            word = word_entry.orth_tokenised
            result = Ccoeff.unique_point(word, self.unique_pt_dic)
            word_entry.append(result)

    def bigram_prob(self):
        if not self.bigram_base:
            self.bigram_base = Biphones.get_bpprob_base(self.freq_dic)
        for word_entry in self.output.word_entries:
            word = word_entry.orth_tokenised
            word_entry.append(Biphones.get_biphone_prob(word, self.bigram_base))
