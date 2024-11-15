# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import struct

VERBOSE_CHANNEL = True
VERBOSE_RACK = True
VERBOSE = True

def chunkview(byr_stream, chunk_obj, supported, numl, viewbytes):
	if supported == 0: supportedtxt = '#'
	if supported == 0.5: supportedtxt = '='
	if supported == 1: supportedtxt = ' '
	print(supportedtxt, '      '*numl, chunk_obj.id, str(chunk_obj.size).ljust(7), end='')
	if viewbytes: print(byr_stream.raw(min(chunk_obj.size, 32)))
	else: print()

def verify(byr_stream, magicnum, name):
	try: byr_stream.magic_check(magicnum)
	except ValueError as t: print('flm: '+name+' '+str(t))

def parse_chunks(byr_stream, size):
	startpos = byr_stream.tell()
	main_iff_obj = byr_stream.chunk_objmake()
	return main_iff_obj.iter(startpos, startpos+size)

class flm_rack_device_sampler_zone:
	def __init__(self, byr_stream):
		self.unk0 = byr_stream.uint8()
		self.unk1 = byr_stream.uint8()
		self.unk2 = byr_stream.uint8()
		self.unk3 = byr_stream.uint8()
		self.name = byr_stream.string(1020)

class flm_rack_device_sampler:
	def __init__(self, byr_stream, size, intype):
		self.zones = []
		self.path = None
		self.pth1 = None

		if intype == 1:
			verify(byr_stream, b'10WD', 'device_sampler')
	
			for chunk_obj in parse_chunks(byr_stream, size):
				if chunk_obj.id == b'ZONE':
					if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 0, 3, False)
					self.zones.append(flm_rack_device_sampler_zone(byr_stream))
				if chunk_obj.id == b'PATh':
					if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 0, 3, False)
					pathsize = byr_stream.uint32()
					self.pth1 = byr_stream.raw(4)
					self.path = byr_stream.string(pathsize-4)
				else:
					if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 0, 3, False)

class flm_rack_device:
	def __init__(self, byr_stream, size):
		self.type = byr_stream.uint32()
		self.order = byr_stream.uint32()

		self.type = None
		self.head_val_1 = None
		self.head_val_2 = None
		self.desc_name = None
		self.desc_name_2 = None
		self.preset_name = ''
		self.preset_path = ''
		self.add1 = None
		self.prms = None
		self.cstm = None
		self.pads = None
		self.minimized = 0

		self.wet_pan = 0.5
		self.mix = 1.0
		self.post_gain = 0.5

		for chunk_obj in parse_chunks(byr_stream, size):
			if chunk_obj.id == b'HEAD':
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 0.5, 2, False)
				self.type = byr_stream.int32()
				self.head_val_1 = byr_stream.int32()
				self.head_val_2 = byr_stream.int8()

			elif chunk_obj.id == b'DESC':
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 1, 2, False)
				self.desc_name = byr_stream.string(256)
				self.desc_name_2 = byr_stream.string(256)

			elif chunk_obj.id == b'PRST':
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 1, 2, False)
				self.preset_name = byr_stream.raw(byr_stream.uint32())
				self.preset_path = byr_stream.raw(byr_stream.uint32())

			elif chunk_obj.id == b'ADD1':
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 0.5, 2, False)
				self.minimized = byr_stream.int8()
				#self.add1 = byr_stream.raw(chunk_obj.size)

			elif chunk_obj.id == b'PRMS':
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 1, 2, False)
				self.prms = byr_stream.l_float(chunk_obj.size//4)

			elif chunk_obj.id == b'PADS':
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 0, 2, False)
				self.pads = byr_stream.raw(chunk_obj.size)

			elif chunk_obj.id == b'CSTM':
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 0, 2, False)
				flm_rack_device_sampler(byr_stream, chunk_obj.size, self.type)

			elif chunk_obj.id == b'SMPR':
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 1, 2, False)
				self.wet_pan = byr_stream.float()
				self.mix = byr_stream.float()
				self.post_gain = byr_stream.float()

			else:
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 0, 2, True)


