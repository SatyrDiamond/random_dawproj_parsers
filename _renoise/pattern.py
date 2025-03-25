# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

import xml.etree.ElementTree as ET

from _renoise import device
from _renoise import pattern
from _renoise import func
strbool = func.strbool
maketxtsub = func.maketxtsub
get_int_comma = func.get_int_comma
make_int_comma = func.make_int_comma

# --------------------------------------------------------- LINES ---------------------------------------------------------

class renoise_pattern_effectcolumn:
	def __init__(self):
		self.value = ''
		self.number = ''

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'Value': self.value = xpart.text
			if xpart.tag == 'Number': self.number = xpart.text

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'EffectColumn')
		if self.value: maketxtsub(tempd, 'Value', str(self.value))
		if self.number: maketxtsub(tempd, 'Number', str(self.number))

class renoise_pattern_notecolumn:
	def __init__(self):
		self.note = ''
		self.instrument = ''
		self.volume = ''

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'Note': self.note = xpart.text
			if xpart.tag == 'Instrument': self.instrument = xpart.text
			if xpart.tag == 'Volume': self.volume = xpart.text

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'NoteColumn')
		if self.note: maketxtsub(tempd, 'Note', str(self.note))
		if self.instrument: maketxtsub(tempd, 'Instrument', str(self.instrument))
		if self.volume: maketxtsub(tempd, 'Volume', str(self.volume))

class renoise_pattern_line:
	def __init__(self):
		self.data = {}
		self.notecolumns = []
		self.effectcolumns = []

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'NoteColumns': 
				for xinpart in xpart:
					if xinpart.tag == 'NoteColumn':
						notecolumn_obj = renoise_pattern_notecolumn()
						notecolumn_obj.read(xinpart)
						self.notecolumns.append(notecolumn_obj)
			if xpart.tag == 'EffectColumns': 
				for xinpart in xpart:
					if xinpart.tag == 'EffectColumn':
						effectcolumn_obj = renoise_pattern_effectcolumn()
						effectcolumn_obj.read(xinpart)
						self.effectcolumns.append(effectcolumn_obj)

	def write(self, xmldata, index):
		tempd = ET.SubElement(xmldata, 'Line')
		tempd.set('index', str(index))
		NoteColumns = ET.SubElement(tempd, 'NoteColumns')
		for notecolumn_obj in self.notecolumns: notecolumn_obj.write(NoteColumns)
		EffectColumns = ET.SubElement(tempd, 'EffectColumns')
		for effectcolumn_obj in self.effectcolumns: effectcolumn_obj.write(EffectColumns)

class renoise_pattern_lines:
	def __init__(self):
		self.data = {}

	def read(self, xmldata):
		for xpart in xmldata:
			attrib = xpart.attrib
			if 'index' in attrib:
				line_obj = renoise_pattern_line()
				line_obj.read(xpart)
				self.data[int(attrib['index'])] = line_obj

	def write(self, xmldata):
		if self.data:
			tempd = ET.SubElement(xmldata, 'Lines')
			for index, line_obj in self.data.items():
				line_obj.write(tempd, index)

# --------------------------------------------------------- SEQUENCE ---------------------------------------------------------

class renoise_pattern_automations_envelope:
	def __init__(self):
		self.DeviceIndex = 0
		self.ParameterIndex = 0
		self.Envelope = device.renoise_envelope()

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'DeviceIndex': self.DeviceIndex = int(xpart.text)
			if xpart.tag == 'ParameterIndex': self.ParameterIndex = int(xpart.text)
			if xpart.tag == 'Envelope': self.Envelope.read(xpart)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'Envelope')
		maketxtsub(tempd, 'DeviceIndex', str(self.DeviceIndex))
		maketxtsub(tempd, 'ParameterIndex', str(self.ParameterIndex))
		self.Envelope.write(tempd, 'Envelope')

