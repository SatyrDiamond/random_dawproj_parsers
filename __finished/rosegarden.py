# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

import xml.etree.ElementTree as ET
import gzip
import logging

dictprobe = []

def get_xml_tree(path):
	with open(path, 'rb') as file:
		try:
			data = gzip.decompress(file.read())
			return ET.fromstring(data)

		except:
			return ET.parse(path).getroot()

def property_get(indata, tagname):
	outdict = {}
	for x_part in indata:
		if x_part.tag == tagname:
			attrib = x_part.attrib
			attlist = list(attrib)
			if 'name' in attrib:
				name = attrib['name']
				if 'int' in attlist: outdict[name] = int(attrib['int'])
				elif 'string' in attlist: outdict[name] = attrib['string']
	return outdict

def property_make(xmldata, indata, tagname):
	for name, value in indata.items():
		tempd = ET.SubElement(xmldata, tagname)
		tempd.set('name', name)
		valtype = type(value)
		if valtype == str: tempd.set('string', value)
		if valtype == int: tempd.set('int', str(value))

def metadata_to_dict(xml_proj):
	out_dict = {}
	for xmlpart in xml_proj:
		if xmlpart.tag == 'property': out_dict[xmlpart.get('name')] = xmlpart.get('value')
	return out_dict

def dict_to_metadata(in_dict, xml_proj):
	tempxml = ET.SubElement(xml_proj, "metadata")
	for k, v in in_dict.items():
		metaxml = ET.SubElement(tempxml, "property")
		metaxml.set('name', k)
		metaxml.set('value', str(v))

def create_val(xml_proj, name, val):
	tempxml = ET.SubElement(xml_proj, name)
	tempxml.set('value', str(val))
	return tempxml

def bool_get(indata): return indata=='true'
def bool_make(indata): return 'true' if indata else 'false'

def float_get(val): return float(val) if '.' in val else int(val)

class rosegarden_event:
	def __init__(self, indata):
		self.type = ''
		self.subordering = 0
		self.absoluteTime = -1
		self.duration = 0
		self.timeOffset = 0
		self.prop = {}
		self.nprop = {}
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'type' in attribs: self.type = attribs['type']
		if 'subordering' in attribs: self.subordering = int(attribs['subordering'])
		if 'absoluteTime' in attribs: self.absoluteTime = int(attribs['absoluteTime'])
		if 'duration' in attribs: self.duration = int(attribs['duration'])
		if 'timeOffset' in attribs: self.timeOffset = int(attribs['timeOffset'])
		self.prop = property_get(indata, 'property')
		self.nprop = property_get(indata, 'nproperty')

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'event')
		tempd.set("type", self.type)
		if self.duration: tempd.set("duration", str(self.duration))
		if self.subordering: tempd.set("subordering", str(self.subordering))
		if self.absoluteTime != -1: tempd.set("absoluteTime", str(self.absoluteTime))
		if self.timeOffset: tempd.set("timeOffset", str(self.timeOffset))
		property_make(tempd, self.prop, 'property')
		property_make(tempd, self.nprop, 'nproperty')

