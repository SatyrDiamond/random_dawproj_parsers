# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import zlib
import logging

class xtracker_dmf_pattern:
	def __init__(self, byr_stream):
		size = byr_stream.uint16()
		print(size)
		with byr_stream.isolate_size(size, True) as bye_stream:
			pass
		#	track_entries = byr_stream.uint16()
		#	print(track_entries)

class xtracker_dmf_song:
	def __init__(self):
		self.version = 0
		self.tracker_name = ''
		self.title = ''
		self.composer = ''
		self.date = None
		self.day = 0
		self.month = 0
		self.year = 0
		self.disc = []
		self.seq_start = 0
		self.seq_end = 0
		self.seq_order = []

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)
		byr_stream.magic_check(b'DDMF')
		self.version = byr_stream.uint8()
		self.tracker_name = byr_stream.string(8)
		self.title = byr_stream.string(30)
		self.composer = byr_stream.string(20)
		self.day = byr_stream.uint8()
		self.month = byr_stream.uint8()
		self.year = byr_stream.uint8()+1900

		while byr_stream.remaining():
			chunkname = byr_stream.raw(4)
			chunksize = byr_stream.uint32()
			if chunkname == b'CMSG':
				with byr_stream.isolate_size(chunksize, True) as bye_stream:
					bye_stream.skip(1)
					self.disc = [byr_stream.string(40, encoding='iso8859_1') for v in range((chunksize-1)//40)]
			elif chunkname == b'SEQU':
				with byr_stream.isolate_size(chunksize, True) as bye_stream:
					self.seq_start = bye_stream.uint16()
					self.seq_end = bye_stream.uint16()
					self.seq_order = bye_stream.l_uint16(bye_stream.remaining()//2)
			elif chunkname == b'PATT':
				with byr_stream.isolate_size(chunksize, True) as bye_stream:
					pat_entries = bye_stream.uint16()
					max_tracks = bye_stream.uint8()


			else:
				print(chunkname)
				break


apeinst_obj = xtracker_dmf_song()
apeinst_obj.load_from_file("G:\\RandomMusicFiles\\tracker_lessknown\\X-Tracker\\p3_bop.dmf")
