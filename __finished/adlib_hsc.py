# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import logging

class adlib_hsc_song:
	def __init__(self):
		self.instruments = None
		self.orderlist = None
		self.patterns = []

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)
		self.instruments = byr_stream.table8((128, 12))
		self.orderlist = byr_stream.l_uint8(51)
		while byr_stream.remaining():
			self.patterns.append(byr_stream.table8((64, 9, 2)))

apeinst_obj = adlib_hsc_song()
apeinst_obj.load_from_file("TorbyTorrents - CrackMe Extra v2.hsc")
