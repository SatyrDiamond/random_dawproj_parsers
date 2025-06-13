# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import zlib
import logging

def chunk(byr_stream):
	name = byr_stream.raw(4)
	size = byr_stream.uint32_b()
	return name, size

class notion_chunk:
	def __init__(self, byr_stream):
		self.type = byr_stream.uint8()
		self.name = byr_stream.raw(4)
		self.value = None

		if self.type == 1: self.value = byr_stream.raw(4)
		elif self.type == 2: self.value = byr_stream.int8()
		elif self.type == 3: self.value = byr_stream.string_t()

		elif self.type == 20: self.value = byr_stream.int8()
		elif self.type == 22: self.value = byr_stream.uint32_b()
		elif self.type == 23: self.value = byr_stream.uint8()
		elif self.type == 24: self.value = byr_stream.uint16_b()
		elif self.type == 25: self.value = byr_stream.uint32_b()
		elif self.type == 26: self.value = byr_stream.float_b()
		elif self.type == 27: self.value = byr_stream.double_b()

		elif self.type == 40: self.value = byr_stream.l_int8(byr_stream.uint32_b())
		elif self.type == 42: self.value = byr_stream.l_uint32_b(byr_stream.uint32_b())
		elif self.type == 43: self.value = byr_stream.l_uint8(byr_stream.uint32_b())
		elif self.type == 44: self.value = byr_stream.l_uint16_b(byr_stream.uint32_b())
		elif self.type == 45: self.value = byr_stream.l_uint32_b(byr_stream.uint32_b())
		elif self.type == 46: self.value = byr_stream.l_float_b(byr_stream.uint32_b())
		elif self.type == 47: self.value = byr_stream.l_double_b(byr_stream.uint32_b())

	def __repr__(self):
		return '<Notion Chunk - Name: %s | Type %i >' % (self.name.decode(), self.type)

class notion_group:
	def __init__(self, byr_stream):
		self.name = None
		self.data = []
		if byr_stream: self.read(byr_stream)

	def __repr__(self):
		return '<Notion Group - Name: %s | %i Chunks >' % (self.name, len(self.data))

	def read(self, byr_stream):
		self.name = byr_stream.raw(4)
		gsize = byr_stream.uint32_b()

		numpoints = byr_stream.uint32_b()
		for _ in range(numpoints):
			name = byr_stream.string(4)
			size = byr_stream.uint32_b()
			with byr_stream.isolate_size(size, True) as bye_stream:
				indata = []
				while bye_stream.remaining():
					chunk_obj = notion_chunk(bye_stream)
					if chunk_obj.value is None:
						rawd = byr_stream.raw(bye_stream.remaining())
						break
					else:
						self.data.append([name, chunk_obj])

class notion_song:
	def __init__(self):
		self.groups = {}
		self.version = 4

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)

		byr_stream.magic_check(b'ttkb')
		self.version = byr_stream.uint32_b()
		while byr_stream.remaining():
			group_obj = notion_group(byr_stream)
			self.groups[group_obj.name] = group_obj
		
apeinst_obj = notion_song()
apeinst_obj.load_from_file("Bach - Brandenburg Concerto No.4 Allegro.notion")