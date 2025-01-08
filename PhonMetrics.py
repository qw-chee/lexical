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
from Stress import Stress
from Neighbours import Neighbours
from Tokeniser import Tokeniser
from Exceptions import TokeniseException

class PhonMetrics(Metrics):
    def __init__(self, key, words, corpus, output, print_init=True):
        words = list(filter(lambda x: x != "", words))
        super().__init__(key, output, corpus)
        self.tokeniser = Tokeniser(key)
        self.print_init = print_init
        for word_index in range(len(words)):
            word = words[word_index]
            tokenised = self.tokenise(word)
            self.output.init_word_at_index(word_index, word, tokenised, isOrth=False, print_init=print_init)

        freq_dic = self.create_word_to_freq_dic(corpus)
        self.word_to_tokens_dic = self.create_word_to_tokens_dic(freq_dic)
        self.neighbour_calc = Neighbours(freq_dic)
        self.freq_dic = self.create_tokens_to_freq_dic(self.word_to_tokens_dic, freq_dic)
        self.phon_to_orth_dic = self.create_phon_to_orth_dic(corpus)
        self.biphone_base = None
        self.stress_code_calc = None
        self.stress_typ_calc = None
        self.unique_pt_dic = None
        self.ipa_words = list(map(lambda w: w[1], self.corpus))

    def set_word(self, word, output):
        self.output = output
        tokenised = self.tokenise(word)
        self.output.init_word_at_index(0, word, tokenised, isOrth=False, print_init=self.print_init)

    def create_word_to_freq_dic(self, data):
        '''
        Returns a dictionary mapping phonological words as strings to frequency.
        '''
        freq_dic = {}
        for row in data:
            word = row[1]
            if word not in freq_dic:
                freq_dic[word] = 0
            freq_dic[word] += float(row[2])
        return freq_dic

    def create_phon_to_orth_dic(self, data):
        '''
        Returns a dictionary mapping phonological words to orthographic words (untokenised).
        '''
        dic = {}
        for row in data:
            if row[1] in dic:
                dic[row[1]] += "/" + row[0]
            else:
                dic[row[1]] = row[0]
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
        corpus = list(self.word_to_tokens_dic.values())  # list of tokenised words
        uniq_pt_dic = {}
        for word in corpus:
            if word == []:
                continue
            if word[0] not in uniq_pt_dic:
                uniq_pt_dic[word[0]] = []
            uniq_pt_dic[word[0]].append(word)
        return uniq_pt_dic

    def tokenise(self, word):
        try:
            return self.tokeniser.tokenise(word)
        except TokeniseException as e:
            raise e

    ####
    # Surface metrics
    ####

    def primary_stress_code(self):
        if not self.stress_code_calc:
            self.stress_code_calc = Stress(self.key)
        for word_entry in self.output.word_entries:
            word_entry.append(self.stress_code_calc.get_primary_stress_code(word_entry.phon_word))

    def secondary_stress_code(self):
        if not self.stress_code_calc:
            self.stress_code_calc = Stress(self.key)
        for word_entry in self.output.word_entries:
            word_entry.append(self.stress_code_calc.get_secondary_stress_code(word_entry.phon_word))

    def stress_typicality(self):
        if not self.stress_typ_calc:
            self.stress_typ_calc = Stress(self.key, self.ipa_words)
        for word_entry in self.output.word_entries:
            word = word_entry.phon_word
            word_entry.append(self.stress_typ_calc.get_stress_typicality(word))

    ####
    # Length
    ####

    def n_phon(self):
        for word_entry in self.output.word_entries:
            word_entry.append(len(word_entry.phon_tokenised))

    def num_syllables(self):
        for word_entry in self.output.word_entries:
            word = word_entry.phon_word
            word_entry.append(self.tokeniser.get_num_syllables(word))

    ####
    # Neighbourhood metrics
    ####

    def find_neighbours(self, sub_only=False):
        if sub_only:
            if self.output.has_phon_sub_neighbours:
                return
        else:
            if self.output.has_phon_sad_neighbours:
                return

        for word_entry in self.output.word_entries:
            word = word_entry.phon_tokenised
            neighbours = self.neighbour_calc.find_neighbours(word, self.word_to_tokens_dic, sub_only)
            neighbours_in_spelling = self.get_neighbours_in_spelling(neighbours)
            word_entry.set_phon_neighbours(neighbours, neighbours_in_spelling, sub_only)

        if sub_only:
            self.output.has_phon_sub_neighbours = True
        else:
            self.output.has_phon_sad_neighbours = True

    def find_position_neighbours(self):
        for word_entry in self.output.word_entries:
            word = word_entry.phon_tokenised
            result = self.neighbour_calc.find_position_neighbours(word, self.word_to_tokens_dic)
            word_entry.append(result)

    def get_neighbours_in_spelling(self, neighbours):
        result = []
        for word in neighbours:
            result.append(self.phon_to_orth_dic[word])
        return result

    def n_density(self, sub_only=False):
        for word_entry in self.output.word_entries:
            if sub_only:
                neighbours = word_entry.phon_neighbours_sub
            else:
                neighbours = word_entry.phon_neighbours_sad
            word_entry.append(self.neighbour_calc.n_density(neighbours))
            word_entry.print_phon_neighbours(sub_only)

    def n_freq(self, sub_only=False):
        for word_entry in self.output.word_entries:
            if sub_only:
                neighbours = word_entry.phon_neighbours_sub
            else:
                neighbours = word_entry.phon_neighbours_sad
            result = self.neighbour_calc.n_freq(neighbours)
            mean = self.neighbour_calc.n_freq_mean(result)
            sd = self.neighbour_calc.n_freq_sd(result)
            word_entry.add([mean, sd])

    def PLD20(self, sub_only=False):
        for word_entry in self.output.word_entries:
            word = word_entry.phon_tokenised
            result = self.neighbour_calc.find_PLD_20(word, self.word_to_tokens_dic, sub_only)

            result[0] = list(map(lambda x: (self.phon_to_orth_dic[x[0]], x[1]), result[0]))
            word_entry.add(result[1:])
            neighbours = result[0]
            word_entry.add_PLD20_neighbours(neighbours)

    ####
    # Others
    ####

    def ccoeff(self):
        for word_entry in self.output.word_entries:
            if self.output.has_phon_sad_neighbours:
                neighbours = word_entry.phon_neighbours_sad
            else:
                word = word_entry.phon_tokenised
                neighbours = self.neighbour_calc.find_neighbours(word, self.word_to_tokens_dic, False)
            neighbours = list(map(lambda x: self.tokenise(x), neighbours))
            result = Ccoeff.ccoeff(neighbours, False)
            word_entry.append(result)

    def phon_spread(self):
        for word_entry in self.output.word_entries:
            word = word_entry.phon_tokenised
            if self.output.has_phon_sub_neighbours:
                neighbours = word_entry.phon_neighbours_sub
            else:
                neighbours = self.neighbour_calc.find_neighbours(word, self.word_to_tokens_dic, True)
            neighbours = list(map(lambda x: self.tokenise(x), neighbours))
            result = Ccoeff.phon_spread(word, neighbours)
            word_entry.append(result)

    def unique_point(self):
        if not self.unique_pt_dic:
            self.unique_pt_dic = self.create_uniq_pt_dic()
        for word_entry in self.output.word_entries:
            word = word_entry.phon_tokenised
            result = Ccoeff.unique_point(word, self.unique_pt_dic)
            word_entry.append(result)

    def biphone_prob(self):
        if not self.biphone_base:
            self.biphone_base = Biphones.get_bpprob_base(self.freq_dic)
        for word_entry in self.output.word_entries:
            word = word_entry.phon_tokenised
            word_entry.append(Biphones.get_biphone_prob(word, self.biphone_base))