class rosegarden_segment:
	def __init__(self, indata):
		self.track = 0
		self.start = 0
		self.label = ''
		self.endmarker = 0
		self.colourindex = 0
		self.transpose = 0
		self.rtdelaysec = 0
		self.rtdelaynsec = 0 
		self.repeat = False 
		self.fornotation = True 
		self.excludefromprinting = False 
		self.parts = []
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'track' in attribs: self.track = int(attribs["track"])
		if 'start' in attribs: self.start = int(attribs["start"])
		if 'label' in attribs: self.label = attribs["label"]
		if 'repeat' in attribs: self.repeat = bool_get(attribs["repeat"])
		if 'endmarker' in attribs: self.endmarker = int(attribs["endmarker"])
		if 'colourindex' in attribs: self.colourindex = int(attribs["colourindex"])
		if 'transpose' in attribs: self.transpose = int(attribs["transpose"])
		if 'rtdelaysec' in attribs: self.rtdelaysec = int(attribs["rtdelaysec"])
		if 'rtdelaynsec' in attribs: self.rtdelaynsec = int(attribs["rtdelaynsec"])
		if 'fornotation' in attribs: self.fornotation = bool_get(attribs["fornotation"])
		if 'excludefromprinting' in attribs: self.excludefromprinting = bool_get(attribs["excludefromprinting"])
		for x_part in indata:
			if x_part.tag == 'event': self.parts.append(['event', rosegarden_event(x_part)])
			elif x_part.tag == 'chord': self.parts.append(['chord', [rosegarden_event(x_inpart) for x_inpart in x_part if x_inpart.tag == 'event']])

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'segment')
		tempd.set("track", str(self.track))
		tempd.set("start", str(self.start))
		tempd.set("label", str(self.label))
		if self.repeat: tempd.set("repeat", bool_make(self.repeat))
		if self.transpose: tempd.set("transpose", str(self.transpose))
		if self.rtdelaysec or self.rtdelaynsec: 
			tempd.set("rtdelaysec", str(self.rtdelaysec))
			tempd.set("rtdelaynsec", str(self.rtdelaynsec))
		if self.colourindex: tempd.set("colourindex", str(self.colourindex))
		if self.endmarker: tempd.set("endmarker", str(self.endmarker))
		if self.fornotation != True: tempd.set("fornotation", bool_make(self.fornotation))
		if self.excludefromprinting != False: tempd.set("excludefromprinting", bool_make(self.repeat))
		for etype, edata in self.parts:
			if etype == 'event': edata.write(tempd)
			if etype == 'chord': 
				chordd = ET.SubElement(tempd, 'chord')
				for x in edata: x.write(chordd)

		xmatrix = ET.SubElement(tempd, 'matrix')
		xmatrix_hzoom = ET.SubElement(xmatrix, 'hzoom')
		xmatrix_hzoom.set('factor', '1')
		xmatrix_vzoom = ET.SubElement(xmatrix, 'vzoom')
		xmatrix_vzoom.set('factor', '1')
		xnotation = ET.SubElement(tempd, 'notation')

class rosegarden_track:
	def __init__(self, indata):
		self.id = 1
		self.label = ''
		self.shortLabel = ''
		self.position = 1
		self.muted = False
		self.archived = False
		self.solo = False
		self.instrument = 1000
		self.defaultLabel = ''
		self.defaultClef = 0
		self.defaultTranspose = 0
		self.defaultColour = 0
		self.defaultHighestPlayable = 127
		self.defaultLowestPlayable = 0
		self.staffSize = 0
		self.staffBracket = 0
		self.inputDevice = 10001
		self.inputChannel = 1
		self.thruRouting = 0
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'id' in attribs: self.id = int(attribs["id"])
		if 'label' in attribs: self.label = attribs["label"]
		if 'shortLabel' in attribs: self.shortLabel = attribs["shortLabel"]
		if 'position' in attribs: self.position = int(attribs["position"])
		if 'muted' in attribs: self.muted = bool_get(attribs["muted"])
		if 'archived' in attribs: self.archived = bool_get(attribs["archived"])
		if 'solo' in attribs: self.solo = bool_get(attribs["solo"])
		if 'instrument' in attribs: self.instrument = int(attribs["instrument"])
		if 'defaultLabel' in attribs: self.defaultLabel = attribs["defaultLabel"]
		if 'defaultClef' in attribs: self.defaultClef = int(attribs["defaultClef"])
		if 'defaultTranspose' in attribs: self.defaultTranspose = int(attribs["defaultTranspose"])
		if 'defaultColour' in attribs: self.defaultColour = int(attribs["defaultColour"])
		if 'defaultHighestPlayable' in attribs: self.defaultHighestPlayable = int(attribs["defaultHighestPlayable"])
		if 'defaultLowestPlayable' in attribs: self.defaultLowestPlayable = int(attribs["defaultLowestPlayable"])
		if 'staffSize' in attribs: self.staffSize = int(attribs["staffSize"])
		if 'staffBracket' in attribs: self.staffBracket = int(attribs["staffBracket"])
		if 'inputDevice' in attribs: self.inputDevice = int(attribs["inputDevice"])
		if 'inputChannel' in attribs: self.inputChannel = int(attribs["inputChannel"])
		if 'thruRouting' in attribs: self.thruRouting = int(attribs["thruRouting"])

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'track')
		tempd.set("id", str(self.id))
		tempd.set("label", str(self.label))
		tempd.set("shortLabel", str(self.shortLabel))
		tempd.set("position", str(self.position))
		tempd.set("muted", bool_make(self.muted))
		tempd.set("archived", bool_make(self.archived))
		tempd.set("solo", bool_make(self.solo))
		tempd.set("instrument", str(self.instrument))
		tempd.set("defaultLabel", str(self.defaultLabel))
		tempd.set("defaultClef", str(self.defaultClef))
		tempd.set("defaultTranspose", str(self.defaultTranspose))
		tempd.set("defaultColour", str(self.defaultColour))
		tempd.set("defaultHighestPlayable", str(self.defaultHighestPlayable))
		tempd.set("defaultLowestPlayable", str(self.defaultLowestPlayable))
		tempd.set("staffSize", str(self.staffSize))
		tempd.set("staffBracket", str(self.staffBracket))
		tempd.set("inputDevice", str(self.inputDevice))
		tempd.set("inputChannel", str(self.inputChannel))
		tempd.set("thruRouting", str(self.thruRouting))

