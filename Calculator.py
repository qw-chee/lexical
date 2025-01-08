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

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot, QThreadPool
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QMessageBox
from UI_Calculator import Ui_LexiCAL
from ReadWrite import *
from ExecCalculator import ExecCalculator
from SelectedButtons import SelectedButtons
from Exceptions import *
from Phonemes import Phonemes
from FileReader import FileReader
from Messages import FinishMessage, AbortMessage, ErrorMessage

class CalculatorWindow(QtWidgets.QMainWindow, Ui_LexiCAL):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.buttons = [self.IPA, self.Klattese, self.SAMPA, self.other_system, self.num_letters, self.orth_n_dens,
                        self.orth_n_freq, self.OLD20, self.orth_c_coeff, self.orth_spread, self.orth_uniq_pt,
                        self.orth_bfreq, self.n_phon, self.num_syl, self.phon_n_dens, self.phon_n_freq,
                        self.phon_c_coeff, self.phon_uniq_pt, self.phon_spread, self.phon_bfreq, self.PLD20,
                        self.pg_n_dens, self.pg_n_freq, self.pg_c_coeff, self.p_stress_code,
                        self.stress_typ]
        self.sub_only_buttons = [self.orth_n_dens_sub, self.orth_n_freq_sub, self.phon_n_dens_sub,
                                 self.phon_n_freq_sub, self.pg_n_dens_sub, self.pg_n_freq_sub]
        self.sad_buttons = [self.orth_n_dens_sad, self.orth_n_freq_sad, self.phon_n_dens_sad, self.phon_n_freq_sad,
                            self.pg_n_dens_sad, self.pg_n_freq_sad]

        self.tabWidget.setCurrentIndex(0)
        self.configure_buttons()
        self.max_input = 50000
        self.file_reader = FileReader(self.max_input)
        self.startup_settings()
        self.show()

    def startup_settings(self):
        '''
        Set default startup settings for UI
        '''
        self.input_is_orth_only = False
        self.input_is_both_phon_and_orth = False
        self.orth_only_button.setChecked(True)
        self.set_orth_only()
        self.progress_bar.setValue(0)
        self.clear_buttons()
        self.other_system.setChecked(False)
        self.select_predefined_system.setChecked(True)
        self.other_phon_system.clear()
        self.predefined_systems.setEnabled(True)
        self.language.setCurrentIndex(0)
        self.IPA.setChecked(True)
        self.other_phon_system.clear()

    def configure_buttons(self):
        '''
        Configure links between buttons and triggers to functions
        '''
        self.submit_button.clicked.connect(self.run)
        self.default_button.clicked.connect(self.set_default_buttons)
        self.clear_button.clicked.connect(self.clear_all)
        self.abort_button.clicked.connect(self.abort)
        self.abort_button.setEnabled(False)
        self.input_browse_button.clicked.connect(self.open_input_file)
        self.corpus_browse_button.clicked.connect(self.open_corpus_file)

        self.language.addItems(["English (US)", "English (UK)", "French", "Spanish", "Dutch", "German"])
        self.language.currentIndexChanged.connect(self.enable_Klattese)
        self.IPA.clicked.connect(self.enable_surface_metrices)
        self.Klattese.clicked.connect(self.disable_surface_metrics)
        self.SAMPA.clicked.connect(self.enable_surface_metrices)
        self.other_system.clicked.connect(self.enable_other_system_browse)
        self.select_predefined_system.clicked.connect(self.enable_other_system_browse)
        self.enable_other_system_browse()
        self.phon_system_browse.clicked.connect(self.browse_phonetic_system)

        self.phon_n_dens.clicked.connect(self.allow_check_phon_n_dens)
        self.phon_n_freq.clicked.connect(self.allow_check_phon_n_freq)
        self.orth_n_dens.clicked.connect(self.allow_check_orth_n_dens)
        self.orth_n_freq.clicked.connect(self.allow_check_orth_n_freq)
        self.pg_n_dens.clicked.connect(self.allow_check_pg_n_dens)
        self.pg_n_freq.clicked.connect(self.allow_check_pg_n_freq)
        for button in self.sub_only_buttons:
            button.setChecked(False)
            button.setEnabled(False)
        for button in self.sad_buttons:
            button.setEnabled(False)

        self.orth_only_button.clicked.connect(self.set_orth_only)
        self.both_phon_and_orth_button.clicked.connect(self.set_both_phon_and_orth)

    def run(self):
        '''
        Main execution method. Load input and corpus file, run prechecks and ask user for output filename.
        If successful, create worker thread (ExecCalculator class) and start the thread.
        '''
        load_input_is_success = self.load_input_file()
        load_corpus_is_success = self.load_corpus_file()
        if not load_input_is_success or not load_corpus_is_success:
            return
        if not self.run_prechecks():
            return
        if not self.load_input_words():
            return
        if not self.specify_output_file():
            return

        if not self.init_worker():
            return
        self.threadpool = QThreadPool()
        self.threadpool.start(self.worker)
        self.submit_button.setEnabled(False)
        self.abort_button.setEnabled(True)

    def load_input_file(self):
        '''
        Read input file using the FileReader. Return False if unsuccessful.
        '''
        try:
            self.input_data = self.file_reader.read_input(self.input_filename)
            return True
        except (FileNotFoundError, OSError):
            self.return_error("The specified input file cannot be found in the directory.")
            return False
        except PermissionError:
            self.return_error("Unable to read input file. Please close the file if it is open.")
            return False
        except UnicodeDecodeError:
            self.return_error("Unable to read input file. Please check that it is saved in CSV format.")
            return False
        except NoFileSelectedException:
            self.return_error("No input file is selected. Please select an input file.")
            return False
        except EmptyCellException:
            self.return_error("There are empty cells in the input. Please check the input file.")
            return False

    def load_corpus_file(self):
        '''
        Read corpus file using FileReader. Return False if unsuccessful.
        '''
        try:
            self.corpus = self.file_reader.read_corpus(self.corpus_filename, self.input_is_both_phon_and_orth)
            return True
        except (FileNotFoundError, OSError):
            self.return_error("The specified corpus file was not found in the directory.")
            return False
        except PermissionError:
            self.return_error("Unable to read corpus file. Please close the file if it is open.")
            return False
        except UnicodeDecodeError:
            self.return_error("Unable to read corpus file. Please check that it is saved in CSV format.")
            return False
        except NoFileSelectedException:
            self.return_error("No corpus file is selected. Please select a corpus file.")
            return False
        except WrongCorpusInputException:
            self.return_error("The corpus file format is incorrect. Please ensure that the number of columns is correct.")
            return False
        except EmptyCellException:
            self.return_error("There are empty cells in the corpus. Please check the corpus file.")
            return False
        except CorpusFreqNotFloatException:
            self.return_error("Please ensure that only numbers are in the frequency column of the corpus file.")
            return False

    def load_input_words(self):
        '''
        Load words into lists of orthographic words, phonological words, and phonographic words. Only orthographic
        words are read if the input is orthography only.
        Perform checks to ensure selected metrics apply to the type of words. Return False if unsuccessful.
        '''
        self.orth_words = []
        self.phon_words = []
        self.pg_words = []
        self.num_words = 0

        if self.input_is_orth_only:
            self.orth_words = self.file_reader.get_orth_words()
            self.num_words = len(self.orth_words)
        elif self.input_is_both_phon_and_orth:
            self.orth_words = self.file_reader.get_orth_words()
            self.phon_words = self.file_reader.get_phon_words()
            self.num_words = max(len(self.orth_words), len(self.phon_words))
            self.pg_words = self.file_reader.get_pg_words(self.num_words, self.orth_words, self.phon_words)

        if not self.input_is_orth_only and self.no_phonetic_system_is_checked():
            self.return_error("No phonetic system is selected. Please select a phonetic system.")
            return False
        if not self.phon_words and self.selected_buttons.is_any_phon_metric_checked():
            self.return_error("Words (phonological) must not be empty for phonological metrics.")
            return False
        if not self.orth_words and self.selected_buttons.is_any_orth_metric_checked():
            self.return_error("Words (orthographic) must not be empty for orthographic metrics.")
            return False
        if not self.pg_words and self.selected_buttons.is_any_pg_metric_checked():
            self.return_error("Words (phonological) and Words (orthographic) must not be empty " +
                              "for phonographic metrics.")
            return False
        if not self.phon_words and self.selected_buttons.is_any_stress_metric_checked():
            self.return_error("Words (phonological) must not be empty for surface metrics.")
            return False

        return True

    def run_prechecks(self):
        '''
        Perform checks before running:
        1. Phonetic system file must be selected and valid if other phonetic system is selected.
        2. At least one metric must be selected.
        3. Transcription system must have a primary stress symbol for surface metrics.
        4. Corpus needs at least 20 unique items if OLD20 or PLD20 is selected.
        '''
        if self.other_system.isChecked():
            if self.other_phon_system.text() == "":
                self.return_error("No phonetic system file is selected. Please select a phonetic system file.")
                return False
            if not self.open_phonetic_system(self.other_phon_system.text() + ".csv"):
                return False

        self.selected_buttons = self.get_selected_buttons()
        if not self.selected_buttons.is_any_checked():
            self.return_error("No metrics have been selected.")
            return False

        if self.p_stress_code.isChecked() or self.stress_typ.isChecked():
            if self.get_transcription_system() == Phonemes.CUSTOM_KEY and Phonemes.custom_primary_stress is None:
                self.return_error("Please specify a stress mark in the phonetic system.")
                return False
            elif self.get_transcription_system() not in Phonemes.SAMPA_KEYS + Phonemes.IPA_KEYS + [Phonemes.CUSTOM_KEY]:
                self.return_error("The phonetic system does not support stress marking for surface metrics.")
                return False

        if (self.OLD20.isChecked() and len(list(set(map(lambda x: x[0], self.corpus)))) < 20) \
                or (self.PLD20.isChecked() and len(list(set(map(lambda x: x[1], self.corpus)))) < 20):
            self.return_error("The corpus needs at least 20 unique items if OLD20/PLD20 is selected.")
            return False
        return True

    def init_worker(self):
        '''
        Initialise a worker (ExecCalculator) with the corpus and input words. Return False if word cannot be
        tokenised, else connect signals to UI and return True.
        '''
        self.worker = ExecCalculator(self.corpus, self.selected_buttons, self.orth_words,
                                     self.phon_words, self.pg_words, self.num_words)
        try:
            self.worker.init()
        except TokeniseException as e:
            self.return_error("Unable to tokenise the string '" + e.word + "'.")
            return False

        self.worker.signals.num_words_processed.connect(self.get_slider_value)
        self.worker.signals.total_num_words.connect(self.set_max_value)
        self.worker.signals.completed_signal.connect(self.finished)
        return True

    @pyqtSlot(int)
    def get_slider_value(self, val):
        '''
        Slot takes in number of processed words to update the progress bar.
        '''
        self.progress_bar.setValue(val)

    @pyqtSlot(int)
    def set_max_value(self, val):
        '''
        Set the minimum and maximum value of the progress bar based on the number of words in input.
        '''
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(val)

    @pyqtSlot()
    def finished(self):
        '''
        If execution is not successful, return an error message. Else, save the execution output
        and return a finished message.
        '''
        if not self.worker.exec_is_success:
            self.return_error(self.worker.error_msg)
            self.progress_bar.setValue(0)
        else:
            self.final_output = self.worker.output
            self.save_output()
            self.progress_bar.setValue(self.worker.get_number_of_words())
            self.message_box = FinishMessage()
            self.message_box.show()
            self.message_box.buttonClicked.connect(self.startup_settings)
        self.submit_button.setEnabled(True)
        self.abort_button.setEnabled(False)

    def return_error(self, msg):
        '''
        Generate and display the error message.
        '''
        self.error_msg = ErrorMessage(msg)
        self.error_msg.show()

    def clear_all(self):
        '''
        Clear all method triggered by the "Clear" button.
        '''
        self.clear_buttons()
        self.other_system.setChecked(False)
        self.select_predefined_system.setChecked(True)
        self.other_phon_system.clear()
        self.predefined_systems.setEnabled(True)
        self.language.setCurrentIndex(0)
        self.IPA.setChecked(True)
        self.tableWidget.clearContents()
        self.corpus_table.clearContents()
        self.input_filename.clear()
        self.corpus_filename.clear()
        self.other_phon_system.clear()
        self.progress_bar.setValue(0)

    def clear_buttons(self):
        for button in self.buttons:
            button.setChecked(False)
        for button in self.sub_only_buttons:
            button.setCheckable(False)
            button.setChecked(False)
            button.setEnabled(False)
        for button in self.sad_buttons:
            button.setCheckable(False)
            button.setChecked(False)
            button.setEnabled(False)

    def abort(self):
        '''
        Displays abort warning, triggers abort_process on confirm.
        '''
        self.abort_msg = AbortMessage()
        self.abort_msg.buttonClicked.connect(self.abort_process)
        self.abort_msg.exec_()

    def abort_process(self, button):
        '''
        Aborts the worker thread execution.
        '''
        if button.text() == "OK":
            self.worker.abort()

    def specify_output_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path = QFileDialog.getSaveFileName(None, "Save Output File", "",
                                           "csv files (*.csv)", options=options)
        filename = path[0]
        if filename == '':
            return False
        if filename[-4:] != ".csv":
            self.filename = filename + ".csv"
        else:
            self.filename = filename
        try:
            write([], self.filename)
            return True
        except PermissionError:
            self.return_error("The file " + self.filename + " is open. Please close it.")

    def save_output(self):
        try:
            write(self.final_output, self.filename)
        except PermissionError:
            self.return_error("The file " + self.filename + " is open. Please close it.")
            self.retry_save_output()

    def retry_save_output(self):
        self.specify_output_file()
        self.save_output()

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit the program?"
        reply = QMessageBox.question(self, 'Exit', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    ###
    # Methods to load input and corpus data into tables
    ###

    def set_orth_only(self):
        if self.input_is_orth_only:
            return
        self.clear_buttons()
        self.input_transcription.setEnabled(False)
        self.surface_metrics.setEnabled(False)
        self.orth_metrics.setEnabled(True)
        self.phon_metrics.setEnabled(False)
        self.pg_metrics.setEnabled(False)
        self.change_input_table(has_phon_column=False)
        self.change_corpus_table(has_phon_column=False)

        self.input_is_orth_only = True
        self.input_is_both_phon_and_orth = False

    def set_both_phon_and_orth(self):
        if self.input_is_both_phon_and_orth:
            return
        self.clear_buttons()
        self.input_transcription.setEnabled(True)
        self.surface_metrics.setEnabled(True)
        self.orth_metrics.setEnabled(True)
        self.phon_metrics.setEnabled(True)
        self.pg_metrics.setEnabled(True)

        self.change_input_table(has_phon_column=True)
        self.change_corpus_table(has_phon_column=True)
        self.input_is_both_phon_and_orth = True
        self.input_is_orth_only = False

        self.reload_input_file_to_table()
        self.reload_corpus_file_to_table()

    def reload_input_file_to_table(self):
        filename = self.input_filename.text()
        if filename == '':
            return
        try:
            self.read_file_to_table(filename + ".csv", self.tableWidget)
        except PermissionError:
            self.return_error("Unable to read input file. Please close the file if it is open.")
            return
        except (FileNotFoundError, OSError):
            self.return_error("The specified input file cannot be found in the directory.")
            return
        except UnicodeDecodeError:
            self.return_error("Unable to read input file. Please check that it is saved in CSV format.")
            return

    def reload_corpus_file_to_table(self):
        corpus_filename = self.corpus_filename.text()
        if corpus_filename == '':
            return
        try:
            self.read_file_to_table(corpus_filename + ".csv", self.corpus_table)
        except PermissionError:
            self.return_error("Unable to read corpus file. Please close the file if it is open.")
            return
        except (FileNotFoundError, OSError):
            self.return_error("The specified corpus file cannot be found in the directory.")
            return
        except UnicodeDecodeError:
            self.return_error("Unable to read corpus file. Please check that it is saved in CSV format.")
            return

    def change_input_table(self, has_phon_column):
        if has_phon_column:
            self.tableWidget.setColumnCount(2)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(1, item)
            _translate = QtCore.QCoreApplication.translate
            item = self.tableWidget.horizontalHeaderItem(1)
            item.setText(_translate("LexiCAL", "Word (Phonological)"))
        else:
            self.tableWidget.setColumnCount(1)
            item = QtWidgets.QTableWidgetItem()
            self.tableWidget.setHorizontalHeaderItem(0, item)
            _translate = QtCore.QCoreApplication.translate
            item = self.tableWidget.horizontalHeaderItem(0)
            item.setText(_translate("LexiCAL", "Word (Orthographic)"))

    def change_corpus_table(self, has_phon_column):
        if has_phon_column:
            self.corpus_table.setColumnCount(3)
            item = QtWidgets.QTableWidgetItem()
            self.corpus_table.setHorizontalHeaderItem(2, item)
            _translate = QtCore.QCoreApplication.translate
            item = self.corpus_table.horizontalHeaderItem(0)
            item.setText(_translate("LexiCAL", "Word (Orthographic)"))
            item = self.corpus_table.horizontalHeaderItem(1)
            item.setText(_translate("LexiCAL", "Word (Phonological)"))
            item = self.corpus_table.horizontalHeaderItem(2)
            item.setText(_translate("LexiCAL", "Frequency"))
        else:
            self.corpus_table.setColumnCount(2)
            _translate = QtCore.QCoreApplication.translate
            item = self.corpus_table.horizontalHeaderItem(1)
            item.setText(_translate("LexiCAL", "Frequency"))

    def open_input_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path = QFileDialog.getOpenFileName(None, "Open Input File", "",
                                           "csv files (*.csv)", options=options)
        filename = path[0]
        if filename == '':
            return
        try:
            self.read_file_to_table(filename, self.tableWidget)
        except PermissionError:
            self.return_error("Unable to read input file. Please close the file if it is open.")
            return
        except (FileNotFoundError, OSError):
            self.return_error("The specified input file cannot be found in the directory.")
            return
        except UnicodeDecodeError:
            self.return_error("Unable to read input file. Please check that it is saved in CSV format.")
            return
        self.input_filename.setText(filename[:-4])
        self.tabWidget.setCurrentIndex(0)

    def open_corpus_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path = QFileDialog.getOpenFileName(None, "Open Corpus File", "",
                                           "csv files (*.csv)", options=options)
        filename = path[0]
        if filename == '':
            return
        try:
            self.read_file_to_table(filename, self.corpus_table)
        except PermissionError:
            self.return_error("Unable to read corpus file. Please close the file if it is open.")
            return
        except (FileNotFoundError, OSError):
            self.return_error("The specified corpus file cannot be found in the directory.")
            return
        except UnicodeDecodeError:
            self.return_error("Unable to read corpus file. Please check that it is saved in CSV format.")
            return
        self.corpus_filename.setText(filename[:-4])
        self.tabWidget.setCurrentIndex(1)

    def read_file_to_table(self, filename, table):
        with open(filename, encoding='utf-8') as f:
            data = []
            for row in csv.reader(f):
                data.append(row)
            if data[0][0][0] == '\ufeff':
                data[0][0] = data[0][0][1:]  # deletes '\ufeff' from beginning
        self.load_data_into_table(data, 0, 0, table)

    def load_data_into_table(self, data, startRow, startCol, table):
        table.clearContents()
        for row in range(len(data)):
            if row > table.rowCount():
                break
            for col in range(len(data[row])):
                if col > table.columnCount():
                    continue
                cell_content = data[row][col]
                table.setItem(row + startRow, col + startCol, QTableWidgetItem(cell_content))

    ###
    # Handle buttons
    ###

    def set_default_buttons(self):
        self.both_phon_and_orth_button.setChecked(True)
        self.set_both_phon_and_orth()
        self.language.setCurrentIndex(0)
        self.predefined_systems.setEnabled(True)
        self.other_system.setChecked(False)
        self.select_predefined_system.setChecked(True)
        self.IPA.setChecked(True)
        self.orth_n_dens.setChecked(True)
        self.allow_check_orth_n_dens()
        self.orth_n_freq.setChecked(True)
        self.allow_check_orth_n_freq()
        self.OLD20.setChecked(True)
        self.n_phon.setChecked(True)
        self.num_syl.setChecked(True)
        self.phon_n_dens.setChecked(True)
        self.allow_check_phon_n_dens()
        self.phon_n_freq.setChecked(True)
        self.allow_check_phon_n_freq()
        self.PLD20.setChecked(True)

    def get_selected_buttons(self):
        buttons = SelectedButtons()
        buttons.set_transcription_system(self.get_transcription_system())
        buttons.num_letters = self.num_letters.isChecked()
        buttons.orth_n_dens = self.orth_n_dens.isChecked()
        buttons.orth_n_dens_sub = self.orth_n_dens_sub.isChecked()
        buttons.orth_n_freq = self.orth_n_freq.isChecked()
        buttons.orth_n_freq_sub = self.orth_n_freq_sub.isChecked()
        buttons.OLD20 = self.OLD20.isChecked()
        buttons.orth_c_coeff = self.orth_c_coeff.isChecked()
        buttons.orth_spread = self.orth_spread.isChecked()
        buttons.orth_uniq_pt = self.orth_uniq_pt.isChecked()
        buttons.orth_bfreq = self.orth_bfreq.isChecked()

        buttons.n_phon = self.n_phon.isChecked()
        buttons.num_syl = self.num_syl.isChecked()
        buttons.phon_n_dens = self.phon_n_dens.isChecked()
        buttons.phon_n_dens_sub = self.phon_n_dens_sub.isChecked()
        buttons.phon_n_freq = self.phon_n_freq.isChecked()
        buttons.phon_n_freq_sub = self.phon_n_freq_sub.isChecked()
        buttons.PLD20 = self.PLD20.isChecked()
        buttons.phon_c_coeff = self.phon_c_coeff.isChecked()
        buttons.phon_spread = self.phon_spread.isChecked()
        buttons.phon_uniq_pt = self.phon_uniq_pt.isChecked()
        buttons.phon_bfreq = self.phon_bfreq.isChecked()

        buttons.pg_n_dens = self.pg_n_dens.isChecked()
        buttons.pg_n_dens_sub = self.pg_n_dens_sub.isChecked()
        buttons.pg_n_freq = self.pg_n_freq.isChecked()
        buttons.pg_n_freq_sub = self.pg_n_freq_sub.isChecked()
        buttons.pg_c_coeff = self.pg_c_coeff.isChecked()

        buttons.p_stress_code = self.p_stress_code.isChecked()
        buttons.stress_typ = self.stress_typ.isChecked()
        return buttons

    def get_transcription_system(self):
        if self.other_system.isChecked():
            key = 13
            return key
        if self.IPA.isChecked():
            key = 0
        elif self.SAMPA.isChecked():
            key = 6
        elif self.Klattese.isChecked():
            key = 12
        else:
            key = -1  # default key for orthography
        if self.language.isEnabled():
            language = self.language.currentIndex()
            key = language + key
        return key

    def allow_check_phon_n_dens(self):
        can_click = self.phon_n_dens.isChecked()
        self.phon_n_dens_sub.setEnabled(can_click)
        self.phon_n_dens_sad.setEnabled(can_click)
        self.phon_n_dens_sub.setCheckable(can_click)
        self.phon_n_dens_sad.setCheckable(can_click)
        self.phon_n_dens_sad.setChecked(True)

    def allow_check_phon_n_freq(self):
        can_click = self.phon_n_freq.isChecked()
        self.phon_n_freq_sub.setEnabled(can_click)
        self.phon_n_freq_sad.setEnabled(can_click)
        self.phon_n_freq_sub.setCheckable(can_click)
        self.phon_n_freq_sad.setCheckable(can_click)
        self.phon_n_freq_sad.setChecked(True)

    def allow_check_orth_n_dens(self):
        can_click = self.orth_n_dens.isChecked()
        self.orth_n_dens_sad.setEnabled(can_click)
        self.orth_n_dens_sub.setEnabled(can_click)
        self.orth_n_dens_sad.setCheckable(can_click)
        self.orth_n_dens_sub.setCheckable(can_click)
        self.orth_n_dens_sub.setChecked(False)
        self.orth_n_dens_sad.setChecked(True)

    def allow_check_orth_n_freq(self):
        can_click = self.orth_n_freq.isChecked()
        self.orth_n_freq_sub.setEnabled(can_click)
        self.orth_n_freq_sad.setEnabled(can_click)
        self.orth_n_freq_sub.setCheckable(can_click)
        self.orth_n_freq_sad.setCheckable(can_click)
        self.orth_n_freq_sad.setChecked(True)

    def allow_check_pg_n_dens(self):
        can_click = self.pg_n_dens.isChecked()
        self.pg_n_dens_sub.setEnabled(can_click)
        self.pg_n_dens_sad.setEnabled(can_click)
        self.pg_n_dens_sub.setCheckable(can_click)
        self.pg_n_dens_sad.setCheckable(can_click)
        self.pg_n_dens_sad.setChecked(True)

    def allow_check_pg_n_freq(self):
        can_click = self.pg_n_freq.isChecked()
        self.pg_n_freq_sub.setEnabled(can_click)
        self.pg_n_freq_sad.setEnabled(can_click)
        self.pg_n_freq_sub.setCheckable(can_click)
        self.pg_n_freq_sad.setCheckable(can_click)
        self.pg_n_freq_sad.setChecked(True)

    def enable_Klattese(self):
        if self.language.currentIndex() != 0:
            self.Klattese.setEnabled(False)
            if self.Klattese.isChecked():
                self.IPA.setChecked(True)
        else:
            self.Klattese.setEnabled(True)

    # Enables browsing for other phonetic system if other is checked, disables otherwise
    def enable_other_system_browse(self):
        if self.other_system.isChecked():
            self.other_phon_system.setEnabled(True)
            self.phon_system_browse.setEnabled(True)
            self.disable_surface_metrics()
            self.predefined_systems.setEnabled(False)
        else:
            self.other_phon_system.setText("")
            self.other_phon_system.setEnabled(False)
            self.phon_system_browse.setEnabled(False)
            self.predefined_systems.setEnabled(True)

    def browse_phonetic_system(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        path = QFileDialog.getOpenFileName(None, "Select Phonetic System", "",
                                           "csv files (*.csv)", options=options)
        filename = path[0]
        if not self.open_phonetic_system(filename):
            return
        self.other_phon_system.setText(filename[:-4])
        if Phonemes.custom_primary_stress is not None:
            self.surface_metrics.setEnabled(True)
        else:
            self.disable_surface_metrics()

    def open_phonetic_system(self, filename):
        if filename != '':
            try:
                if not Phonemes().get_custom_phonemes(filename):
                    self.return_error("The phonetic system file format is incorrect.")
                    return False
                return True
            except (FileNotFoundError, OSError):
                self.return_error("The specified phonetic system file was not found in the directory.")
                return False
            except UnicodeDecodeError:
                self.return_error("Unable to read phonetic system file. " +
                                  "Please ensure that the file is saved in CSV format.")
                return False
            except PermissionError:
                self.return_error("Unable to read phonetic system file. Please close the file if it is open.")
                return False

    def disable_surface_metrics(self):
        self.p_stress_code.setChecked(False)
        self.stress_typ.setChecked(False)
        self.surface_metrics.setEnabled(False)

    def enable_surface_metrices(self):
        self.surface_metrics.setEnabled(True)

    def no_phonetic_system_is_checked(self):
        return not self.other_system.isChecked() and not self.IPA.isChecked() \
               and not self.Klattese.isChecked() and not self.SAMPA.isChecked()

class CalculatorStub(QtWidgets.QMainWindow, Ui_LexiCAL):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
