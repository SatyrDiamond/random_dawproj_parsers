# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import logging

class atari_sap:
	def __init__(self):
		self.header = {}
		self.blocks = {}

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)
		byr_stream.magic_check(b'SAP')

		mc = 0
		startaft = 0
		while byr_stream.remaining() and mc!=2:
			startaft += 1
			if byr_stream.raw(1)==b'\xff': mc += 1
			else: mc = 0

		byr_stream.seek(3)
		stringd = byr_stream.string(startaft-5)
		for text in stringd.strip().split('\r\n'):
			splittxt = text.split(' ', 1)
			if len(splittxt) == 1: self.header[splittxt[0]] = splittxt[1]

		byr_stream.seek(startaft+3)

		while byr_stream.remaining():
			m_start = byr_stream.uint16()
			m_end = byr_stream.uint16()
			m_raw = byr_stream.raw((m_end-m_start)+1)
			self.blocks[m_start] = m_raw

apeinst_obj = atari_sap()
apeinst_obj.load_from_file("TorbyTorrents - NoClone crk.sap")
