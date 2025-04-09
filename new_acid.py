# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
from objects.data_bytes import bytewriter
import logging

# ---------------------- CHUNKS ----------------------

class chunk__unknown_peak:
	def __init__(self, byr_stream):
		self.unknowndata = []
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int64() )
		self.unknowndata.append( byr_stream.int64() )
		self.unknowndata.append( byr_stream.int64() )
		self.unknowndata.append( byr_stream.int64() )
		self.unknowndata.append( byr_stream.int64() )
		self.unknowndata.append( byr_stream.int64() )
		self.unknowndata.append( byr_stream.float() )
		self.unknowndata.append( byr_stream.int32() )

class chunk__peak:
	def __init__(self, byr_stream):
		self.unknowndata = []
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int64() )
		self.unknowndata.append( byr_stream.float() )

class chunk__region:
	def __init__(self, byr_stream):
		self.header = []
		self.header.append( byr_stream.int32() )
		self.header.append( byr_stream.int32() )
		self.flags = byr_stream.flags64()
		self.unknowndata = []
		self.pos = byr_stream.int64()
		self.size = byr_stream.int64()
		self.offset = byr_stream.int64()
		self.pitch = byr_stream.double()
		self.unknowndata.append( byr_stream.double() )
		self.unknowndata.append( byr_stream.int64() )
		self.unknowndata.append( byr_stream.int64() )
		self.index = byr_stream.int64()
		self.unknowndata.append( byr_stream.int64() )
		self.fade_in = byr_stream.int64()
		self.fade_out = byr_stream.int64()
		self.gain = byr_stream.float()
		self.unknowndata.append( byr_stream.int32() )
		self.fade_in_type = byr_stream.int32()
		self.fade_out_type = byr_stream.int32()
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		#print(self.header, self.unknowndata, byr_stream.rest().hex() )

class chunk__maindata:
	def __init__(self, byr_stream):
		self.unknowndata = []
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.double() )
		self.unknowndata.append( byr_stream.double() )
		self.unknowndata.append( byr_stream.int64() )
		self.unknowndata.append( byr_stream.int16() )
		self.unknowndata.append( byr_stream.int16() )
		byr_stream.skip(88)
		if byr_stream.remaining(): self.unknowndata.append( byr_stream.int64() )
		if byr_stream.remaining(): self.unknowndata.append( byr_stream.int32() )
		if byr_stream.remaining(): self.unknowndata.append( byr_stream.string16_t() )
		if byr_stream.remaining(): self.unknowndata.append( byr_stream.string16_t() )
		if byr_stream.remaining(): self.unknowndata.append( byr_stream.string16_t() )
		if byr_stream.remaining(): self.unknowndata.append( byr_stream.string16_t() )
		if byr_stream.remaining(): self.unknowndata.append( byr_stream.string16_t() )
		if byr_stream.remaining(): self.unknowndata.append( byr_stream.string16_t() )
		if byr_stream.remaining(): self.unknowndata.append( byr_stream.string16_t() )
		if byr_stream.remaining(): self.unknowndata.append( byr_stream.string16_t() )

class chunk__track_data:
	def __init__(self, byr_stream):
		self.unknowndata = []
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.flags = byr_stream.flags32()
		self.size = byr_stream.int32()
		self.type = byr_stream.int32()
		self.color = byr_stream.int32()
		self.id = byr_stream.int32()
		string_size = byr_stream.int32()
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.numaudio = byr_stream.int32()
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.raw(string_size).decode("utf-16") )

class chunk__audioinfo:
	def __init__(self, byr_stream):
		self.unknowndata = []
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.vol = byr_stream.float()
		self.pan = byr_stream.float()
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.float() )
		self.unknowndata.append( byr_stream.int32() )

		self.arrayd = []
		for _ in range(32):
			p = []
			p.append(byr_stream.uint64())
			p.append(byr_stream.uint64())
			self.arrayd.append(p)

		self.send_data = []
		for _ in range(26):
			p = []
			p.append(byr_stream.uint32())
			p.append(byr_stream.float())
			p.append(byr_stream.uint64())
			self.send_data.append(p)

		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.audio_device = byr_stream.int32()
		self.audio_subdevice = byr_stream.int32()
		self.monitor = byr_stream.int32()
		self.unknowndata.append( byr_stream.float() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.arrayd2 = byr_stream.l_float(60)
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )
		self.unknowndata.append( byr_stream.int32() )

class chunk__unknown:
	def __init__(self, byr_stream):
		self.unknowndata = []
		print(self.unknowndata, byr_stream.rest().hex() )

