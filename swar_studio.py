# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader

import numpy as np
import bisect
import struct
import zipfile

# -------------------------------------- DATA --------------------------------------

dtype_tokendata = np.dtype([
	('used', np.int32), 
	('type', np.int32), 
	('value', np.int32), 
	])

TOKEN_OBJ = 0x10
TOKEN_OBJ_END = 0x11

TOKEN_STR_START = 0x20
TOKEN_STR = 0x21
TOKEN_STR_END = 0x22

TOKEN_INT = 0x30
TOKEN_FLOAT = 0x31
TOKEN_ID = 0x32

types = {}
types[0x10] = "TOKEN_OBJ" 
types[0x11] = "TOKEN_OBJ_END" 

types[0x20] = "TOKEN_STR_START" 
types[0x21] = "TOKEN_STR" 
types[0x22] = "TOKEN_STR_END" 

types[0x30] = "TOKEN_INT" 
types[0x31] = "TOKEN_FLOAT" 
types[0x32] = "TOKEN_ID" 

ENABLE_PRINT = False

objnames = {}
objnames[32779] = 'String'
objnames[32808] = 'List'
objnames[322] = 'FX Plugin'
objnames[315] = 'Track'
objnames[325] = 'Track Send'
objnames[105] = 'Clip'

class swar_studio_data_object:
	def __init__(self):
		self.id = 0
		self.data = []

	def __iter__(self):
		if self.id == 32808: 
			for x in self.data[1:]:
				yield x
		else:
			for x in self.data:
				yield x

	def __repr__(self):
		if self.id == 32779: outdata = 'STRING: '+self.data[1]
		elif self.id == 40: outdata = 'DUALVAL: '+str(self.data)
		elif self.id == 32808: outdata = str(len(self.data)-1)+' items'
		else: outdata = str(len(self.data))+' items'

		objname = objnames[self.id]+' ('+str(self.id)+')' if self.id in objnames else self.id

		return '<'+str(objname)+' - '+outdata+'>'

	def __getitem__(self, i):
		return self.data.__getitem__(i)

	def is_iterable(self):
		if self.id == 32779: return False
		if self.id == 40: return False
		return True

class swar_studio_data_id:
	def __init__(self, iid): self.id = iid
	def __str__(self): return '@'+str(self.id)
	def __repr__(self): return '<ID - '+str(self.id)+'>'

class swar_studio_data_tokenmem:
	def __init__(self):
		self.data = np.zeros(0, dtype=dtype_tokendata)
		self.count = 0
		self.size = 0

	def get_cur(self):
		return self.data[self.count-1]

	def set_size(self, sized):
		self.data = np.zeros(sized, dtype=dtype_tokendata)

	def add(self, itype, ivalue, debug_char):
		if ENABLE_PRINT: print(self.count, hex(itype), ivalue, debug_char)
		curc = self.data[self.count]
		curc['used'] = 1
		curc['type'] = itype
		curc['value'] = ivalue
		self.count += 1
		self.size += 1

	def next(self):
		self.count += 1
		out = self.data[self.count-1]
		return out

	def getdata_string(self):
		out = ''
		while True:
			curc = self.next()
			if curc['type'] != TOKEN_STR_END: out += chr(curc['value'])
			else: break
		return out

	def getdata_object(self, curc):
		obj_data = swar_studio_data_object()
		obj_data.id = curc['value'] 
		while True:
			orgc, curc = self.getdata()
			if orgc['type'] == TOKEN_OBJ_END: 
				break
			else: 
				obj_data.data.append(curc)
		return obj_data

	def getdata(self):
		curc = self.next()
		if curc['type'] == TOKEN_INT: return curc, curc['value']
		elif curc['type'] == TOKEN_FLOAT: return curc, struct.unpack('>f', struct.pack('>i', curc['value']))[0]
		elif curc['type'] == TOKEN_STR_START: return curc, self.getdata_string()
		elif curc['type'] == TOKEN_OBJ: return curc, self.getdata_object(curc)
		elif curc['type'] == TOKEN_ID: return curc, swar_studio_data_id(curc['value'])
		else: return curc, curc

	def getroot(self):
		curc = self.next()
		if curc['type'] == TOKEN_INT: return curc['value']
		elif curc['type'] == TOKEN_FLOAT: return struct.unpack('>f', struct.pack('>i', curc['value']))[0]
		elif curc['type'] == TOKEN_STR_START: return self.getdata_string()
		elif curc['type'] == TOKEN_OBJ: return self.getdata_object(curc)
		elif curc['type'] == TOKEN_ID: return swar_studio_data_id(curc['value'])
		else: return curc