class rosegarden_marker:
	def __init__(self, xml_proj):
		self.time = 0
		self.name = ''
		self.description = ''
		if xml_proj is not None: self.read(xml_proj)

	def read(self, xml_proj):
		trackattrib = xml_proj.attrib
		if 'time' in trackattrib: self.time = int(xml_proj.get('time'))
		if 'name' in trackattrib: self.name = xml_proj.get('name')
		if 'description' in trackattrib: self.description = xml_proj.get('description')

	def write(self, xml_proj):
		tempxml = ET.SubElement(xml_proj, "marker")
		if self.time is not None: tempxml.set('time', str(self.time))
		if self.name is not None: tempxml.set('name', str(self.name))
		if self.description is not None: tempxml.set('description', str(self.description))

class rosegarden_timesignature:
	def __init__(self, indata):
		self.time = 0
		self.numerator = 4
		self.denominator = 4
		self.hidden = False
		self.hiddenbars = False
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'time' in attribs: self.time = int(attribs['time'])
		if 'numerator' in attribs: self.numerator = int(attribs['numerator'])
		if 'denominator' in attribs: self.denominator = int(attribs['denominator'])
		if 'hidden' in attribs: self.hidden = bool_get(attribs['hidden'])
		if 'hiddenbars' in attribs: self.hiddenbars = bool_get(attribs['hiddenbars'])

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'timesignature')
		tempd.set("time", str(self.time))
		tempd.set("numerator", str(self.numerator))
		tempd.set("denominator", str(self.denominator))
		if self.hidden: tempd.set("hidden", bool_make(self.hidden))
		if self.hiddenbars: tempd.set("hiddenbars", bool_make(self.hiddenbars))

class rosegarden_tempo:
	def __init__(self, indata):
		self.time = 0
		self.bph = 0
		self.tempo = 0
		self.target = -1
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'time' in attribs: self.time = int(attribs['time'])
		if 'bph' in attribs: self.bph = int(attribs['bph'])
		if 'tempo' in attribs: self.tempo = int(attribs['tempo'])
		if 'target' in attribs: self.target = int(attribs['target'])

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'tempo')
		tempd.set("time", str(self.time))
		tempd.set("bph", str(self.bph))
		tempd.set("tempo", str(self.tempo))
		if self.target != -1: tempd.set("target", str(self.target))

