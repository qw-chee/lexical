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

import csv, io

def read_csv(fname):
    new = []
    with open(fname, encoding = 'utf-8-sig') as f:
        for row in csv.reader(f):
            new.append(row)
    return new

def write(result, output_name):
    ofile = io.open(output_name, 'w', newline='', encoding='utf-32')
    with ofile:
        writer = csv.writer(ofile, delimiter=",", quotechar="'")
        writer.writerows(result)
    ofile.close()