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

import editdistance
import math
import heapq

def num_substitutions(word1, word2):
    '''
    Compares two words and returns the number of differences in their letters
    Returns 0 if the words are of differing length
    '''
    if len(word1) != len(word2):
        return 0
    result = 0
    for i in range(0, len(word1)):
        if word1[i] != word2[i]:
            result += 1
    return result

class Neighbours:
    '''
    Class for computing neighbourhood metrics including neighbourhood density, frequency, PLD20/OLD20.
    '''
    def __init__(self, freq_dic):
        self.freq_dic = freq_dic

    def find_neighbours(self, word, corpus, sub_only):
        '''
        If sub_only is true, then a neighbour is defined by substitutions only
        If it is false, a neighbour is defined by substitution, addition and deletion
        :param word: tokenised word as a list.
        :param corpus: dictionary mapping word as string to tokenised word as list.
        '''
        if type(word) != list:
            raise ValueError("Word is not a tokenised list")
        ld_one = []
        for w in corpus:
            if sub_only:
                ld = num_substitutions(word, corpus[w])
            else:
                if abs(len(corpus[w]) - len(word)) > 1:
                    continue
                ld = editdistance.eval(word, corpus[w])
            if ld == 1:
                ld_one.append(w)
        return ld_one

    def find_position_neighbours(self, word, corpus):
        '''
        Returns a list with number of entries = len(word) and each entry being the number of neighbours at that position.
        :param word: tokenised word.
        :param corpus: dictionary mapping word as string to tokenised word as list.
        '''
        result = [0 for i in range(len(word))]
        for w in corpus:
            w = corpus[w]
            if len(w) != len(word):
                continue
            for idx in range(len(w)):
                if w[:idx] == word[:idx] and w[idx+1:] == word[idx+1:] and w[idx] != word[idx]:
                    result[idx] += 1
        return result

    def n_density(self, neighbours):
        '''
        Returns the neighbourhood density given a list of neighbours.
        '''
        return len(neighbours)

    def n_freq(self, neighbours):
        '''
        Returns the neighbourhood frequency given a list of neighbours using the frequency dictionary.
        '''
        result = []
        if "" in neighbours:
            neighbours.remove("")
        for n in neighbours:
            try:
                result.append(float(self.freq_dic[n]))
            except:
                raise Exception("Neighbours: " + n + " is not in the freq dic")
        return result

    def n_freq_mean(self, n_freq_vals):
        '''
        Returns the mean of the neighbourhood frequency values.
        '''
        if sum(n_freq_vals) == 0:
            return "NULL"
        else:
            return sum(n_freq_vals) / len(n_freq_vals)

    def n_freq_sd(self, n_freq_vals, *mean):
        '''
        Returns the standard deviation of the neighbourhood frequency values.
        '''
        if mean:
            mean = mean[0]
        else:
            mean = self.n_freq_mean(n_freq_vals)
        if mean == "NULL":
            return "NULL"
        sum_of_sq_diff = 0
        for i in n_freq_vals:
            sum_of_sq_diff += (i - mean) ** 2
        if len(n_freq_vals) <= 1:
            return "NULL"
        sd = math.sqrt(sum_of_sq_diff / (len(n_freq_vals) - 1))
        return sd

    def find_PLD_20(self, word, corpus, sub_only):
        '''
        Returns PLD20/OLD20 information in thee form [list of neighbours, mean LD, standard deviation of LD].
        :param word: tokenised word.
        :param corpus: dictionary mapping word as string to tokenised word as list.
        :param sub_only: if True, compute distance as number of substitutions, else by Levenstein distance.
        '''
        word_ld_pairs = []
        for w in corpus:
            if sub_only:
                ld = num_substitutions(word, corpus[w])
            else:
                ld = editdistance.eval(word, corpus[w])
            if ld != 0:
                word_ld_pairs.append((w, ld))
        twenty_word_ld_pairs = heapq.nsmallest(20, word_ld_pairs, key=lambda x: x[1])
        cutoff_ld = max(twenty_word_ld_pairs, key=lambda x: x[1])[1]
        additional_neighbours = list(filter(lambda x: x[1] == cutoff_ld, word_ld_pairs))
        neighbours = list(set(twenty_word_ld_pairs + additional_neighbours))
        neighbours.sort(key=lambda x: x[1])
        LDs = list(map(lambda x: x[1], twenty_word_ld_pairs))
        mean = self.n_freq_mean(LDs)
        stdev = self.n_freq_sd(LDs, mean)
        return [neighbours, mean, stdev]