class rosegarden_composition:
	def __init__(self, indata):
		self.tracks = []
		self.recordtracks = 0
		self.pointer = 0
		self.defaultTempo = 120.0000
		self.compositionDefaultTempo = 12000000
		self.islooping = 0
		self.loopmode = 0
		self.loopstart2 = 0
		self.loopend2 = 0
		self.startMarker = 0
		self.endMarker = 326400
		self.selected = 3
		self.playmetronome = 0
		self.recordmetronome = 1
		self.nexttriggerid = 0
		self.panlaw = 0
		self.notationspacing = 100
		self.editorfollowplayback = 1
		self.mainfollowplayback = 1
		self.timesignatures = []
		self.tempos = []
		self.markers = []
		self.metadata = {}
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'recordtracks' in attribs: self.recordtracks = attribs["recordtracks"]
		if 'pointer' in attribs: self.pointer = int(attribs["pointer"])
		if 'defaultTempo' in attribs: self.defaultTempo = float(attribs["defaultTempo"])
		if 'compositionDefaultTempo' in attribs: self.compositionDefaultTempo = int(attribs["compositionDefaultTempo"])
		if 'islooping' in attribs: self.islooping = int(attribs["islooping"])
		if 'loopmode' in attribs: self.loopmode = int(attribs["loopmode"])
		if 'loopstart2' in attribs: self.loopstart2 = int(attribs["loopstart2"])
		if 'loopend2' in attribs: self.loopend2 = attribs["loopend2"]
		if 'startMarker' in attribs: self.startMarker = int(attribs["startMarker"])
		if 'endMarker' in attribs: self.endMarker = int(attribs["endMarker"])
		if 'selected' in attribs: self.selected = int(attribs["selected"])
		if 'playmetronome' in attribs: self.playmetronome = int(attribs["playmetronome"])
		if 'recordmetronome' in attribs: self.recordmetronome = int(attribs["recordmetronome"])
		if 'nexttriggerid' in attribs: self.nexttriggerid = int(attribs["nexttriggerid"])
		if 'panlaw' in attribs: self.panlaw = int(attribs["panlaw"])
		if 'notationspacing' in attribs: self.notationspacing = int(attribs["notationspacing"])
		if 'editorfollowplayback' in attribs: self.editorfollowplayback = int(attribs["editorfollowplayback"])
		if 'mainfollowplayback' in attribs: self.mainfollowplayback = int(attribs["mainfollowplayback"])

		for x_part in indata:
			if x_part.tag == "tempo": self.tempos.append(rosegarden_tempo(x_part))
			if x_part.tag == "timesignature": self.timesignatures.append(rosegarden_timesignature(x_part))
			if x_part.tag == "track": self.tracks.append(rosegarden_track(x_part))
			if x_part.tag == "metadata": self.metadata = metadata_to_dict(x_part)
			if x_part.tag == "markers": 
				for x_inpart in x_part:
					if x_inpart.tag == 'marker': self.markers.append(rosegarden_marker(x_inpart))

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'composition')
		tempd.set("recordtracks", str(self.recordtracks))
		tempd.set("pointer", str(self.pointer))
		tempd.set("defaultTempo", '%.4f' % self.defaultTempo)
		tempd.set("compositionDefaultTempo", str(self.compositionDefaultTempo))
		tempd.set("islooping", str(self.islooping))
		tempd.set("loopmode", str(self.loopmode))
		tempd.set("loopstart2", str(self.loopstart2))
		tempd.set("loopend2", str(self.loopend2))
		tempd.set("startMarker", str(self.startMarker))
		tempd.set("endMarker", str(self.endMarker))
		tempd.set("selected", str(self.selected))
		tempd.set("playmetronome", str(self.playmetronome))
		tempd.set("recordmetronome", str(self.recordmetronome))
		tempd.set("nexttriggerid", str(self.nexttriggerid))
		tempd.set("panlaw", str(self.panlaw))
		tempd.set("notationspacing", str(self.notationspacing))
		tempd.set("editorfollowplayback", str(self.editorfollowplayback))
		tempd.set("mainfollowplayback", str(self.mainfollowplayback))
		for track in self.tracks: track.write(tempd)
		for timesignature in self.timesignatures: timesignature.write(tempd)
		for tempo in self.tempos: tempo.write(tempd)
		dict_to_metadata(self.metadata, tempd)
		markersd = ET.SubElement(tempd, 'markers')
		for marker in self.markers: marker.write(markersd)

class rosegarden_port:
	def __init__(self, indata):
		self.value = 0
		self.changed = 0
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'value' in attribs: self.value = float_get(attribs['value'])
		if 'changed' in attribs: self.changed = bool_get(attribs['changed'])

	def write(self, xmldata, idv):
		tempd = ET.SubElement(xmldata, 'port')
		tempd.set("id", str(idv))
		tempd.set("value", str(self.value))
		tempd.set("changed", bool_make(self.changed))

