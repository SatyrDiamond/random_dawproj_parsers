# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects import bytereader
import logging

logger_projparse = logging.getLogger('projparse')


class chunk:
	def __init__(self, byr_stream):
		self.type = byr_stream.raw(4)[::-1].decode()
		self.unk1 = byr_stream.uint16()
		self.unk2 = byr_stream.int32()
		self.unk3 = byr_stream.int32()
		self.unk4 = byr_stream.int32()
		self.unk5 = byr_stream.int32()
		self.unk6 = byr_stream.int32()
		self.unk7 = byr_stream.uint16()
		self.data_size = byr_stream.uint32()
		self.unk8 = byr_stream.int32()
		self.data_pos = byr_stream.tell()

		print(self.type, end=' ')
		print(str(self.unk1).ljust(3), end=' ')
		print(str(self.unk2).ljust(3), end=' ')
		print(str(self.unk3>>2).ljust(3), end=' ')
		print(str(self.unk4).ljust(3), end=' ')
		print(str(self.unk5).ljust(12), end=' ')
		print(str(self.unk6).ljust(3), end=' ')
		print(str(self.unk7).ljust(3), end=' ')
		print(str(self.unk8).ljust(3), end=' ')

		with byr_stream.isolate_size(self.data_size, True) as bye_stream:
			print(bye_stream.raw(20).hex(), end=' ')

		print()

class logic_project:
	def load_from_file(self, input_file):

		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)

		byr_stream.seek(0x18)

		while byr_stream.remaining():
			chunk(byr_stream)

		print( byr_stream.raw(10)  )


test_obj = logic_project()
test_obj.load_from_file("G:\\RandomMusicFiles\\logicx\\jukeblocks - House.logicx\\Alternatives\\000\\ProjectData")
