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

from Output import Output
from PhonMetrics import PhonMetrics
from OrthMetrics import OrthMetrics
from PGMetrics import PGMetrics
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable

class WorkerSignals(QObject):
    num_words_processed = pyqtSignal(int)
    total_num_words = pyqtSignal(int)
    completed_signal = pyqtSignal()

class InputWord:
    def __init__(self, orth, phon):
        self.orth = orth
        self.phon = phon

class ExecCalculator(QRunnable):
    '''
    QRunnable class which executes a single run of processing.
    '''
    def __init__(self, corpus, selected_buttons, orth_words, phon_words, pg_words, num_words):
        super().__init__()
        self.init_is_success = False
        self.corpus = corpus
        self.calculator = selected_buttons
        self.orth_words = orth_words
        self.phon_words = phon_words
        self.pg_words = pg_words
        self.num_words = num_words
        self.exec_is_success = False
        self.error_msg = ""
        self.isAbort = False
        self.key = self.calculator.get_transcription_system()
        self.signals = WorkerSignals()

    def init(self):
        '''
        Initialise the words and classes OrthMetrics, PhonMetrics and PGMetrics depending
        on the metrics selected.
        '''
        output = Output(self.num_words)
        self.input_words = self.make_input_words()
        self.phon_metrics = None
        self.orth_metrics = None
        self.pg_metrics = None

        if self.orth_words and self.calculator.is_any_orth_metric_checked():
            self.orth_metrics = OrthMetrics(self.orth_words, self.corpus, output)
        if self.phon_words and (self.calculator.is_any_phon_metric_checked()
                                or self.calculator.is_any_stress_metric_checked()):
            self.phon_metrics = PhonMetrics(self.key, self.phon_words, self.corpus, output)
        if self.pg_words and self.calculator.is_any_pg_metric_checked():
            self.pg_metrics = PGMetrics(self.key, self.pg_words, self.corpus, output)

    @pyqtSlot()
    def run(self):
        '''
        Each word in input is processed one at a time, after which a signal is sent to the progress bar.
        When all words have been processed, the header for the final output is generated and the
        final output is printed. A successful complete signal is sent.
        '''
        output = Output(0)
        count = 0
        num_words = len(self.input_words)
        if num_words == 0:
            self.signals.completed_signal.emit()
        self.signals.total_num_words.emit(num_words)

        for word in self.input_words:
            if self.isAbort:
                self.throw_error("Process was aborted.")
                return
            word_output = Output(1)
            self.generate_word_entry(word, word_output)
            output.add_word_entry(word_output.word_entries[0])
            self.signals.num_words_processed.emit(count)
            count += 1

        output.header = self.generate_header()
        self.output = output.print()

        self.exec_is_success = True
        self.signals.completed_signal.emit()

    def make_input_words(self):
        input_words = []
        if not self.orth_words:
            for word in self.phon_words:
                input_words.append(InputWord(None, word))
        elif not self.phon_words:
            for word in self.orth_words:
                input_words.append(InputWord(word, None))
        elif self.pg_words:
            for word in self.pg_words:
                input_words.append(InputWord(word[0], word[1]))
        return input_words

    def generate_word_entry(self, word, output):
        output.init_word_at_index(0, word.orth, list(word.orth), isOrth=True, print_init=True)
        if self.orth_metrics and self.calculator.is_any_orth_metric_checked():
            self.orth_metrics.set_word(word.orth, output)
            output = self.generate_orth_metrics(self.orth_metrics)
        if self.phon_metrics and self.calculator.is_any_phon_metric_checked():
            self.phon_metrics.set_word(word.phon, output)
            output = self.generate_phon_metrics(self.phon_metrics)
        if self.pg_metrics and self.calculator.is_any_pg_metric_checked():
            self.pg_metrics.set_word(word, output)
            output = self.generate_pg_metrics(self.pg_metrics)
        if self.phon_metrics and self.calculator.is_any_stress_metric_checked():
            self.phon_metrics.set_word(word.phon, output)
            output = self.generate_stress_metrics(self.phon_metrics)
        return output

    @pyqtSlot()
    def abort(self):
        self.isAbort = True

    def throw_error(self, msg):
        self.error_msg = msg
        self.isAbort = False
        self.exec_is_success = False
        self.signals.completed_signal.emit()

    def generate_phon_metrics(self, phon_metrics):
        if self.calculator.n_phon:
            phon_metrics.n_phon()
        if self.calculator.num_syl:
            phon_metrics.num_syllables()

        if self.calculator.phon_n_dens:
            sub_only = self.calculator.phon_n_dens_sub
            phon_metrics.find_neighbours(sub_only)
            phon_metrics.n_density(sub_only)
        if self.calculator.phon_n_freq:
            sub_only = self.calculator.phon_n_freq_sub
            phon_metrics.find_neighbours(sub_only)
            phon_metrics.n_freq(sub_only)

        if self.calculator.PLD20:
            phon_metrics.PLD20()
        if self.calculator.phon_spread:
            phon_metrics.phon_spread()
        if self.calculator.phon_uniq_pt:
            phon_metrics.unique_point()
        if self.calculator.phon_c_coeff:
            phon_metrics.ccoeff()
        if self.calculator.phon_bfreq:
            phon_metrics.biphone_prob()
        return phon_metrics.get_output()

    def generate_orth_metrics(self, orth_metrics):
        if self.calculator.num_letters:
            orth_metrics.num_letters()
        if self.calculator.orth_n_dens:
            sub_only = self.calculator.orth_n_dens_sub
            orth_metrics.find_neighbours(sub_only)
            orth_metrics.n_density(sub_only)
        if self.calculator.orth_n_freq:
            sub_only = self.calculator.orth_n_freq_sub
            orth_metrics.find_neighbours(sub_only)
            orth_metrics.n_freq(sub_only)
        if self.calculator.OLD20:
            orth_metrics.OLD20()
        if self.calculator.orth_spread:
            orth_metrics.orth_spread()
        if self.calculator.orth_uniq_pt:
            orth_metrics.unique_point()
        if self.calculator.orth_c_coeff:
            orth_metrics.ccoeff()
        if self.calculator.orth_bfreq:
            orth_metrics.bigram_prob()
        return orth_metrics.get_output()

    def generate_pg_metrics(self, pg_metrics):
        if self.calculator.pg_n_dens:
            sub_only = self.calculator.pg_n_dens_sub
            pg_metrics.find_pg_neighbours(sub_only)
            pg_metrics.n_density(sub_only)
        if self.calculator.pg_n_freq:
            sub_only = self.calculator.pg_n_freq_sub
            pg_metrics.find_pg_neighbours(sub_only)
            pg_metrics.n_freq(sub_only)
        if self.calculator.pg_c_coeff:
            pg_metrics.ccoeff()
        return pg_metrics.get_output()

    def generate_stress_metrics(self, phon_metrics):
        if self.calculator.p_stress_code:
            phon_metrics.primary_stress_code()
        if self.calculator.stress_typ:
            phon_metrics.stress_typicality()
        return phon_metrics.get_output()

    def generate_header(self):
        header = []
        orth_is_printed = True
        phon_is_printed = False
        header.append("Item (Orthography)") # orth_is_printed by default
        if self.calculator.num_letters:
            header.append("Length")
        if self.calculator.orth_n_dens:
            header.append("Orthographic Neighbourhood Density")
            header.append("Identity of Orthographic Neighbours")
        if self.calculator.orth_n_freq:
            header.append("Orthographic Neighbourhood Frequency (M)")
            header.append("Orthographic Neighbourhood Frequency (SD)")
        if self.calculator.OLD20:
            header.append("OLD-20 (M)")
            header.append("OLD-20 (SD)")
        if self.calculator.orth_spread:
            header.append("Orthographic Spread")
        if self.calculator.orth_uniq_pt:
            header.append("Orthographic Uniqueness Point")
        if self.calculator.orth_c_coeff:
            header.append("Orthographic C Coefficient")
        if self.calculator.orth_bfreq:
            header.append("Sum Bigram Frequency")

        if self.calculator.is_any_phon_metric_checked():
            header.append("Item (Phonology)")
            phon_is_printed = True
        if self.calculator.n_phon:
            header.append("No. of Phonemes")
        if self.calculator.num_syl:
            header.append("No. of Syllables")
        if self.calculator.phon_n_dens:
            header.append("Phonological Neighbourhood Density")
            header.append("Identity of Phonological Neighbours (O)")
            header.append("Identity of Phonological Neighbours (P)")
        if self.calculator.phon_n_freq:
            header.append("Phonological Neighbourhood Frequency (M)")
            header.append("Phonological Neighbourhood Frequency (SD)")
        if self.calculator.PLD20:
            header.append("PLD-20 (M)")
            header.append("PLD-20 (SD)")
        if self.calculator.phon_spread:
            header.append("Phonological Spread")
        if self.calculator.phon_uniq_pt:
            header.append("Phonological Uniqueness Point")
        if self.calculator.phon_c_coeff:
            header.append("Phonological C Coefficient")
        if self.calculator.phon_bfreq:
            header.append("Sum Biphone Frequency")

        if self.calculator.is_any_pg_metric_checked():
            if not orth_is_printed:
                header.append("Item (Orthography)")
            if not phon_is_printed:
                header.append("Item (Phonology)")
        if self.calculator.pg_n_dens:
            header.append("Phonographic Neighbourhood Density")
            header.append("Identity of Phonographic Neighbours (O)")
            header.append("Identity of Phonographic Neighbours (P)")
        if self.calculator.pg_n_freq:
            header.append("Phonographic Neighbourhood Frequency (M)")
            header.append("Phonographic Neighbourhood Frequency (SD)")
        if self.calculator.pg_c_coeff:
            header.append("Phonographic C Coefficient")

        if self.calculator.is_any_stress_metric_checked():
            if not phon_is_printed:
                header.append("Item (Phonology)")
        if self.calculator.p_stress_code:
            header.append("Stress Code")
        if self.calculator.stress_typ:
            header.append("Stress Typicality")
        return header

    def format_result(self, result):
        new_result = []
        for row in result:
            string = ""
            for n in row:
                if type(n) is not str:
                    string += str(n)
                else:
                    string += n
                string += ", "
            new_result.append([string[:-2]])
        return new_result

    def get_number_of_words(self):
        return len(self.input_words)
