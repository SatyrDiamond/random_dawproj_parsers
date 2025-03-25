# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
from objects.data_bytes import bytewriter
import logging

idlist = {}
idlist['49076c4d1623d21186b000c04f8edb8a'] = 'Track'
idlist['276cd4690b7fd211871700c04f8edb8a'] = 'Track:Audio:Info'
idlist['3e0c0223541dfc44aab68330c9121f22'] = 'Track:MIDI:Info'
idlist['6a208d162123d21186b000c04f8edb8a'] = 'Track:Region'
idlist['d0fb0bbbaec4044685662b4bf9cccbb5'] = 'TrackS:Folder'
idlist['2b959c4d344c664295f519126b4420a8'] = 'TrackS:Track'
idlist['9d74b872ab14884594a939343aeef7cc'] = 'MixerChannel'
idlist['a132b74c04e40d498806ede87d7d2c4f'] = 'Track:Groove'
idlist['5c1b70846368d21186fd00c04f8edb8a'] = 'Track:Automation'
idlist['1b1ce45016af194e8cdba707237b7921'] = 'GrooveInfo'

class sony_acid_chunk:
	def __init__(self):
		self.id = None
		self.size = 0
		self.start = 0
		self.end = 0
		self.is_list = False
		self.in_data = []

	def read(self, byr_stream, tnum):
		self.id = byr_stream.raw(16)
		self.size = byr_stream.uint64()-24
		self.start = byr_stream.tell_real()
		self.is_list = self.id[0:4] in [b'riff', b'list']

		if self.is_list:
			print('\t'*tnum, '$Group \\')
			self.id = byr_stream.raw(16)
			with byr_stream.isolate_size(self.size-16, True) as bye_stream: 
				while bye_stream.remaining():
					inchunk = sony_acid_chunk()
					inchunk.read(bye_stream, tnum+1)
					self.in_data.append(inchunk)
			print('\t'*tnum, '       /')

		else:
			idname = self.id.hex()

			if idname == 'dd':
				print(byr_stream.raw(self.size))
			else:
				byr_stream.skip(self.size)

			if idname in idlist: idname = idlist[idname]
			print('\t'*tnum,  idname)

class sony_acid_song:
	def __init__(self):
		self.root = sony_acid_chunk()

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)

		root = sony_acid_chunk()
		root.read(byr_stream, 0)

apeinst_obj = sony_acid_song()
apeinst_obj.load_from_file("G:\\RandomMusicFiles\\old\\acid_pro\\acid 4\\Hybrid.acd")