class rosegarden_plugin:
	def __init__(self, indata):
		self.position = -1
		self.identifier = ''
		self.bypassed = False
		self.ports = {}
		self.configure = {}
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'position' in attribs: self.position = int(attribs['position'])
		if 'identifier' in attribs: self.identifier = attribs['identifier']
		if 'bypassed' in attribs: self.bypassed = bool_get(attribs['bypassed'])
		for x_part in indata:
			if x_part.tag == 'port': self.ports[x_part.get('id')] = rosegarden_port(x_part)
			if x_part.tag == 'configure': self.configure[x_part.get('key')] = x_part.get('value')

	def write(self, xmldata, name):
		tempd = ET.SubElement(xmldata, name)
		if self.position != -1: tempd.set("position", str(self.position))
		tempd.set("identifier", str(self.identifier))
		tempd.set("bypassed", bool_make(self.bypassed))
		for idv, porto in self.ports.items(): porto.write(tempd, idv)
		for key, value in self.configure.items(): 
			keyd = ET.SubElement(tempd, 'configure')
			keyd.set('key', key)
			keyd.set('value', value)

class rosegarden_instrument_bank:
	def __init__(self, indata):
		self.send = False
		self.percussion = False
		self.msb = 0
		self.lsb = 0
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'send' in attribs: self.send = bool_get(attribs['send'])
		if 'percussion' in attribs: self.percussion = bool_get(attribs['percussion'])
		if 'msb' in attribs: self.msb = int(attribs['msb'])
		if 'lsb' in attribs: self.lsb = int(attribs['lsb'])

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'bank')
		tempd.set("send", bool_make(self.send))
		tempd.set("percussion", bool_make(self.percussion))
		tempd.set("msb", str(self.msb))
		tempd.set("lsb", str(self.lsb))

class rosegarden_instrument_program:
	def __init__(self, indata):
		self.send = False
		self.id = 0
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'send' in attribs: self.send = bool_get(attribs['send'])
		if 'id' in attribs: self.id = int(attribs['id'])

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'program')
		tempd.set("id", str(self.id))
		tempd.set("send", bool_make(self.send))

class rosegarden_instrument:
	def __init__(self, indata):
		self.id = 0
		self.channel = 1
		self.fixed = True
		self.type = ''
		self.pan = 100
		self.level = 0
		self.recordLevel = 0
		self.audioInput = 0
		self.audioInput_type = 'record'
		self.audioInput_channel = 0
		self.audioOutput = 0
		self.alias = ''
		self.synth = None
		self.bank = None
		self.program = None
		self.controlchange = {}
		self.plugins = []
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'id' in attribs: self.id = int(attribs['id'])
		if 'channel' in attribs: self.channel = int(attribs['channel'])
		if 'fixed' in attribs: self.fixed = bool_get(attribs['fixed'])
		if 'type' in attribs: self.type = attribs['type']
		for x_part in indata:
			partattribs = x_part.attrib
			if x_part.tag == 'pan': 
				if 'value' in partattribs: self.pan = int(partattribs['value'])
			if x_part.tag == 'level': 
				if 'value' in partattribs: self.level = int(partattribs['value'])
			if x_part.tag == 'recordLevel': 
				if 'value' in partattribs: self.recordLevel = float_get(partattribs['value'])
			if x_part.tag == 'audioInput': 
				if 'value' in partattribs: self.audioInput = int(partattribs['value'])
				if 'type' in partattribs: self.audioInput_type = partattribs['type']
				if 'channel' in partattribs: self.audioInput_channel = int(partattribs['channel'])
			if x_part.tag == 'audioOutput': 
				if 'value' in partattribs: self.audioOutput = int(partattribs['value'])
			if x_part.tag == 'alias': 
				if 'value' in partattribs: self.alias = partattribs['value']
			if x_part.tag == 'plugin': self.plugins.append(rosegarden_plugin(x_part))
			if x_part.tag == 'synth': self.synth = rosegarden_plugin(x_part)
			if x_part.tag == 'bank': self.bank = rosegarden_instrument_bank(x_part)
			if x_part.tag == 'program': self.program = rosegarden_instrument_program(x_part)
			if x_part.tag == 'controlchange': self.controlchange[int(partattribs['type'])] = int(partattribs['value'])

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'instrument')
		tempd.set("id", str(self.id))
		tempd.set("channel", str(self.channel))
		tempd.set("fixed", bool_make(self.fixed))
		tempd.set("type", self.type)
		if self.type in ['softsynth', 'audio']:
			create_val(tempd, 'pan', self.pan)
			create_val(tempd, 'level', self.level)
			create_val(tempd, 'recordLevel', self.recordLevel)
			audioInput = create_val(tempd, 'audioInput', self.audioInput)
			audioInput.set("type", self.audioInput_type)
			audioInput.set("channel", str(self.audioInput_channel))
			create_val(tempd, 'audioOutput', self.audioOutput)
			create_val(tempd, 'alias', self.alias)
			if self.synth is not None: self.synth.write(tempd, 'synth')
			for devobj in self.plugins: devobj.write(tempd, 'plugin')

		if self.type in ['midi']:
			if self.bank is not None: self.bank.write(tempd)
			if self.program is not None: self.program.write(tempd)
			for num, value in self.controlchange.items():
				xcontrolchange = ET.SubElement(tempd, 'controlchange')
				xcontrolchange.set("type", str(num))
				xcontrolchange.set("value", str(value))


