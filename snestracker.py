# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import logging


def readchunks(byr_stream, start, end):
	main_iff_obj = byr_stream.chunk_objmake()
	main_iff_obj.set_sizes_num(1, 2, False)
	for chunk_obj in main_iff_obj.iter(start, end):
		yield(chunk_obj)


class snestracker_sample:
	def __init__(self):
		self.index = 0
		self.data = b''
		self.name = ''
		self.rel_loop = 0
		self.finetune = 0
		self.semitone_offset = 0

	def load(self, byr_stream, size):
		curpos = byr_stream.tell()
		for chunk_obj in readchunks(byr_stream, curpos, curpos+size):
			if chunk_obj.id == 1: self.index = byr_stream.uint8()
			elif chunk_obj.id == 3: self.data = byr_stream.raw(chunk_obj.size)
			elif chunk_obj.id == 2: self.name = byr_stream.string(chunk_obj.size)
			elif chunk_obj.id == 0: self.rel_loop = byr_stream.uint16()
			elif chunk_obj.id == 4: 
				self.finetune = byr_stream.uint8()
				self.semitone_offset = byr_stream.uint8()


class snestracker_inst:
	def __init__(self):
		self.index = 0
		self.srcn = 0
		self.flags = 0
		self.name = ''
		self.vol = 0
		self.pan = 0
		self.adsr = 0
		self.finetune = 0

	def load(self, byr_stream, size):
		curpos = byr_stream.tell()
		for chunk_obj in readchunks(byr_stream, curpos, curpos+size):
			if chunk_obj.id == 1: 
				self.index = byr_stream.uint8()
				self.srcn = byr_stream.uint8()
				self.flags = byr_stream.uint8()
			elif chunk_obj.id == 2: self.name = byr_stream.string(chunk_obj.size)
			elif chunk_obj.id == 0: 
				self.vol = byr_stream.uint8()
				self.pan = byr_stream.uint8()
				self.adsr = byr_stream.uint16()
			elif chunk_obj.id == 3: self.finetune = byr_stream.string(chunk_obj.size)

class snestracker_track:
	def __init__(self):
		self.type = 0
		self.index = 0
		self.data = 0

	def load(self, byr_stream, size):
		curpos = byr_stream.tell()
		for chunk_obj in readchunks(byr_stream, curpos, curpos+size):
			if chunk_obj.id == 0:
				self.type = byr_stream.uint8()
				self.index = byr_stream.uint8()
			elif chunk_obj.id == 1:
				self.data = byr_stream.raw(chunk_obj.size)

class snestracker_pattern:
	def __init__(self):
		self.index = 0
		self.len = 0
		self.name = 0
		self.tracks = {}

	def load(self, byr_stream, size):
		curpos = byr_stream.tell()
		for chunk_obj in readchunks(byr_stream, curpos, curpos+size):
			if chunk_obj.id == 0:
				self.index = byr_stream.uint8()
				self.len = byr_stream.uint8()
			elif chunk_obj.id == 2:
				self.name = byr_stream.string(chunk_obj.size)
			elif chunk_obj.id == 1:
				track_obj = snestracker_track()
				track_obj.load(byr_stream, chunk_obj.size)
				self.tracks[track_obj.index] = track_obj

class snestracker_patseq:
	def __init__(self):
		self.entries = []

	def load(self, byr_stream, size):
		curpos = byr_stream.tell()
		for chunk_obj in readchunks(byr_stream, curpos, curpos+size):
			if chunk_obj.id == 1:
				self.entries = byr_stream.l_uint8(chunk_obj.size)

class snestracker_songsettings:
	def __init__(self):
		self.name = []
		self.bpm = 140
		self.spd = 16
		self.mvol = 0
		self.evol = 0
		self.edl = 0
		self.efb = 0

	def load(self, byr_stream, size):
		curpos = byr_stream.tell()
		for chunk_obj in readchunks(byr_stream, curpos, curpos+size):
			if chunk_obj.id == 0:
				self.name = byr_stream.string(chunk_obj.size)
			elif chunk_obj.id == 1:
				speeddata = byr_stream.uint16()
				self.bpm = speeddata >> 6
				self.spd = speeddata & 0b111111
			elif chunk_obj.id == 2:
				self.mvol = byr_stream.uint8()
				self.evol = byr_stream.uint8()
				self.edl = byr_stream.uint8()
				self.efb = byr_stream.uint8()

class snestracker_version:
	def __init__(self):
		self.version = []
		self.appver = []

	def load(self, byr_stream, size):
		curpos = byr_stream.tell()
		for chunk_obj in readchunks(byr_stream, curpos, curpos+size):
			if chunk_obj.id == 0:
				self.version = byr_stream.l_uint16(3)
				self.appver = byr_stream.l_uint16(3)

class snestracker_song:
	def __init__(self):
		self.samples = {}
		self.instruments = {}
		self.patterns = {}
		self.version = snestracker_version()
		self.patseq = snestracker_patseq()
		self.songsettings = snestracker_songsettings()

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)

		byr_stream.magic_check(b'STSong')

		for chunk_obj in readchunks(byr_stream, byr_stream.tell(), byr_stream.end):
			if chunk_obj.id == 1:
				samp_obj = snestracker_sample()
				samp_obj.load(byr_stream, chunk_obj.size)
				self.samples[samp_obj.index] = samp_obj

			elif chunk_obj.id == 2:
				inst_obj = snestracker_inst()
				inst_obj.load(byr_stream, chunk_obj.size)
				self.instruments[inst_obj.index] = inst_obj

			elif chunk_obj.id == 3:
				pat_obj = snestracker_pattern()
				pat_obj.load(byr_stream, chunk_obj.size)
				self.patterns[inst_obj.index] = pat_obj

			elif chunk_obj.id == 4:
				self.patseq.load(byr_stream, chunk_obj.size)

			elif chunk_obj.id == 0:
				self.songsettings.load(byr_stream, chunk_obj.size)

			elif chunk_obj.id == 5:
				self.version.load(byr_stream, chunk_obj.size)

apeinst_obj = snestracker_song()
apeinst_obj.load_from_file("G:\\RandomMusicFiles\\tracker_sampler\\SNES Tracker v0.2.4-Win64\\demosongs\\dddd.sts")
