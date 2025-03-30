# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import logging

class c64sid_file:
	def __init__(self):
		self.version = 0
		self.dataOffset = 0
		self.loadAddress = 0
		self.initAddress = 0
		self.playAddress = 0
		self.numsongs = 0
		self.startSong = 0
		self.speed = 0
		self.name = ''
		self.author = ''
		self.released = ''
		self.flags = 0
		self.startPage = 0
		self.pageLength = 0
		self.secondSIDAddress = 0
		self.thirdSIDAddress = 0

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)
		byr_stream.magic_check(b'PSID')
		self.version = byr_stream.uint16_b()
		self.dataOffset = byr_stream.uint16_b()
		self.loadAddress = byr_stream.uint16_b()
		self.initAddress = byr_stream.uint16_b()
		self.playAddress = byr_stream.uint16_b()
		self.numsongs = byr_stream.uint16_b()
		self.startSong = byr_stream.uint16_b()
		self.speed = byr_stream.uint32_b()
		self.name = byr_stream.string(32)
		self.author = byr_stream.string(32)
		self.released = byr_stream.string(32)
		if self.version > 1:
			self.flags = byr_stream.flags16()
			self.startPage = byr_stream.uint8()
			self.pageLength = byr_stream.uint8()
			self.secondSIDAddress = byr_stream.uint8()
			self.thirdSIDAddress = byr_stream.uint8()
			self.data = byr_stream.rest()
		else:
			self.data = byr_stream.rest()

apeinst_obj = c64sid_file()
apeinst_obj.load_from_file("TorbyTorrents - MoleskinSoft Clone Remover crk.sid")
