# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import logging

class snes_spc:
	def __init__(self):
		self.data = None
		self.dsp_reg = None
		self.ex_ram = None
		self.version_minor = 0

		self.reg_pc = 0
		self.reg_a = 0
		self.reg_x = 0
		self.reg_y = 0
		self.reg_psw = 0
		self.reg_sp = 0
		self.reg_reserved = 0

		self.title = ''
		self.game_name = ''
		self.dumper = ''
		self.comments = ''
		self.date = None
		self.fadeout_start = None
		self.fadeout_ms = None
		self.artist = ''
		self.defualt_chan_disables = 0
		self.emu_used_dumper = 0

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)
		byr_stream.magic_check(b'SNES-SPC700 Sound File Data v0.30')
		byr_stream.skip(2)
		has_idtag = byr_stream.uint8()
		self.version_minor = byr_stream.uint8()

		self.reg_pc = byr_stream.uint16()
		self.reg_a = byr_stream.uint8()
		self.reg_x = byr_stream.uint8()
		self.reg_y = byr_stream.uint8()
		self.reg_psw = byr_stream.uint8()
		self.reg_sp = byr_stream.uint8()
		self.reg_reserved = byr_stream.uint16()
		if has_idtag == 26:
			self.title = byr_stream.string(32)
			self.game_name = byr_stream.string(32)
			self.dumper = byr_stream.string(16)
			self.comments = byr_stream.string(32)
			self.date = byr_stream.raw(11)
			self.fadeout_start = byr_stream.raw(3)
			self.fadeout_ms = byr_stream.raw(5)
			self.artist = byr_stream.string(32)
			self.disable_channel = byr_stream.uint8()
			self.emu_used_dumper = byr_stream.uint8()


		byr_stream.seek(0x100)
		self.data = byr_stream.raw(65536)
		self.dsp_reg = byr_stream.raw(128)
		byr_stream.skip(64)
		self.ex_ram = byr_stream.raw(64)

apeinst_obj = snes_spc()
apeinst_obj.load_from_file("FFF - Alcohol 120% 1.9.8.7507 kg.spc")