class flm_rack:
	def __init__(self, byr_stream, size):
		self.header_val_0 = 0
		self.tracktype = 0
		self.id = 0
		self.target = 0

		self.volume = 0
		self.pan = 0
		self.mute = 0
		self.solo = 0
		self.param_val_4 = 0
		self.param_val_5 = 0

		byr_stream.skip(4)
		verify(byr_stream, b'10KR', 'rack')

		self.devices_sampler = []
		self.devices = []

		for chunk_obj in parse_chunks(byr_stream, size):

			if chunk_obj.id == b'RHED':
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 0.5, 1, False)
				self.header_val_0 = byr_stream.int32()
				self.tracktype = byr_stream.int32()
				self.id = byr_stream.int32()
				self.target = byr_stream.int32()

			elif chunk_obj.id == b'RPRM':
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 1, 1, False)
				self.volume = byr_stream.float()
				self.pan = byr_stream.float()
				self.mute = byr_stream.float()
				self.solo = byr_stream.float()
				self.param_val_4 = byr_stream.float()
				self.param_val_5 = byr_stream.float()

			elif chunk_obj.id == b'RSMP':
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 1, 1, False)
				self.devices_sampler.append( flm_rack_device(byr_stream, chunk_obj.size) )
			elif chunk_obj.id == b'RMOd':
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 1, 1, False)
				self.devices.append( flm_rack_device(byr_stream, chunk_obj.size) )
			else:
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 0, 1, True)

class flm_channel_evnt:
	def __init__(self, byr_stream, size, version):

		self.events = []

		if version == 1:
			for x in range(size//18):
				event = byr_stream.raw(18)
				unpstruct = struct.unpack('<Idhbbh', event)
				self.events.append(unpstruct)

		if version == 2:
			eventstruct = None
			self.chunksize = byr_stream.uint16()
			if self.chunksize == 19: eventstruct = '<Idhbbhb'
			numnotes = (size-2)//self.chunksize

			for x in range(numnotes):
				event = byr_stream.raw(self.chunksize)
				unpstruct = struct.unpack(eventstruct, event)
				self.events.append(unpstruct)

class flm_channel_clip_sample:
	def __init__(self, byr_stream, size):
		verify(byr_stream, b'20LS', 'clip sample')

		self.prms = []
		self.evn2 = None
		self.stretch_on = 0
		self.stretch_size = 1
		self.pitch = 1
		self.stretch_unk_1 = 0.5
		self.stretch_unk_2 = 0.5

		self.main_unk_1 = -1
		self.main_unk_2 = 0
		self.main_unk_3 = 0
		self.main_unk_4 = 1
		self.main_unk_5 = 0
		self.main_unk_6 = 0
		self.main_unk_7 = 0
		self.main_unk_8 = 0
		self.main_unk_9 = 1

		self.pth1 = b''
		self.sample_path = b''

		for chunk_obj in parse_chunks(byr_stream, size):

			if chunk_obj.id == b'EVN2':
				if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 0.5, 3, False)
				self.evn2 = flm_channel_evnt(byr_stream, chunk_obj.size, 2)
			elif chunk_obj.id == b'STRC':
				if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 0.5, 4, False)
				self.stretch_on = byr_stream.uint8()
				self.stretch_size = byr_stream.double()
				self.pitch = byr_stream.double()
				self.stretch_unk_1 = byr_stream.float()
				self.stretch_unk_2 = byr_stream.float()
			elif chunk_obj.id == b'PRMS':
				if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 1, 4, False)
				self.prms = byr_stream.l_float(chunk_obj.size//4)
			elif chunk_obj.id == b'MAIN':
				if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 0.5, 4, False)
				self.main_unk_1 = byr_stream.int32()
				self.main_unk_2 = byr_stream.int32()
				self.main_unk_3 = byr_stream.float()
				self.sample_name = byr_stream.raw(512)
				self.sample_folder = byr_stream.raw(512)
				self.main_unk_4 = byr_stream.int8()
				self.main_unk_5 = byr_stream.int32()
				self.main_unk_6 = byr_stream.int32()
				self.main_unk_7 = byr_stream.float()
				self.main_unk_8 = byr_stream.int8()
				self.main_unk_9 = byr_stream.int8()
			elif chunk_obj.id == b'PTH1':
				if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 0.5, 4, False)
				pathsize = byr_stream.uint16()
				self.pth1 = byr_stream.raw(4)
				self.sample_path = byr_stream.string(pathsize-4)
			else:
				if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 0, 4, True)

