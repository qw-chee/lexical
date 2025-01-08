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

from PhonMetrics import PhonMetrics
from OrthMetrics import OrthMetrics
from PGMetrics import PGMetrics
from Output import Output
from ReadWrite import *
from Phonemes import Phonemes
import time

'''
Tests for OrthMetrics, PhonMetrics and PGMetrics independent of UI.
'''

def orth_test(words, file, output):
    m = OrthMetrics(words, file, output)
    m.num_letters()
    m.bigram_prob()
    m.find_neighbours()
    m.find_position_neighbours()
    m.n_density()
    m.n_freq()
    m.ccoeff()
    m.orth_spread()
    m.unique_point()
    m.OLD20()
    result = m.get_output().print()
    write(result, "output.csv")

def phon_test(words, key, file, output):
    m = PhonMetrics(key, words, file, output)
    m.unique_point()
    m.n_phon()
    m.num_syllables()
    m.biphone_prob()
    m.find_neighbours()
    m.find_position_neighbours()
    m.n_density()
    m.n_freq()
    m.ccoeff()
    m.phon_spread()
    m.PLD20()
    result = m.get_output().print()
    write(result, "output.csv")

def pg_test(words, key, file, output):
    pg = PGMetrics(key, words, file, output)
    pg.find_pg_neighbours()
    pg.n_density()
    pg.n_freq()
    pg.ccoeff()
    pg.PGLD20()
    result = pg.get_output().print()
    write(result, "output.csv")

def stress_test(words, key, file, output):
    m = PhonMetrics(key, words, file, output, print_init=False)
    m.primary_stress_code()
    m.stress_typicality()
    result = m.get_output().print()
    write(result, "output.csv")

def test(key, input, corpus):
    t0 = time.time()
    file = read_csv(corpus)[1:]
    orth_words = list(map(lambda x: x[0], read_csv(input)))
    output = Output(len(orth_words))
    orth_test(orth_words, file, output)
    phon_words = list(map(lambda x: x[1], read_csv(input)))
    phon_test(phon_words, key, file, output)
    pg_words = list(zip(orth_words, phon_words))
    pg_test(pg_words, key, file, output)
    if key != Phonemes.KLATTESE_KEY:
        stress_test(phon_words, key, file, output)
    t1 = time.time()
    print(t1-t0)


''' Sample test commands '''
# test(1, "Sample Data/input.csv", "Sample Data/ELP Final (UK).csv")
# test(1, "Sample Data/UK Input.csv", "Sample Data/ELP Final (UK).csv")
# test(0, "Sample Data/US Input.csv", "Sample Data/ELP Final (US).csv")
# test(12, "Sample Data/Klattese Input.csv", "Sample Data/Klattese Corpus.csv")
# test(6, "Sample Data/SAMPA Input.csv", "Sample Data/SAMPA Corpus.csv")
# Phonemes().get_custom_phonemes("Sample Data/Test Phonetic System.csv")
# test(13, "Sample Data/SAMPA Input.csv", "Sample Data/SAMPA Corpus.csv")