class rosegarden_librarian:
	def __init__(self, indata):
		self.name = ''
		self.email = ''
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'name' in attribs: self.name = attribs['name']
		if 'email' in attribs: self.email = attribs['email']

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'librarian')
		tempd.set("name", str(self.name))
		tempd.set("email", str(self.email))

class rosegarden_metronome:
	def __init__(self, indata):
		self.instrument = 2009
		self.barpitch = 37
		self.beatpitch = 37
		self.subbeatpitch = 37
		self.depth = 2
		self.barvelocity = 120
		self.beatvelocity = 100
		self.subbeatvelocity = 80
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'instrument' in attribs: self.instrument = int(attribs['instrument'])
		if 'barpitch' in attribs: self.barpitch = int(attribs['barpitch'])
		if 'beatpitch' in attribs: self.beatpitch = int(attribs['beatpitch'])
		if 'subbeatpitch' in attribs: self.subbeatpitch = int(attribs['subbeatpitch'])
		if 'depth' in attribs: self.depth = int(attribs['depth'])
		if 'barvelocity' in attribs: self.barvelocity = int(attribs['barvelocity'])
		if 'beatvelocity' in attribs: self.beatvelocity = int(attribs['beatvelocity'])
		if 'subbeatvelocity' in attribs: self.subbeatvelocity = int(attribs['subbeatvelocity'])

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'metronome')
		tempd.set("instrument", str(self.instrument))
		tempd.set("barpitch", str(self.barpitch))
		tempd.set("beatpitch", str(self.beatpitch))
		tempd.set("subbeatpitch", str(self.subbeatpitch))
		tempd.set("depth", str(self.depth))
		tempd.set("barvelocity", str(self.barvelocity))
		tempd.set("beatvelocity", str(self.beatvelocity))
		tempd.set("subbeatvelocity", str(self.subbeatvelocity))

class rosegarden_program:
	def __init__(self, indata):
		self.id = ''
		self.name = ''
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'id' in attribs: self.id = int(attribs['id'])
		if 'name' in attribs: self.name = attribs['name']

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'program')
		tempd.set("id", str(self.id))
		tempd.set("name", str(self.name))

class rosegarden_bank:
	def __init__(self, indata):
		self.name = ''
		self.percussion = False
		self.msb = 0
		self.lsb = 0
		self.programs = []
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'name' in attribs: self.name = attribs['name']
		if 'percussion' in attribs: self.percussion = bool_get(attribs['percussion'])
		if 'msb' in attribs: self.msb = int(attribs['msb'])
		if 'lsb' in attribs: self.lsb = int(attribs['lsb'])
		for x_part in indata:
			partattribs = x_part.attrib
			if x_part.tag == 'program': self.programs.append(rosegarden_program(x_part))

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'bank')
		tempd.set("name", str(self.name))
		tempd.set("percussion", bool_make(self.percussion))
		tempd.set("msb", str(self.msb))
		tempd.set("lsb", str(self.lsb))
		for program in self.programs: program.write(tempd)

