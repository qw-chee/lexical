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

from ReadWrite import read_csv
from Exceptions import *

class FileReader:
    '''
    Class for reading csv file input into lists.
    '''
    def __init__(self, max_input):
        self.max_input = max_input

    def read_file(self, filename):
        try:
            return read_csv(filename)
        except FileNotFoundError:
            raise FileNotFoundError
        except PermissionError:
            raise PermissionError
        except UnicodeDecodeError:
            raise UnicodeDecodeError

    def read_input(self, input_filename):
        '''
        Reads in csv input. Expects either 1 or 2 columns of words.
        :param input_filename: input filename without csv extension
        :return: a list of lists of size 1 or 2.
        '''
        if input_filename.text() == "" or input_filename.text() is None:
            raise NoFileSelectedException
        input_file = input_filename.text() + ".csv"
        self.input_data = self.read_file(input_file)
        try:
            self.clean_input(self.input_data)
        except EmptyCellException:
            raise EmptyCellException
        return self.input_data

    def read_corpus(self, corpus_filename, has_phon_column):
        '''
        Read in csv corpus file. Expects either 2 columns (orthographic word and frequency) or
        3 columns (orthographic word, phonological word and frequency).
        :param corpus_filename: corpus filename without csv extension.
        :param has_phon_column: True if corpus file has additional phonological column.
        :return: a list of lists of size 3. Phonological column is padded with empty string.
        '''
        if corpus_filename.text() == "" or corpus_filename.text() is None:
            raise NoFileSelectedException
        corpus_file = corpus_filename.text() + ".csv"
        self.corpus = self.read_file(corpus_file)
        try:
            if has_phon_column:
                self.clean_corpus_orth_and_phon(self.corpus)
            else:
                self.clean_corpus_orth_only(self.corpus)
                self.corpus = list(map(lambda row: [row[0], "", row[1]], self.corpus))
        except EmptyCellException:
            raise EmptyCellException
        except WrongCorpusInputException:
            raise WrongCorpusInputException
        return self.corpus

    def get_words(self, col):
        '''
        Returns the input words in the specified column in a list.
        '''
        words = []
        count = 1
        if col == 1 and len(self.input_data[0]) < 2:
            return words
        for row in self.input_data:
            if count > self.max_input:
                break
            word = row[col].strip()
            if word != "":
                words.append(word)
            count += 1
        return words

    def get_orth_words(self):
        orth_words = self.get_words(col=0)
        if orth_words is None:
            return []
        else:
            orth_words = list(map(lambda word: word.lower(), orth_words))
            return orth_words

    def get_phon_words(self, input_is_phon_only=False):
        col = 0 if input_is_phon_only else 1
        phon_words = self.get_words(col=col)
        if phon_words is None:
            return []
        else:
            return phon_words

    def get_pg_words(self, num_words, orth_words, phon_words):
        pg_words = []
        if orth_words and phon_words:
            for w in range(num_words):
                pg_word = (orth_words[w], phon_words[w])
                pg_words.append(pg_word)
        return pg_words

    def clean_input(self, input):
        '''
        Verify input.
        Ensures that there are no stray white spaces in input and deletes '\ufeff' from beginning
        Ensures that no cells in input are empty, if there are empty cells, raises EmptyCellException
        '''
        if input[0][0][0] == '\ufeff':
            input[0][0] = input[0][0][1:] # deletes '\ufeff' from beginning
        for row in input:
            for col in range(len(row)):
                if not row[col]:
                    raise EmptyCellException
                row[col] = row[col].strip()

    def clean_corpus_orth_and_phon(self, corpus):
        '''
        Verify input if corpus file has 3 columns including orthographic and phonological columns.
        Ensures that there are no stray white spaces in corpus and deletes '\ufeff' from beginning
        Ensures that no cells in input are empty, if there are empty cells, raises EmptyCellException
        Converts all frequencies into floats and raises CorpusFreqNotFloatException if non-number is found.
        '''
        if corpus[0][0][0] == '\ufeff':
            corpus[0][0] = corpus[0][0][1:] # deletes '\ufeff' from beginning
        if min(list(map(lambda row: len(row), corpus))) != 3:
            raise WrongCorpusInputException
        for row in corpus:
            for col in range(3):
                row[col] = row[col].strip()
                if not row[col]:
                    if self.row_is_empty(row):
                        continue
                    else:
                        raise EmptyCellException
                if col == 0:
                    row[col] = row[col].lower()
                if col == 2:
                    try:
                        row[col] = float(row[col])
                    except ValueError:
                        raise CorpusFreqNotFloatException

    def clean_corpus_orth_only(self, corpus):
        '''
        Verify input if corpus file has 2 columns with only orthographic column.
        Ensures that there are no stray white spaces in corpus and deletes '\ufeff' from beginning
        Ensures that no cells in input are empty, if there are empty cells, raises EmptyCellException
        Converts all frequencies into floats and raises CorpusFreqNotFloatException if non-number is found.
        '''
        if corpus[0][0][0] == '\ufeff':
            corpus[0][0] = corpus[0][0][1:] # deletes '\ufeff' from beginning
        if min(list(map(lambda row: len(row), corpus))) != 2:
            raise WrongCorpusInputException
        for row in corpus:
            for col in range(2):
                row[col] = row[col].strip()
                if not row[col]:
                    if self.row_is_empty(row):
                        continue
                    else:
                        raise EmptyCellException
                if col == 0:
                    row[col] = row[col].lower()
                if col == 1:
                    try:
                        row[col] = float(row[col])
                    except ValueError:
                        raise CorpusFreqNotFloatException

    def row_is_empty(self, row):
        for el in row:
            if el != "":
                return False
        return True