chunksdef = {}
chunksdef['52a1a0b25e05754486f15d78af15a056'] = chunk__unknown_peak
chunksdef['754be33a5ef5ec44a2f0f4eb3c53af7d'] = chunk__peak
chunksdef['6a208d162123d21186b000c04f8edb8a'] = chunk__region
chunksdef['5a2d8fb20f23d21186af00c04f8edb8a'] = chunk__maindata
chunksdef['49076c4d1623d21186b000c04f8edb8a'] = chunk__track_data
chunksdef['276cd4690b7fd211871700c04f8edb8a'] = chunk__audioinfo

# ---------------------- INDATA ----------------------

VERBOSE = True

verboseid = {}
verboseid['5a2d8fb20f23d21186af00c04f8edb8a'] = 'MainData'
verboseid['49076c4d1623d21186b000c04f8edb8a'] = 'Track:Data'
verboseid['276cd4690b7fd211871700c04f8edb8a'] = 'Track:Audio:Info'
verboseid['3e0c0223541dfc44aab68330c9121f22'] = 'Track:MIDI:Info'
verboseid['6a208d162123d21186b000c04f8edb8a'] = 'Track:Region'
verboseid['d0fb0bbbaec4044685662b4bf9cccbb5'] = 'TrackS:Folder'
verboseid['2b959c4d344c664295f519126b4420a8'] = 'TrackS:Track'
verboseid['9d74b872ab14884594a939343aeef7cc'] = 'MixerChannel'
verboseid['a132b74c04e40d498806ede87d7d2c4f'] = 'Track:Groove'
verboseid['5c1b70846368d21186fd00c04f8edb8a'] = 'Track:Automation'
verboseid['1b1ce45016af194e8cdba707237b7921'] = 'GrooveInfo'
verboseid['b5c7e0971f2d46449de8c07ff6f43b3b'] = 'RegionData'
verboseid['5662f7ab2d39d21186c700c04f8edb8a'] = 'Marker'
verboseid['754be33a5ef5ec44a2f0f4eb3c53af7d'] = 'Peak'

verboseid['44030abfa7f8f44788cba63c7756ba9e'] = 'AudioDef:Info'

verboseid['a95c808a7402c242b8b9572f6786317c'] = 'Group:AudioDef'
verboseid['5b2d8fb20f23d21186af00c04f8edb8a'] = 'Group:RegionDatas'
verboseid['a59e8054b89bcd458d2b3ef94586a8e0'] = 'Group:GroovePool'
verboseid['48076c4d1623d21186b000c04f8edb8a'] = 'Group:Track'
verboseid['47076c4d1623d21186b000c04f8edb8a'] = 'Group:TrackList'
verboseid['e42b0d22d37fd211871800c04f8edb8a'] = 'Group:Mixer'
verboseid['f40e02902d39d21186c700c04f8edb8a'] = 'Group:Markers'
verboseid['172d16be624d2c48b80bfcf30fa53b02'] = 'Group:Peaks'

class sony_acid_chunk:
	def __init__(self):
		self.id = None
		self.size = 0
		self.start = 0
		self.end = 0
		self.is_list = False
		self.in_data = []
		self.def_data = None

	def read(self, byr_stream, tnum):
		self.id = byr_stream.raw(16)
		self.size = byr_stream.uint64()-24
		self.start = byr_stream.tell_real()
		self.is_list = self.id[0:4] in [b'riff', b'list']

		if self.is_list:
			self.id = byr_stream.raw(16)
			gidname = self.id.hex()
			if gidname in verboseid: gidname = verboseid[gidname]
			if VERBOSE: print('\t'*tnum, '$Group %s \\' % gidname)
			with byr_stream.isolate_size(self.size-16, True) as bye_stream: 
				while bye_stream.remaining():
					inchunk = sony_acid_chunk()
					inchunk.read(bye_stream, tnum+1)
					self.in_data.append(inchunk)
			if VERBOSE: print('\t'*tnum, '       /')

		else:
			idname = self.id.hex()

			if idname in chunksdef: 
				with byr_stream.isolate_size(self.size, True) as bye_stream:
					self.def_data = chunksdef[idname](bye_stream)
				#print(byr_stream.raw(self.size).hex())
			else:
				byr_stream.skip(self.size)

			if idname in verboseid: idname = verboseid[idname]
			if VERBOSE: print('\t'*tnum,  idname)

class sony_acid_song:
	def __init__(self):
		self.root = sony_acid_chunk()

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)

		root = sony_acid_chunk()
		root.read(byr_stream, 0)

apeinst_obj = sony_acid_song()
apeinst_obj.load_from_file("Hybrid.acd")