class swar_studio_data_main:
	def __init__(self):
		self.tokenmem = swar_studio_data_tokenmem()

	def __iter__(self):
		self.tokenmem.count = 0
		startd = self.tokenmem.getroot()
		for x in startd:
			iterd = False
			if isinstance(x, swar_studio_data_object): iterd = x.is_iterable()
			yield iterd, x

	def read__unescape_char(self, byr_stream):
		chard = byr_stream.raw(1)
		if chard == b'\\': 
			chardt = byr_stream.raw(1)
			if chardt == b'x': return bytes.fromhex(byr_stream.raw(2).decode())
			else: return chardt
		else: return chard

	def read__unescape_char_num(self, byr_stream):
		chard = byr_stream.uint8()
		if chard == 92: 
			chardt = byr_stream.uint8()
			if chardt == 120: return int(byr_stream.raw(2).decode(), 16)
			else: return chardt
		else: return chard

	def read__char(self, byr_stream, num):
		outbytes = b''
		for x in range(num): outbytes += self.read__unescape_char(byr_stream)
		return outbytes

	def read__var(self, byr_stream):
		outnum = b''
		while byr_stream.remaining():
			chard = self.read__char(byr_stream, 1)
			if chard == b'\n': break
			else: outnum += chard
		if not outnum: outnum = read__var(byr_stream)
		return outnum

	def read__num(self, byr_stream):
		return int(self.read__var(byr_stream))

	def read__printerr(self, byr_stream, message):
		print(message, end=' ')
		print('at line', bisect.bisect_left(self.foundent, byr_stream.tell()))
		exit()

	def read__part(self, byr_stream, is_string):
		char = byr_stream.raw(1)
		if char == b'\n': char = byr_stream.raw(1)
		if char == b':':
			self.tokenmem.add(TOKEN_OBJ, self.read__num(byr_stream), char)
			secchar = byr_stream.raw(1)
			if secchar == b'\n': secchar = byr_stream.raw(1)
			if secchar == b'\\':
				thirdchar = byr_stream.raw(1)
				if thirdchar != b'[': self.read__printerr(byr_stream, 'object must start with [')
		elif char == b'@':
			self.tokenmem.add(TOKEN_ID, self.read__num(byr_stream), char)
		elif char == b'\\':
			secchar = byr_stream.raw(1)
			if secchar == b']':
				self.tokenmem.add(TOKEN_OBJ_END, 0, secchar)
		elif char == b'"':
			count = self.tokenmem.get_cur()
			if count['type'] == TOKEN_INT:
				self.tokenmem.add(TOKEN_STR_START, 0, 0)
				for _ in range(count['value']):
					sch = self.read__unescape_char_num(byr_stream)
					if sch == 10: sch = self.read__unescape_char_num(byr_stream)
					self.tokenmem.add(TOKEN_STR, sch, sch)
				self.tokenmem.add(TOKEN_STR_END, 0, 0)
				char = byr_stream.raw(1)
				if char == b'\n': char = byr_stream.raw(1)
				if char != b'"': self.read__printerr(byr_stream, 'qoute expected')
			else: self.read__printerr(byr_stream, 'number is not before qoute')
		else:
			outnum = char
			while byr_stream.remaining():
				chard = self.read__unescape_char(byr_stream)
				if chard == b'\n': break
				else: outnum += chard
			outnum = outnum.decode()
			if outnum.replace('-','',1).isdigit():
				self.tokenmem.add(TOKEN_INT, int(outnum), outnum)
			else:
				numdata = struct.unpack('>i', struct.pack('>f', float(outnum)))[0]
				self.tokenmem.add(TOKEN_FLOAT, numdata, outnum)

	def debug_preview(self, rootdata, tabnum):
		for x in rootdata:
			print('   '*tabnum + '|', x)
			if isinstance(x, swar_studio_data_object):
				if x.is_iterable():
					self.debug_preview(x, tabnum+1)

	def debug_preview_root(self):
		self.tokenmem.count = 0
		startd = self.tokenmem.getroot()
		self.debug_preview(startd, 0)

	def load(self, data):
		data = data.replace(b'\r', b'')
		byr_stream = bytereader.bytereader()
		byr_stream.load_raw(data)
		self.foundent = [i for i, ltr in enumerate(data) if ltr == 10]
		self.tokenmem.set_size(len(data))
		while byr_stream.remaining(): self.read__part(byr_stream, False)

# -------------------------------------- PROJECT --------------------------------------