class rosegarden_control:
	def __init__(self, indata):
		self.name = "Expression"
		self.type = "controller"
		self.description = "none" 
		self.min = 0
		self.max = 127
		self.default = 127
		self.controllervalue = 11
		self.colourindex = 2
		self.ipbposition = 1
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'name' in attribs: self.name = attribs["name"]
		if 'type' in attribs: self.type = attribs["type"]
		if 'description' in attribs: self.description = attribs["description"]
		if 'min' in attribs: self.min = int(attribs["min"])
		if 'max' in attribs: self.max = int(attribs["max"])
		if 'default' in attribs: self.default = int(attribs["default"])
		if 'controllervalue' in attribs: self.controllervalue = int(attribs["controllervalue"])
		if 'colourindex' in attribs: self.colourindex = int(attribs["colourindex"])
		if 'ipbposition' in attribs: self.ipbposition = int(attribs["ipbposition"])

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'control')
		tempd.set("name", str(self.name))
		tempd.set("type", str(self.type))
		tempd.set("description", str(self.description))
		tempd.set("min", str(self.min))
		tempd.set("max", str(self.max))
		tempd.set("default", str(self.default))
		tempd.set("controllervalue", str(self.controllervalue))
		tempd.set("colourindex", str(self.colourindex))
		tempd.set("ipbposition", str(self.ipbposition))

class rosegarden_device:
	def __init__(self, indata):
		self.id = 0
		self.name = ''
		self.direction = ''
		self.variation = ''
		self.connection = ''
		self.type = ''
		self.instruments = []
		self.librarian = None
		self.metronome = None
		self.bank = None
		self.controls = None
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'id' in attribs: self.id = int(attribs['id'])
		if 'name' in attribs: self.name = attribs['name']
		if 'direction' in attribs: self.direction = attribs['direction']
		if 'variation' in attribs: self.variation = attribs['variation']
		if 'connection' in attribs: self.connection = attribs['connection']
		if 'type' in attribs: self.type = attribs['type']
		for x_part in indata:
			if x_part.tag == 'instrument': self.instruments.append(rosegarden_instrument(x_part))
			if x_part.tag == 'librarian': self.librarian = rosegarden_librarian(x_part)
			if x_part.tag == 'metronome': self.metronome = rosegarden_metronome(x_part)
			if x_part.tag == 'bank': self.bank = rosegarden_bank(x_part)
			if x_part.tag == 'controls': 
				self.controls = []
				for x_inpart in x_part:
					if x_inpart.tag == 'control': self.controls.append(rosegarden_control(x_inpart))

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'device')
		tempd.set("id", str(self.id))
		tempd.set("name", self.name)
		if self.type == 'midi':
			tempd.set("direction", self.direction)
			tempd.set("variation", self.variation)
			tempd.set("connection", self.connection)
		tempd.set("type", self.type)
		if self.librarian is not None: self.librarian.write(tempd)
		if self.metronome is not None: self.metronome.write(tempd)
		if self.bank is not None: self.bank.write(tempd)

		if self.controls is not None:
			controlsd = ET.SubElement(tempd, 'controls')
			for control in self.controls: control.write(controlsd)

		for instrument in self.instruments: instrument.write(tempd)

