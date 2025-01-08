'''
LexiCAL is a calculator for psycholinguistic variables.
Copyright (C) 2019 Chee, Q.W., Chow, K.J., Goh, W.D., & Yap, M.J.; National University of Singapore.

LexiCAL is free software: you can redistribute it and/or modify
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

'''
Only first three functions are used in LexiCAL, the last two are from an older version.
The words passed into these functions should be tokenised.
The term "biphone" is used but the same functions are also used for computing bigram metrics.
'''

def get_biphones(word):
    '''
    Takes in a tokenised word and returns the biphones.
    '''
    lst = []
    for i in range(len(word)-1):
        new = word[i] + word[i+1]
        lst.append(new)
    return lst

def get_bpprob_base(corpus):
    '''
    Takes in a dictionary mapping tokenised words to their frequency.
    Returns a nested dictionary of dictionaries, where each dictionary is for a
    different biphone position and maps biphone to their probability.
    '''
    dic = {}
    for word in corpus:
        biphones = get_biphones(word)
        for idx in range(len(biphones)):
            bp = biphones[idx]
            if idx not in dic:
                dic[idx] = {}
            if bp not in dic[idx]:
                dic[idx][bp] = 0
            dic[idx][bp] += corpus[word]

    base = {}
    for idx in dic:
        base[idx] = {}
        for bp in dic[idx]:
            if sum(list(dic[idx].values())) == 0:
                continue
            base[idx][bp] = dic[idx][bp] / sum(list(dic[idx].values()))
    return base

def get_biphone_prob(word, base):
    '''
    Takes in a tokenised word and the base computed by get_bpprob_base,
    returns the sum of the biphone probabilities at each position.
    '''
    biphones = get_biphones(word)
    if not biphones:
        return "NULL"
    result = []
    for idx in range(len(biphones)):
        bp = biphones[idx]
        if bp in base[idx]:
            result.append(base[idx][bp])
        else:
            result.append(0.0)
    biphone_prob_sum = sum(result)
    return biphone_prob_sum

def get_bpprob_base_simple(tokenised_words):
    dic = {}
    for word in tokenised_words:
        biphones = get_biphones(word)
        for bp in biphones:
            if bp not in dic:
                dic[bp] = 0
            dic[bp] += 1
    biphone_prob_dic = {}
    total = sum(list(dic.values()))
    for word in dic:
        biphone_prob_dic[word] = dic[word]/total
    return biphone_prob_dic

def get_biphone_prob_simple(word, base):
    lst = get_biphones(word)
    if not lst:
        return "NULL"
    result = []
    for i in lst:
        if i in base:
            result.append(base[i])
        else:
            result.append(0.0)
    biphone_prob_sum = sum(result)
    return biphone_prob_sum