class swar_studio_clipsdata:
	def read(self, indata):
		for n, x in enumerate(indata):
			print(n, x)

class swar_studio_track:
	def read(self, indata):
		for n, x in enumerate(indata):
			#print(n, x)
			if n == 0: self.name = x
			if n == 1: self.muted = x
			if n == 2: self.__unk_2 = x
			if n == 3: self.solo = x
			if n == 4: self.__unk_4 = x
			if n == 5: self.__unk_5 = x
			if n == 6: self.__unk_6 = x
			if n == 7: self.__unk_7 = x
			if n == 8: self.__unk_8 = x
			if n == 9: self.__unk_9 = x
			if n == 10: self.__unk_10 = x
			if n == 11: self.__unk_11 = x
			if n == 12: self.__unk_12 = x
			if n == 13: self.__unk_13 = x
			if n == 14: self.__unk_14 = x
			if n == 15: self.__unk_15 = x
			if n == 16: self.__unk_16 = x
			if n == 17: self.__unk_17 = x
			if n == 18: self.__unk_18 = x
			if n == 19: self.__unk_19 = x
			if n == 20: self.__unk_20 = x
			if n == 21: self.__unk_21 = x
			if n == 22: self.__unk_22 = x
			if n == 23: self.__unk_23 = x
			if n == 24: self.id = x
			if n == 25: self.__unk_25 = x
			if n == 26: self.__unk_26 = x
			if n == 27: self.type = x
			if n == 28: self.__unk_28 = x
			if n == 29: self.plugindata = x
			if n == 30: self.__unk_30 = x
			if n == 31: self.__unk_31 = x
			if n == 32: self.__unk_32 = x
			if n == 33: self.__unk_33 = x
			if n == 34: self.clipdata = x
			if n == 35: self.__unk_35 = x
			if n == 36: self.__unk_36 = x
			if n == 37: self.__unk_37 = x
			if n == 38: self.__unk_38 = x
			if n == 39: self.volume = x
			if n == 40: self.pan = x
			if n == 41: self.pbr = x
			if n == 42: self.pitch = x
			if n == 43: self.pan_r = x
			if n == 44: self.__unk_44 = x
			if n == 45: self.__unk_45 = x
			if n == 46: self.__unk_46 = x
			if n == 47: self.__unk_47 = x
			if n == 48: self.sends = x
			if n == 49: self.icon = x
			if n == 50: self.display_gain_curve = x
			if n == 51: self.display_signal = x
			if n == 52: self.__unk_52 = x
			if n == 53: self.automation = x

class swar_studio_song:
	def __init__(self):
		self.__unk_0 = None
		self.__unk_1 = None
		self.tracks = []
		self.__unk_3 = None
		self.__unk_4 = None
		self.__unk_5 = None
		self.__unk_6 = None
		self.__unk_7 = None
		self.__unk_8 = None
		self.__unk_9 = None
		self.__unk_10 = None
		self.__unk_11 = None
		self.__unk_12 = None
		self.__unk_13 = None
		self.__unk_14 = None
		self.__unk_15 = None
		self.__unk_16 = None
		self.__unk_17 = None
		self.__unk_18 = None

	def load_from_file(self, input_file):
		songdata = swar_studio_data_main()
		self.zipfile = zipfile.ZipFile(input_file, 'r')
		zipdata = self.zipfile.read('Main.stc')
		infile = open(input_file, 'rb')
		songdata.load(self.zipfile.read('Main.stc'))

		songdata.debug_preview_root()

		for n, x in enumerate(songdata):
			if n == 0: self.__unk_0 = x
			if n == 1: self.__unk_1 = x
			if n == 2: 
				for track in x[1]:
					track_obj = swar_studio_track()
					track_obj.read(track)
			if n == 3: self.__unk_3 = x
			if n == 4: self.__unk_4 = x
			if n == 5: self.__unk_5 = x
			if n == 6: self.__unk_6 = x
			if n == 7: self.__unk_7 = x
			if n == 8: self.__unk_8 = x
			if n == 9: self.__unk_9 = x
			if n == 10: self.__unk_10 = x
			if n == 11: self.__unk_11 = x
			if n == 12: self.__unk_12 = x
			if n == 13: self.__unk_13 = x
			if n == 14: self.__unk_14 = x
			if n == 15: self.__unk_15 = x
			if n == 16: self.__unk_16 = x
			if n == 17: self.__unk_17 = x
			if n == 18: self.__unk_18 = x


apeinst_obj = swar_studio_song()
apeinst_obj.load_from_file("C:\\ProgramData\\Swar Studio Demo\\Songs\\testin.stz")
