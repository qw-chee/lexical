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

def ccoeff(neighbours, sub_only=False):
    '''
    Computes the C coefficient based only on neighbours with edit distance = 1.
    :param neighbours: a list of tokenised words
    :param sub_only: if True, compute distance as number of substitutions, else by Levenstein distance.
    '''
    if len(neighbours) <= 1:
        return "NULL"
    num_edges = 0
    # count number of connections based on edit distance or num_substitutions = 1
    for w1 in neighbours:
        for w2 in neighbours:
            if w1 == w2:
                continue
            elif abs(len(w1) - len(w2)) > 1:
                continue
            if sub_only:
                ld = num_substitutions(w1, w2)
            else:
                ld = editdistance.eval(w1, w2)
            if ld == 1:
                num_edges += 1
    # divide by 2 since each edge was counted twice
    num_edges /= 2
    num_nodes = len(neighbours)
    # total possible number of edges in a complete graph:
    poss_edges = (num_nodes * (num_nodes - 1)) / 2
    if poss_edges == 0:
        return 0
    return num_edges / poss_edges

def phon_spread(word, neighbours):
    '''
    Computes both phonological and orthographic spread.
    :param word: tokenised word
    :param neighbours: a list of tokenised neighbours
    '''
    count = 0
    result = 0
    if len(neighbours) == 0:
        return 0
    while count < len(word):
        sub_neighbours = list(map(lambda x: x[:count] + x[count+1:], neighbours))
        if (word[:count] + word[count + 1:]) in sub_neighbours:
            result += 1
        count += 1
    return result

def unique_point(word, corpus):
    '''
    Given a word and a corpus, returns the uniqueness point i.e. index where word is unique in corpus
    :param word: string
    :param corpus: a dictionary mapping letters to a list of words beginning with that letter
    '''
    temp = []
    if word == "":
        return 0
    # filter corpus by first letter for efficiency
    corpus = corpus[word[0]] if word[0] in corpus else []
    if word in corpus:
        corpus = [x for x in corpus if x != word]
    point = 1
    for i in word:
        temp.append(i)
        corpus = list(filter(lambda x: x[:len(temp)] == temp, corpus))
        if len(corpus) != 0:
            point += 1
    return point
