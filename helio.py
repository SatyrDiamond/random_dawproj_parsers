# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
from objects.binary_fmt import juce_binaryxml
import logging

class helio_note:
	def __init__(self, bx_part):
		self.id = ''
		self.key = 0
		self.ts = 0
		self.len = 0
		self.vol = 0
		if bx_part is not None: self.read(bx_part)

	def read(self, bx_part):
		attrib = bx_part.get_attrib_native()
		if 'id' in attrib: self.id = attrib['id']
		if 'key' in attrib: self.key = attrib['key']
		if 'ts' in attrib: self.ts = attrib['ts']
		if 'len' in attrib: self.len = attrib['len']
		if 'vol' in attrib: self.vol = attrib['vol']

class helio_clip:
	def __init__(self, bx_part):
		self.id = ''
		self.key = 0
		self.ts = 0
		self.vol = 1024
		if bx_part is not None: self.read(bx_part)

	def read(self, bx_part):
		attrib = bx_part.get_attrib_native()
		if 'id' in attrib: self.id = attrib['id']
		if 'key' in attrib: self.key = attrib['key']
		if 'ts' in attrib: self.ts = attrib['ts']
		if 'vol' in attrib: self.vol = attrib['vol']

class helio_event:
	def __init__(self, bx_part):
		self.id = ''
		self.value = 0
		self.curve = 0.5
		self.ts = 0
		if bx_part is not None: self.read(bx_part)

	def read(self, bx_part):
		attrib = bx_part.get_attrib_native()
		if 'id' in attrib: self.id = attrib['id']
		if 'value' in attrib: self.value = attrib['value']
		if 'curve' in attrib: self.curve = attrib['curve']
		if 'ts' in attrib: self.ts = attrib['ts']

class helio_node:
	def __init__(self, bx_part):
		self.vcsId = None
		self.type = None
		self.name = None
		self.trackId = None
		self.colour = None
		self.channel = 0
		self.controller = 0
		self.notes = []
		self.clips = []
		self.events = []
		if bx_part is not None: self.read(bx_part)

	def read(self, bx_part):
		attrib = bx_part.get_attrib_native()
		if 'vcsId' in attrib: self.vcsId = attrib['vcsId']
		if 'type' in attrib: self.type = attrib['type']
		if 'name' in attrib: self.name = attrib['name']
		if 'trackId' in attrib: self.trackId = attrib['trackId']
		if 'colour' in attrib: self.colour = attrib['colour']
		if 'channel' in attrib: self.channel = attrib['channel']
		if 'controller' in attrib: self.controller = attrib['controller']

		for x in bx_part.children:
			if x.tag == 'track': 
				for inpart in x.children:
					if inpart.tag == 'note': self.notes.append(helio_note(inpart))
			elif x.tag == 'pattern': 
				for inpart in x.children:
					if inpart.tag == 'clip': self.clips.append(helio_clip(inpart))
			elif x.tag == 'automation': 
				for inpart in x.children:
					if inpart.tag == 'event': self.events.append(helio_event(inpart))
			else: print('    ', x.tag, len(x.children))

class helio_song:
	def __init__(self):
		self.vcsId = ''
		self.projectTimeStamp = ''
		self.license = ''
		self.author = ''
		self.description = ''
		self.nodes = []

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)

		self.rootele = juce_binaryxml.juce_binaryxml_element()
		self.rootele.read_byr(byr_stream)

		for bx_part in self.rootele.children:
			if bx_part.tag == "projectInfo":
				attrib = bx_part.get_attrib_native()
				if "vcsId" in attrib: self.vcsId = attrib['vcsId']
				if "projectTimeStamp" in attrib: self.projectTimeStamp = attrib['projectTimeStamp']
				if "license" in attrib: self.license = attrib['license']
				if "author" in attrib: self.author = attrib['author']
				if "description" in attrib: self.description = attrib['description']
			if bx_part.tag == "node":
				self.nodes.append(helio_node(bx_part))

apeinst_obj = helio_song()
apeinst_obj.load_from_file("G:\\Documents\\Helio\\riseshine_midi.helio")