class rosegarden_studio:
	def __init__(self, indata):
		self.thrufilter = 0
		self.recordfilter = 0
		self.audioinputpairs = 2
		self.metronomedevice = 0
		self.amwshowaudiofaders = 1
		self.amwshowsynthfaders = 1
		self.amwshowaudiosubmasters = 1
		self.amwshowunassignedfaders = 0
		self.devices = []
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'thrufilter' in attribs: self.thrufilter = int(attribs["thrufilter"])
		if 'recordfilter' in attribs: self.recordfilter = int(attribs["recordfilter"])
		if 'audioinputpairs' in attribs: self.audioinputpairs = int(attribs["audioinputpairs"])
		if 'metronomedevice' in attribs: self.metronomedevice = int(attribs["metronomedevice"])
		if 'amwshowaudiofaders' in attribs: self.amwshowaudiofaders = int(attribs["amwshowaudiofaders"])
		if 'amwshowsynthfaders' in attribs: self.amwshowsynthfaders = int(attribs["amwshowsynthfaders"])
		if 'amwshowaudiosubmasters' in attribs: self.amwshowaudiosubmasters = int(attribs["amwshowaudiosubmasters"])
		if 'amwshowunassignedfaders' in attribs: self.amwshowunassignedfaders = int(attribs["amwshowunassignedfaders"])
		for x_part in indata:
			if x_part.tag == 'device': self.devices.append(rosegarden_device(x_part))

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'studio')
		tempd.set("thrufilter", str(self.thrufilter))
		tempd.set("recordfilter", str(self.recordfilter))
		tempd.set("audioinputpairs", str(self.audioinputpairs))
		tempd.set("metronomedevice", str(self.metronomedevice))
		tempd.set("amwshowaudiofaders", str(self.amwshowaudiofaders))
		tempd.set("amwshowsynthfaders", str(self.amwshowsynthfaders))
		tempd.set("amwshowaudiosubmasters", str(self.amwshowaudiosubmasters))
		tempd.set("amwshowunassignedfaders", str(self.amwshowunassignedfaders))
		for devobj in self.devices: devobj.write(tempd)

class rosegarden_colourpair:
	def __init__(self, indata):
		self.name = ''
		self.red = ''
		self.green = ''
		self.blue = ''
		if indata is not None: self.read(indata)

	def read(self, indata):
		attribs = indata.attrib
		if 'name' in attribs: self.name = attribs['name']
		if 'red' in attribs: self.red = int(attribs['red'])
		if 'green' in attribs: self.green = int(attribs['green'])
		if 'blue' in attribs: self.blue = int(attribs['blue'])

	def write(self, xmldata, idv):
		tempd = ET.SubElement(xmldata, 'colourpair')
		tempd.set("id", str(idv))
		tempd.set("name", str(self.name))
		tempd.set("red", str(self.red))
		tempd.set("green", str(self.green))
		tempd.set("blue", str(self.blue))

class rosegarden_appearance:
	def __init__(self, indata):
		self.colourmaps = {}
		if indata is not None: self.read(indata)

	def read(self, indata):
		for x_part in indata:
			if x_part.tag == "colourmap":
				outpair = {}
				for x_inpart in x_part:
					if x_inpart.tag == 'colourpair': outpair[int(x_inpart.get('id'))] = rosegarden_colourpair(x_inpart)
				self.colourmaps[x_part.get('name')] = outpair
				
	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'appearance')
		for name, data in self.colourmaps.items():
			xcolourpair = ET.SubElement(tempd, 'colourmap')
			for idv, pairdata in data.items():
				pairdata.write(xcolourpair, idv)
			xcolourpair.set('name', name)


class rosegarden_song:
	def __init__(self):
		self.segments = []
		self.composition = rosegarden_composition(None)
		self.studio = rosegarden_studio(None)
		self.appearance = rosegarden_appearance(None)

	def load_from_file(self, input_file):
		x_root = get_xml_tree(input_file)
		for x_part in x_root:
			print(x_part.tag)
			if x_part.tag == "composition": self.composition.read(x_part)
			if x_part.tag == "studio": self.studio.read(x_part)
			if x_part.tag == "appearance": self.appearance.read(x_part)
			if x_part.tag == "segment": self.segments.append(rosegarden_segment(x_part))

		outfile = ET.ElementTree(x_root)
		ET.indent(outfile)
		outfile.write("in.xml", xml_declaration = True)

	def save_to_file(self, out_file):
		rosegarden_proj = ET.Element("rosegarden-data")
		rosegarden_proj.set("version", "22.12.1")
		rosegarden_proj.set("format-version-major", "1")
		rosegarden_proj.set("format-version-minor", "6")
		rosegarden_proj.set("format-version-point", "9")

		self.composition.write(rosegarden_proj)
		for segment in self.segments: segment.write(rosegarden_proj)
		self.studio.write(rosegarden_proj)
		self.appearance.write(rosegarden_proj)

		outfile = ET.ElementTree(rosegarden_proj)
		ET.indent(outfile)
		outfile.write(out_file, xml_declaration = True)

apeinst_obj = rosegarden_song()
apeinst_obj.load_from_file("dd.rg")
apeinst_obj.save_to_file("out.xml")
