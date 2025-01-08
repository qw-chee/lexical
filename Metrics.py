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

class Metrics:
    '''
    Parent class for OrthMetrics, PhonMetrics and PGMetrics.
    Keys are defined in Phonemes.py, and are as follows:
    -1 : Orthographic
    0 : IPA US
    1 : IPA UK
    2 : IPA French
    3 : IPA Spanish
    4 : IPA Dutch
    5 : IPA German
    6 : SAMPA US
    7 : SAMPA UK
    8 : SAMPA French
    9 : SAMPA Spanish
    10 : SAMPA Dutch
    11 : SAMPA German
    12 : Klattese US
    13 : Custom Phonetic System
    '''
    def __init__(self, key, output, corpus):
        self.key = key
        self.output = output
        self.corpus = corpus

    def get_output(self):
        return self.output
