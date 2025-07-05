# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import logging
import numpy as np

def valprint(tabv, txt, val, **k):
	print(('\t'*tabv)+txt.rjust(8), val, **k)

VERBOSE = True

def decode_value_debug(byr_stream, tabnum):
	vtype = byr_stream.uint8()
	if vtype == 2: 
		value = byr_stream.int32()
		if VERBOSE: valprint(tabnum, 'INT32', value)
	elif vtype == 3: 
		value = byr_stream.uint64()
		if VERBOSE: valprint(tabnum, 'UINT64', value)
	elif vtype == 4: 
		value = byr_stream.float()
		if VERBOSE: valprint(tabnum, 'FLOAT', value)
	elif vtype == 5: 
		value = byr_stream.double()
		if VERBOSE: valprint(tabnum, 'DOUBLE', value)
	elif vtype == 6: 
		value = byr_stream.uint16()
		if VERBOSE: valprint(tabnum, 'UINT16', value)
	elif vtype == 7: 
		value = byr_stream.string(byr_stream.uint32())
		if VERBOSE: valprint(tabnum, 'STRING', value)
	elif vtype == 8: 
		value = byr_stream.raw(byr_stream.uint32())
		if VERBOSE: valprint(tabnum, 'RAW', value)
	elif vtype == 9: 
		if VERBOSE: valprint(tabnum, '>>DICT>>', '')
		numparts = byr_stream.uint32()
		value = dict([
			[
			decode_value(byr_stream, tabnum+1)[1], 
			decode_value(byr_stream, tabnum+1)] for _ in range(numparts)
			])
	elif vtype == 10: 
		if VERBOSE: valprint(tabnum, '>>LIST>>', '')
		numparts = byr_stream.uint32()
		value = [decode_value(byr_stream, tabnum+1) for _ in range(numparts)]
	else: 
		print('unknown type', vtype)
		exit()
	return vtype, value

def decode_value_1way(byr_stream):
	vtype = byr_stream.uint8()
	if vtype == 2: 
		return byr_stream.int32()
	elif vtype == 3: 
		return byr_stream.uint64()
	elif vtype == 4: 
		return byr_stream.float()
	elif vtype == 5: 
		return byr_stream.double()
	elif vtype == 6: 
		return byr_stream.uint16()
	elif vtype == 7: 
		return byr_stream.string(byr_stream.uint32())
	elif vtype == 8: 
		return byr_stream.raw(byr_stream.uint32())
	elif vtype == 9: 
		numparts = byr_stream.uint32()
		value = dict([
			[
			decode_value_1way(byr_stream), 
			decode_value_1way(byr_stream)] for _ in range(numparts)
			])
		return value
	elif vtype == 10: 
		numparts = byr_stream.uint32()
		return [decode_value_1way(byr_stream) for _ in range(numparts)]
	else: 
		print('unknown type', vtype)
		exit()

class soundop_song:
	def __init__(self):
		self.maindata = {}

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)

		byr_stream.magic_check(b'$$mcrootv0000$$')
		self.maindata = decode_value_1way(byr_stream)

apeinst_obj = soundop_song()
apeinst_obj.load_from_file("G:\\Projects\\parser_tobe\\soundop\\Mixspace 1\\Mixspace 18.msf")