class flm_channel_clip:
	def __init__(self, byr_stream, size, auto_on):
		self.unk = byr_stream.uint32()
		self.evn2 = None
		self.evnt = None
		self.sample = None

		self.zoom_start = 0
		self.zoom_2 = 0
		self.zoom_3 = 0

		self.duration = 4
		self.loop_end = 4
		self.cut_start = 0

		header = byr_stream.raw(4)
		if header in [b'20LC', b'10LC']:
			for chunk_obj in parse_chunks(byr_stream, size):
				if chunk_obj.id == b'EVN2':
					if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 1, 3, False)
					self.evn2 = flm_channel_evnt(byr_stream, chunk_obj.size, 2)
				elif chunk_obj.id == b'EVNT':
					if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 1, 3, False)
					self.evn2 = flm_channel_evnt(byr_stream, chunk_obj.size, 1)
				elif chunk_obj.id == b'ZOOM':
					if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 1, 3, False)
					self.zoom_start = byr_stream.double()
					self.zoom_2 = byr_stream.double()
					self.zoom_3 = byr_stream.double()
				elif chunk_obj.id == b'CLSm':
					if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 1, 3, False)
					self.sample = flm_channel_clip_sample(byr_stream, chunk_obj.size)
				elif chunk_obj.id == b'CLHd':
					if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 1, 3, False)
					self.duration = byr_stream.double()
					self.loop_end = byr_stream.double()
					self.cut_start = byr_stream.double()
				elif chunk_obj.id == b'CLHD':
					if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 1, 3, False)
					self.duration = byr_stream.double()
					self.loop_end = byr_stream.double()
					self.cut_start = byr_stream.double()
				else:
					if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 0, 3, True)
		else:
			raise ProjectFileParserException("flm: Magic Check Failed: b'20LC' or b'10LC'")

class flm_channel_track:
	def __init__(self, byr_stream, size):

		self.clips = []
		self.auto_on = 0
		self.auto_device = 0
		self.auto_param = 0
		self.unk1 = 0
		self.unk2 = 0
		self.unk3 = 1
		self.hide_value = 0
		self.name = ''

		for chunk_obj in parse_chunks(byr_stream, size):
			if chunk_obj.id == b'CLIP':
				if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 1, 2, False)
				self.clips.append( flm_channel_clip(byr_stream, chunk_obj.size, self.auto_on) )
			elif chunk_obj.id == b'DESc':
				if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 1, 2, False)
				self.auto_on = byr_stream.uint32()
				self.auto_device = byr_stream.int32()
				self.auto_param = byr_stream.int32()
				self.unk1 = byr_stream.int32()
				self.unk2 = byr_stream.int32()
				self.unk3 = byr_stream.int32()
				self.hide_value = byr_stream.int32()
				self.name = byr_stream.string(1024)
			else:
				if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 0, 2, True)

class flm_channel:
	def __init__(self, byr_stream, size):

		self.name = ''
		self.tracknum = 0
		self.color = 0
		self.color_2 = 0
		self.unk1 = 0
		self.unk2 = 0

		self.version1 = byr_stream.uint16()
		self.version2 = byr_stream.uint16()

		header = byr_stream.raw(4)
		if header in [b'20HC', b'10HC']:
			for chunk_obj in parse_chunks(byr_stream, size):
				if chunk_obj.id == b'CHHD':
					if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 0.5, 1, False)
					self.name = byr_stream.raw(1024)
					self.tracknum = byr_stream.double()
					self.color = byr_stream.float()
					self.color_2 = byr_stream.float()
					self.unk1 = byr_stream.double()
					self.unk2 = byr_stream.double()
				elif chunk_obj.id == b'TRKH':
					if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 1, 1, False)
					flm_channel_track(byr_stream, chunk_obj.size)
				else:
					if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 0, 1, True)
		else:
			raise ProjectFileParserException("flm: Magic Check Failed: b'20HC' or b'10HC'")



class flm_project:
	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)

		self.timediv_num = 4
		self.timediv_denum = 4
		self.racks = []
		self.channels = []

		verify(byr_stream, b'10LF', 'main')

		for chunk_obj in parse_chunks(byr_stream, byr_stream.end):
			if chunk_obj.id == b'RACK':
				if VERBOSE_RACK: chunkview(byr_stream, chunk_obj, 1, 0, False)
				self.racks.append(flm_rack(byr_stream, chunk_obj.size))
			elif chunk_obj.id == b'CHNL':
				if VERBOSE_CHANNEL: chunkview(byr_stream, chunk_obj, 1, 0, False)
				self.channels.append(flm_channel(byr_stream, chunk_obj.size))
			elif chunk_obj.id == b'TDIV':
				if VERBOSE: chunkview(byr_stream, chunk_obj, 1, 0, False)
				self.timediv_num = byr_stream.int8()
				self.timediv_denum = byr_stream.int8()
			else:
				if VERBOSE: chunkview(byr_stream, chunk_obj, 0, 0, True)
