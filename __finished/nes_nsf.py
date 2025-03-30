# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import zlib
import logging

class nes_nsf_file:
	def __init__(self):
		pass
		self.version = 0
		self.total_songs = 0
		self.start_song = 0
		self.addr_load = 0
		self.addr_init = 0
		self.addr_play = 0
		self.name = ''
		self.artist = ''
		self.copyright = ''
		self.speed_ntsc = 0
		self.bankswitch_initval = 0
		self.speed_pal = 0
		self.flags_pal_ntsc = []
		self.flags_soundchip = []
		self.reserved_nsf2 = 0
		self.data = None

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)
		byr_stream.magic_check(b'NESM\x1a')
		self.version = byr_stream.uint8()
		self.total_songs = byr_stream.uint8()
		self.start_song = byr_stream.uint8()
		self.addr_load = byr_stream.uint16()
		self.addr_init = byr_stream.uint16()
		self.addr_play = byr_stream.uint16()
		self.name = byr_stream.string(32)
		self.artist = byr_stream.string(32)
		self.copyright = byr_stream.string(32)
		self.speed_ntsc = byr_stream.uint16()
		self.bankswitch_initval = byr_stream.l_uint8(8)
		self.speed_pal = byr_stream.uint16()
		self.flags_pal_ntsc = byr_stream.flags8()
		self.flags_soundchip = byr_stream.flags8()
		self.reserved_nsf2 = byr_stream.uint8()
		datalen = byr_stream.uint24()
		self.data = byr_stream.rest() if not datalen else byr_stream.raw(datalen)

apeinst_obj = nes_nsf_file()
apeinst_obj.load_from_file("MESMERiZE - Cockos Reaper 3.75 x64 kg.nsf")
