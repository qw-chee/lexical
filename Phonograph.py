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
import heapq
import math

def ccoeff_pg(neighbours):
    '''
    Computes the C coefficient based only on neighbours with both orthographgic and phonological edit distance = 1.
    :param neighbours: a list of tokenised words.
    '''
    num_edges = 0
    if len(neighbours) <= 1:
        return "NULL"
    # count number of connections based on edit distance or substitutions = 1
    for w1 in neighbours:
        for w2 in neighbours:
            if w1 == w2:
                continue
            elif abs(len(w1[0]) - len(w2[0])) > 1:
                continue
            elif abs(len(w1[1]) - len(w2[1])) > 1:
                continue
            else:
                ld_orth = editdistance.eval(w1[0], w2[0])
                ld_phon = editdistance.eval(w1[1], w2[1])
            if ld_orth == 1 and ld_phon == 1:
                num_edges += 1
    # divide by 2 since each edge was counted twice
    num_edges /= 2
    num_nodes = len(neighbours)
    # total possible number of edges in a complete graph:
    poss_edges = (num_nodes * (num_nodes - 1)) / 2
    if poss_edges == 0:
        return 0
    return num_edges / poss_edges

def get_mean(n_freq_vals):
    if sum(n_freq_vals) == 0:
        return 0
    else:
        return sum(n_freq_vals) / len(n_freq_vals)

def get_sd(n_freq_vals, *mean):
    if mean:
        mean = mean[0]
    else:
        mean = get_mean(n_freq_vals)
    sum_of_sq_diff = 0
    for i in n_freq_vals:
        sum_of_sq_diff += (i - mean) ** 2
    if len(n_freq_vals) <= 0:
        return 0
    sd = math.sqrt(sum_of_sq_diff / (len(n_freq_vals) - 1))
    return sd

def find_PGLD_20(word, corpus):
    '''
    PGLD20 is no longer exposed on the UI.
    Returns PGLD20, the LD20 for phonographic words. LD for phonological and orthographic words must be identical.
    :param word: (tokenised orth, tokenised phon) tuple
    :param corpus: corpus is a dictionary of (orth, phon) : (orth_tokenised, phon_tokenised) key value mappings
    '''
    word_ld_pairs = []
    for w in corpus:
        orth_ld = editdistance.eval(word[0], corpus[w][0])
        phon_ld = editdistance.eval(word[1], corpus[w][1])
        if phon_ld != orth_ld:
            continue
        if phon_ld != 0:
            word_ld_pairs.append((w, phon_ld))
    twenty_word_ld_pairs = heapq.nsmallest(20, word_ld_pairs, key=lambda x: x[1])
    cutoff_ld = max(twenty_word_ld_pairs, key=lambda x: x[1])
    additional_neighbours = list(filter(lambda x: x[1] == cutoff_ld, word_ld_pairs))
    neighbours = list(set(twenty_word_ld_pairs + additional_neighbours))
    neighbours.sort(key=lambda x: x[1])
    neighbours = list(map(lambda x: (x[0][0], x[1]), neighbours))
    LDs = list(map(lambda x: x[1], neighbours))
    mean = get_mean(LDs)
    stdev = get_sd(LDs, mean)
    return [neighbours, mean, stdev]
