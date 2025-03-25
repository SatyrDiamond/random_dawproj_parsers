# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import logging

class motorola_pwt:
	def __init__(self):
		self.data = []

	def load_from_file(self, input_file):
		linefile = open(input_file, 'r')
		lines = [x.strip().split('\t') for x in linefile.readlines()]
		self.data = lines

apeinst_obj = motorola_pwt()
apeinst_obj.load_from_file("G:\\RandomMusicFiles\\mobile\\pwt\\Motorola_C115\\system\\l_error.pwt")