class renoise_pattern_automations:
	def __init__(self):
		self.Envelopes = []

	def __getitem__(self, v):
		return self.Envelopes.__getitem__(v)
		
	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'Envelopes': 
				for xinpart in xpart:
					if xinpart.tag == 'Envelope':
						envelope_obj = renoise_pattern_automations_envelope()
						envelope_obj.read(xinpart)
						self.Envelopes.append(envelope_obj)

	def write(self, xmldata):
		if self.Envelopes:
			tempd = ET.SubElement(xmldata, 'Automations')
			patxml = ET.SubElement(tempd, 'Envelopes')
			for envelope_obj in self.Envelopes: envelope_obj.write(patxml)

class renoise_pattern_patterntrack:
	def __init__(self):
		self.type = ''
		self.SelectedPresetName = ''
		self.SelectedPresetIsModified = False
		self.Lines = pattern.renoise_pattern_lines()
		self.AliasPatternIndex = -1
		self.ColorEnabled = False
		self.Color = [0,0,0]
		self.Automations = renoise_pattern_automations()

	def read(self, xmldata):
		self.type = xmldata.tag
		for xpart in xmldata:
			if xpart.tag == 'SelectedPresetName': self.SelectedPresetName = xpart.text
			if xpart.tag == 'SelectedPresetIsModified': self.SelectedPresetIsModified = xpart.text=='true'
			if xpart.tag == 'Lines': self.Lines.read(xpart)
			if xpart.tag == 'AliasPatternIndex': self.AliasPatternIndex = int(xpart.text)
			if xpart.tag == 'ColorEnabled': self.ColorEnabled = xpart.text=='true'
			if xpart.tag == 'Color': self.Color = get_int_comma(xpart.text)
			if xpart.tag == 'Automations': self.Automations.read(xpart)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, self.type)
		tempd.set('type', self.type)
		maketxtsub(tempd, 'SelectedPresetName', self.SelectedPresetName)
		maketxtsub(tempd, 'SelectedPresetIsModified', strbool(self.SelectedPresetIsModified))
		self.Lines.write(tempd)
		maketxtsub(tempd, 'AliasPatternIndex', str(self.AliasPatternIndex))
		maketxtsub(tempd, 'ColorEnabled', strbool(self.SelectedPresetIsModified))
		maketxtsub(tempd, 'Color', make_int_comma(self.Color))
		self.Automations.write(tempd)

class renoise_pattern_pattern:
	def __init__(self):
		self.Name = None
		self.NumberOfLines = 4
		self.Tracks = []

	def __getitem__(self, v):
		return self.Tracks.__getitem__(v)

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'NumberOfLines': self.NumberOfLines = int(xpart.text)
			if xpart.tag == 'Name': self.Name = xpart.text
			if xpart.tag == 'Tracks': 
				for xinpart in xpart:
					patterntrack_obj = renoise_pattern_patterntrack()
					patterntrack_obj.read(xinpart)
					self.Tracks.append(patterntrack_obj)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'Pattern')
		if self.Name is not None: maketxtsub(tempd, 'Name', str(self.Name))
		maketxtsub(tempd, 'NumberOfLines', str(self.NumberOfLines))
		patxml = ET.SubElement(tempd, 'Tracks')
		for track_obj in self.Tracks: track_obj.write(patxml)

class renoise_pattern_patternpool:
	def __init__(self):
		self.HighliteStep = 0
		self.DefaultPatternLength = 64
		self.Patterns = []

	def __getitem__(self, v):
		return self.Patterns.__getitem__(v)

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'HighliteStep': self.HighliteStep = int(xpart.text)
			if xpart.tag == 'DefaultPatternLength': self.DefaultPatternLength = int(xpart.text)
			if xpart.tag == 'Patterns': 
				for xinpart in xpart:
					if xinpart.tag == 'Pattern':
						pattern_obj = renoise_pattern_pattern()
						pattern_obj.read(xinpart)
						self.Patterns.append(pattern_obj)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'PatternPool')
		maketxtsub(tempd, 'HighliteStep', str(self.HighliteStep))
		maketxtsub(tempd, 'DefaultPatternLength', str(self.DefaultPatternLength))

		patxml = ET.SubElement(tempd, 'Patterns')
		for pattern_obj in self.Patterns: pattern_obj.write(patxml)
