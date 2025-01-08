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

class SelectedButtons:
    def __init__(self):
        self.key = None
        self.num_letters = False
        self.orth_n_dens = False
        self.orth_n_dens_sub = False
        self.orth_n_freq = False
        self.orth_n_freq_sub = False
        self.OLD20 = False
        self.orth_c_coeff = False
        self.orth_spread = False
        self.orth_uniq_pt = False
        self.orth_bfreq = False

        self.n_phon = False
        self.num_syl = False
        self.phon_n_dens = False
        self.phon_n_dens_sub = False
        self.phon_n_freq = False
        self.phon_n_freq_sub = False
        self.PLD20 = False
        self.phon_c_coeff = False
        self.phon_spread = False
        self.phon_uniq_pt = False
        self.phon_bfreq = False

        self.pg_n_dens = False
        self.pg_n_dens_sub = False
        self.pg_n_freq = False
        self.pg_n_freq_sub = False
        self.pg_c_coeff = False
        self.p_stress_code = False
        self.ps_stress_code = False
        self.stress_typ = False

    def is_any_orth_metric_checked(self):
        return self.num_letters or self.orth_n_dens or self.orth_n_freq \
               or self.OLD20 or self.orth_c_coeff or self.orth_spread \
               or self.orth_uniq_pt or self.orth_bfreq

    def is_any_phon_metric_checked(self):
        return self.n_phon or self.num_syl or self.phon_n_dens or self.phon_n_freq \
               or self.PLD20 or self.phon_c_coeff or self.phon_spread \
               or self.phon_uniq_pt or self.phon_bfreq

    def is_any_pg_metric_checked(self):
        return self.pg_n_dens or self.pg_n_freq or self.pg_c_coeff

    def is_any_stress_metric_checked(self):
        return self.p_stress_code or self.stress_typ

    def is_any_checked(self):
        return (self.is_any_orth_metric_checked() or self.is_any_phon_metric_checked()
                or self.is_any_pg_metric_checked() or self.is_any_stress_metric_checked())

    def set_transcription_system(self, key):
        self.key = key

    def get_transcription_system(self):
        return self.key