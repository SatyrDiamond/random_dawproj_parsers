# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import logging

class sc68_file:
	def __init__(self):
		self.scfn = ''
		self.scdf = 0
		self.scmu = None
		self.track_name = ''
		self.author_name = ''
		self.composer_name = ''
		self.scd0 = 0
		self.scat = 0
		self.track_time = 0
		self.scfr = 0
		self.scfq = 0
		self.sclp = 0
		self.scty = 0
		self.external_replay_name = ''
		self.data = b''
		self.scef = None

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)
		byr_stream.magic_check(b'SC68 Music-file / (c) (BeN)jamin Gerard / SasHipA-Dev  \0')

		byr_stream.magic_check(b'SC68')
		byr_stream.skip(4)

		main_iff_obj = byr_stream.chunk_objmake()
		main_iff_obj.set_sizes(4, 4, False)
		for chunk_obj in main_iff_obj.iter(byr_stream.tell(), byr_stream.end):
			cid = chunk_obj.id
			if cid == b'SCFN': self.scfn = byr_stream.string(chunk_obj.size)
			if cid == b'SCDF': self.scdf = byr_stream.int32()
			if cid == b'SCMU': self.scmu = byr_stream.raw(chunk_obj.size)
			if cid == b'SCMN': self.track_name = byr_stream.string(chunk_obj.size)
			if cid == b'SCAN': self.author_name = byr_stream.string(chunk_obj.size)
			if cid == b'SCCN': self.composer_name = byr_stream.string(chunk_obj.size)
			if cid == b'SCD0': self.scd0 = byr_stream.int32()
			if cid == b'SCAT': self.scat = byr_stream.int32()
			if cid == b'SCTI': self.track_time = byr_stream.int32()
			if cid == b'SCFR': self.scfr = byr_stream.int32()
			if cid == b'SCFQ': self.scfq = byr_stream.int32()
			if cid == b'SCLP': self.sclp = byr_stream.int32()
			if cid == b'SCTY': self.scty = byr_stream.int32()
			if cid == b'SCRE': self.external_replay_name = byr_stream.string(chunk_obj.size)
			if cid == b'SCDA': self.data = byr_stream.raw(chunk_obj.size)
			if cid == b'SCEF': break

apeinst_obj = sc68_file()
apeinst_obj.load_from_file("SCOOPEX - Logical Preview intro.sc68")
