# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import logging
import numpy as np

class mixpad_chunk:
	def __init__(self, byr_stream):
		self.id = -1
		self.type = 0
		self.data = None
		if byr_stream: self.read(byr_stream)

	def debugtxt(self, tabv):
		tabtxt = ('   '*tabv)
		if self.type:
			print(tabtxt, self)
		else:
			print(tabtxt, self)
			for x in self.data:
				x.debugtxt(tabv+1)

	def __repr__(self):
		if self.type:
			return '<MixPad Chunk - %s, %i, %s>' % (self.id, self.type, str(self.data))
		else:
			return '<MixPad Container - %s, %i>' % (self.id, self.type)

	def read(self, byr_stream):
		self.id = byr_stream.raw(2).hex()
		self.type = byr_stream.uint16()
		size = byr_stream.uint64()
		#print('CHUNK', self.id_1, self.id_2, self.type, end=' ')
		with byr_stream.isolate_size(size, True) as bye_stream: 
			if self.type == 0: 
				self.data = []
				while bye_stream.remaining(): self.data.append(mixpad_chunk(bye_stream))
			elif self.type == 1: self.data = byr_stream.uint8()
			elif self.type == 2: self.data = byr_stream.int32()
			elif self.type == 3: self.data = byr_stream.int64()
			elif self.type == 4: self.data = byr_stream.float()
			elif self.type == 6: self.data = byr_stream.raw(size)
			else: 
				print('unknown type', self.type)
				self.data = byr_stream.raw(size)
		#print(self.data)

class mixpad_song:
	def __init__(self):
		self.main_chunk = None

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)

		byr_stream.magic_check(b'lsdf')
		self.unk_1 = byr_stream.uint16()
		self.unk_2 = byr_stream.uint32()
		self.unk_3 = byr_stream.uint16()

		self.main_chunk = mixpad_chunk(byr_stream)
		#self.main_chunk.debugtxt(0)

apeinst_obj = mixpad_song()
apeinst_obj.load_from_file("C:\\ProgramData\\NCH Software\\MixPad\\example\\example.mpdp")
