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

from PyQt5.QtWidgets import QWidget, QMessageBox

class ErrorMessage(QMessageBox):
    def __init__(self, msg):
        super().__init__()
        self.setIcon(QMessageBox.Critical)
        self.setText(msg)
        self.setWindowTitle("Error")

class AbortMessage(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setIcon(QMessageBox.Question)
        self.setWindowTitle("Abort confirmation")
        self.setText("Are you sure you want to abort?")
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

class FinishMessage(QMessageBox):
    def __init__(self):
        super().__init__()
        self.setText("The execution is complete. The output file may now be opened.")
        self.setIcon(QMessageBox.Information)
        self.setWindowTitle("Complete")

class HelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Help")
