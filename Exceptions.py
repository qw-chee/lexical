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

class NoFileSelectedException(Exception):
    pass

class WrongCorpusInputException(Exception):
    pass

class EmptyCellException(Exception):
    pass

class CorpusFreqNotFloatException(Exception):
    pass

class TokeniseException(Exception):
    def __init__(self, word):
        super().__init__()
        self.word = word

class NoStressException(Exception):
    pass
