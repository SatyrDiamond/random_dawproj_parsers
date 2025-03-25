# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import logging
import numpy as np

dtype_note = np.dtype([
	('key', np.uint8),
	('ctrl', np.uint8),
	('pos', np.uint16),
	('unk1', np.uint16),
	('dur', np.int16),
	('vel', np.uint16),
	]) 

class cherry_track:
	def __init__(self, byr_stream):
		if byr_stream: self.read(byr_stream)

	def read(self, byr_stream):
		self.size = byr_stream.uint32()
		with byr_stream.isolate_size(self.size, False) as bye_stream:
			bye_stream.skip(12)
			self.mode = bye_stream.uint16()
			self.num = bye_stream.uint32()
			bye_stream.skip(42)
			self.name = bye_stream.string(64)
			remainsize = ((bye_stream.remaining()-4)//10)
			self.data = np.frombuffer(bye_stream.read(10*remainsize), dtype=dtype_note)

class cherry_song:
	def __init__(self):
		self.tracks = []
		self.unk1 = 0
		self.unk2 = 0
		self.num_tracks = 0
		self.name = ''
		self.copyright = ''
		self.endfile = 0

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)
		byr_stream.magic_check(b'CHRY0101')

		self.unk1 = byr_stream.uint8()
		self.unk2 = byr_stream.uint8()
		self.num_tracks = byr_stream.uint8()

		byr_stream.seek(0x100)

		self.name = byr_stream.string(128)
		self.copyright = byr_stream.string(128)
		self.endfile = byr_stream.uint32()

		byr_stream.seek(0x300)
		offsets = byr_stream.l_uint32(self.num_tracks)

		for offset in offsets:
			byr_stream.seek(offset)
			self.tracks.append(cherry_track(byr_stream))

apeinst_obj = cherry_song()
apeinst_obj.load_from_file("Untitled3.chy")
