# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import zlib
import logging

class sunvox_pattern:
	def __init__(self):
		self.is_clone = False
		self.clone_source = -1
		self.data = b''
		self.name = ''
		self.number_of_tracks = 0
		self.number_of_lines = 0
		self.height = 0
		self.appearance_flags = []
		self.icon = b''
		self.color_foreground = []
		self.color_background = []
		self.flags = []
		self.pos_x = 0
		self.pos_y = 0

class sunvox_song:
	def __init__(self):
		self.version = []
		self.bversion = []
		self.bpm = 120
		self.global_vol = 0
		self.speed = 0
		self.timegrid = 0
		self.timegrid2 = 0
		self.name = ''
		self.modules_scale = 0
		self.modules_zoom = 0
		self.modules_x_offset = 0
		self.modules_y_offset = 0
		self.modules_layer_mask = 0
		self.modules_current_layer = 0
		self.current_timeline_position = 0
		self.restart_position = 0
		self.index_of_last_selected_module = 0
		self.index_of_last_selected_generator_module = 0
		self.pat_cursor_index = 0
		self.pat_cursor_trackindex = 0
		self.pat_cursor_lineindex = 0
		self.patterns = []

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)

		_curpat = None

		main_iff_obj = byr_stream.chunk_objmake()
		for chunk_obj in main_iff_obj.iter(0, byr_stream.end):
			#print(chunk_obj.id)
			if chunk_obj.id == b'SVOX':
				pass 
			elif chunk_obj.id == b'VERS': self.version = byr_stream.l_uint8(4)
			elif chunk_obj.id == b'BVER': self.bversion = byr_stream.uint32()
			elif chunk_obj.id == b'BPM ': self.bpm = byr_stream.uint32()
			elif chunk_obj.id == b'GVOL': self.global_vol = byr_stream.uint32()
			elif chunk_obj.id == b'SPED': self.speed = byr_stream.uint32()
			elif chunk_obj.id == b'TGRD': self.timegrid = byr_stream.uint32()
			elif chunk_obj.id == b'TGD2': self.timegrid2 = byr_stream.uint32()
			elif chunk_obj.id == b'NAME': self.name = byr_stream.string_t()
			elif chunk_obj.id == b'MSCL': self.modules_scale = byr_stream.uint32()
			elif chunk_obj.id == b'MZOO': self.modules_zoom = byr_stream.uint32()
			elif chunk_obj.id == b'MXOF': self.modules_x_offset = byr_stream.int32()
			elif chunk_obj.id == b'MYOF': self.modules_y_offset = byr_stream.int32()
			elif chunk_obj.id == b'LMSK': self.modules_layer_mask = byr_stream.uint32()
			elif chunk_obj.id == b'CURL': self.modules_current_layer = byr_stream.uint32()
			elif chunk_obj.id == b'TIME': self.current_timeline_position = byr_stream.int32()
			elif chunk_obj.id == b'REPS': self.restart_position = byr_stream.int32()
			elif chunk_obj.id == b'SELS': self.index_of_last_selected_module = byr_stream.uint32()
			elif chunk_obj.id == b'LGEN': self.index_of_last_selected_generator_module = byr_stream.uint32()
			elif chunk_obj.id == b'PATN': self.pat_cursor_index = byr_stream.uint32()
			elif chunk_obj.id == b'PATT': self.pat_cursor_trackindex = byr_stream.uint32()
			elif chunk_obj.id == b'PATL': self.pat_cursor_lineindex = byr_stream.uint32()
			elif chunk_obj.id == b'PDTA': 
				if not _curpat:
					pattern_obj = sunvox_pattern()
					self.patterns.append(pattern_obj)
					_curpat = pattern_obj
					#print('new pattern: normal')

			elif chunk_obj.id == b'PNME': _curpat.name = byr_stream.string_t()
			elif chunk_obj.id == b'PCHN': _curpat.number_of_tracks = byr_stream.uint32()
			elif chunk_obj.id == b'PLIN': _curpat.number_of_lines = byr_stream.uint32()
			elif chunk_obj.id == b'PYSZ': _curpat.height = byr_stream.uint32()
			elif chunk_obj.id == b'PFLG': _curpat.appearance_flags = byr_stream.flags32()
			elif chunk_obj.id == b'PICO': _curpat.icon = byr_stream.raw(32)
			elif chunk_obj.id == b'PFGC': _curpat.color_foreground = byr_stream.l_uint8(3)
			elif chunk_obj.id == b'PBGC': _curpat.color_background = byr_stream.l_uint8(3)
			elif chunk_obj.id == b'PFFF': _curpat.flags = byr_stream.flags32()
			elif chunk_obj.id == b'PXXX': _curpat.pos_x = byr_stream.int32()
			elif chunk_obj.id == b'PYYY': _curpat.pos_y = byr_stream.int32()
			elif chunk_obj.id == b'PEND': _curpat = None
			elif chunk_obj.id == b'PPAR': 
				if not _curpat:
					pattern_obj = sunvox_pattern()
					self.patterns.append(pattern_obj)
					_curpat = pattern_obj
					_curpat.is_clone = True
					_curpat.clone_source = byr_stream.uint32()
					#print('new pattern: clone')
			elif chunk_obj.id == b'SFFF':
				print(chunk_obj.id)

			else:
				print('UNKNOWN CHUNK', chunk_obj.id)
				break

		exit()

apeinst_obj = sunvox_song()
apeinst_obj.load_from_file("G:\\RandomMusicFiles\\tracker_lessknown\\sunvox\\Philip Bergwerf - Venaya.sunvox")
