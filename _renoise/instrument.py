# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from _renoise import pattern
from _renoise import device
import xml.etree.ElementTree as ET

from _renoise import func
strbool = func.strbool
maketxtsub = func.maketxtsub
get_int_comma = func.get_int_comma
make_int_comma = func.make_int_comma

class renoise_triggeroptions:
	def __init__(self):
		self.BaseNote = 48
		self.KeyTracking = 'Transpose'
		self.Loop = True
		self.LoopStart = 0
		self.LoopEnd = 32

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'BaseNote': self.BaseNote = int(xpart.text)
			if xpart.tag == 'KeyTracking': self.KeyTracking = xpart.text
			if xpart.tag == 'Loop': self.Loop = xpart.text=='true'
			if xpart.tag == 'LoopStart': self.LoopStart = int(xpart.text)
			if xpart.tag == 'LoopEnd': self.LoopEnd = int(xpart.text)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'TriggerOptions')
		maketxtsub(tempd, 'BaseNote', str(self.BaseNote))
		maketxtsub(tempd, 'KeyTracking', self.KeyTracking)
		maketxtsub(tempd, 'Loop', strbool(self.Loop))
		maketxtsub(tempd, 'LoopStart', str(self.LoopStart))
		maketxtsub(tempd, 'LoopEnd', str(self.LoopEnd))

# --------------------------------------------------------- PHRASEMAP ---------------------------------------------------------

class renoise_instrument_phrasemap_mapping:
	def __init__(self):
		self.PhraseIndex = 0
		self.NoteRangeStart = 0
		self.NoteRangeEnd = 0
		self.TriggerOptions = renoise_triggeroptions()

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'PhraseIndex': self.PhraseIndex = int(xpart.text)
			if xpart.tag == 'NoteRangeStart': self.NoteRangeStart = int(xpart.text)
			if xpart.tag == 'NoteRangeEnd': self.NoteRangeEnd = int(xpart.text)
			if xpart.tag == 'TriggerOptions': self.TriggerOptions.read(xpart)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'Mapping')
		maketxtsub(tempd, 'PhraseIndex', str(self.PhraseIndex))
		maketxtsub(tempd, 'NoteRangeStart', str(self.NoteRangeStart))
		maketxtsub(tempd, 'NoteRangeEnd', str(self.NoteRangeEnd))
		self.TriggerOptions.write(tempd)

class renoise_instrument_phrasemap:
	def __init__(self):
		self.SelectedMappingIndex = 0
		self.Mappings = []

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'SelectedMappingIndex': self.SelectedMappingIndex = int(xpart.text)

			if xpart.tag == 'Mappings':
				for xinpart in xpart:
					if xinpart.tag == 'Mapping':
						map_obj = renoise_instrument_phrasemap_mapping()
						map_obj.read(xinpart)
						self.Mappings.append(map_obj)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'PhraseMap')
		if self.Mappings:
			xmlmappings = ET.SubElement(tempd, 'Mappings')
			for map_obj in self.Mappings: map_obj.write(xmlmappings)
		maketxtsub(tempd, 'SelectedMappingIndex', str(self.SelectedMappingIndex))

# --------------------------------------------------------- PHRASE ---------------------------------------------------------

class renoise_instrument_phrase:
	def __init__(self):
		self.SelectedPresetName = ""
		self.SelectedPresetIsModified = "Linear"
		self.Lines = pattern.renoise_pattern_lines()
		self.Name = "Phrase"
		self.Autoseek = True
		self.LinesPerBeat = 4
		self.ShuffleIsActive = False
		self.shuffleamounts = []
		self.NumberOfLines = 16
		self.VisibleNoteColumns = 2
		self.VisibleEffectColumns = 1
		self.NoteColumnNames = []
		self.NoteColumnStates = []
		self.InstrumentColumnIsVisible = False
		self.VolumeColumnIsVisible = True
		self.PanningColumnIsVisible = False
		self.DelayColumnIsVisible = False
		self.SampleEffectsColumnIsVisible = True
		self.TriggerOptions = renoise_triggeroptions()

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'SelectedPresetName': self.SelectedPresetName = xpart.text
			if xpart.tag == 'SelectedPresetIsModified': self.SelectedPresetIsModified = xpart.text=='true'
			if xpart.tag == 'Lines': self.Lines.read(xpart)
			if xpart.tag == 'Name': self.Name = xpart.text
			if xpart.tag == 'Autoseek': self.Autoseek = xpart.text=='true'
			if xpart.tag == 'LinesPerBeat': self.LinesPerBeat = xpart.text
			if xpart.tag == 'ShuffleIsActive': self.ShuffleIsActive = xpart.text=='true'
			if xpart.tag == 'ShuffleAmounts': 
				for xinpart in xpart:
					if xinpart.tag == 'ShuffleAmount': 
						self.shuffleamounts.append(int(xinpart.text))
			if xpart.tag == 'NumberOfLines': self.NumberOfLines = int(xpart.text)
			if xpart.tag == 'VisibleNoteColumns': self.VisibleNoteColumns = int(xpart.text)
			if xpart.tag == 'VisibleEffectColumns': self.VisibleEffectColumns = int(xpart.text)
			if xpart.tag == 'NoteColumnNames': 
				for xinpart in xpart:
					if xinpart.tag == 'NoteColumnName': 
						self.NoteColumnNames.append(xinpart.text)
			if xpart.tag == 'NoteColumnStates': 
				for xinpart in xpart:
					if xinpart.tag == 'NoteColumnState': 
						self.NoteColumnStates.append(xinpart.text)
			if xpart.tag == 'InstrumentColumnIsVisible': self.InstrumentColumnIsVisible = xpart.text=='true'
			if xpart.tag == 'VolumeColumnIsVisible': self.VolumeColumnIsVisible = xpart.text=='true'
			if xpart.tag == 'PanningColumnIsVisible': self.PanningColumnIsVisible = xpart.text=='true'
			if xpart.tag == 'DelayColumnIsVisible': self.DelayColumnIsVisible = xpart.text=='true'
			if xpart.tag == 'SampleEffectsColumnIsVisible': self.SampleEffectsColumnIsVisible = xpart.text=='true'
			if xpart.tag == 'TriggerOptions': self.TriggerOptions.read(xpart)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'Phrase')
		maketxtsub(tempd, 'SelectedPresetName', str(self.SelectedPresetName))
		maketxtsub(tempd, 'SelectedPresetIsModified', strbool(self.SelectedPresetIsModified))
		self.Lines.write(tempd)
		maketxtsub(tempd, 'Name', str(self.Name))
		maketxtsub(tempd, 'Autoseek', strbool(self.Autoseek))
		maketxtsub(tempd, 'LinesPerBeat', str(self.LinesPerBeat))
		maketxtsub(tempd, 'ShuffleIsActive', strbool(self.ShuffleIsActive))
		ShuffleAmounts = ET.SubElement(tempd, 'ShuffleAmounts')
		for x in self.shuffleamounts: maketxtsub(ShuffleAmounts, 'ShuffleAmount', str(x))
		maketxtsub(tempd, 'NumberOfLines', str(self.NumberOfLines))
		maketxtsub(tempd, 'VisibleNoteColumns', str(self.VisibleNoteColumns))
		maketxtsub(tempd, 'VisibleEffectColumns', str(self.VisibleEffectColumns))
		NoteColumnNames = ET.SubElement(tempd, 'NoteColumnNames')
		for x in self.NoteColumnNames: maketxtsub(NoteColumnNames, 'NoteColumnName', x)
		NoteColumnStates = ET.SubElement(tempd, 'NoteColumnStates')
		for x in self.NoteColumnStates: maketxtsub(NoteColumnStates, 'NoteColumnState', x)
		maketxtsub(tempd, 'InstrumentColumnIsVisible', strbool(self.InstrumentColumnIsVisible))
		maketxtsub(tempd, 'VolumeColumnIsVisible', strbool(self.VolumeColumnIsVisible))
		maketxtsub(tempd, 'PanningColumnIsVisible', strbool(self.PanningColumnIsVisible))
		maketxtsub(tempd, 'DelayColumnIsVisible', strbool(self.DelayColumnIsVisible))
		maketxtsub(tempd, 'SampleEffectsColumnIsVisible', strbool(self.SampleEffectsColumnIsVisible))
		self.TriggerOptions.write(tempd)

class renoise_instrument_phrasegenerator:
	def __init__(self):
		self.PlaybackSync = False
		self.PlaybackMode = 'Keymap'
		self.SelectedPhraseIndex = 0
		self.Phrases = []
		self.PhraseMap = renoise_instrument_phrasemap()

	def __getitem__(self, v):
		return self.Phrases.__getitem__(v)
		
	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'PlaybackSync': self.PlaybackSync = xpart.text=='true'
			if xpart.tag == 'PlaybackMode': self.PlaybackMode = xpart.text
			if xpart.tag == 'SelectedPhraseIndex': self.SelectedPhraseIndex = int(xpart.text)
			if xpart.tag == 'PhraseMap': self.PhraseMap.read(xpart)

			if xpart.tag == 'Phrases':
				for xinpart in xpart:
					if xinpart.tag == 'Phrase':
						phrase_obj = renoise_instrument_phrase()
						phrase_obj.read(xinpart)
						self.Phrases.append(phrase_obj)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'PhraseGenerator')
		maketxtsub(tempd, 'PlaybackSync', strbool(self.PlaybackSync))
		maketxtsub(tempd, 'PlaybackMode', str(self.PlaybackMode))
		maketxtsub(tempd, 'SelectedPhraseIndex', str(self.SelectedPhraseIndex))
		if self.Phrases:
			xmlmappings = ET.SubElement(tempd, 'Phrases')
			for phrase_obj in self.Phrases: phrase_obj.write(xmlmappings)
		self.PhraseMap.write(tempd)

# --------------------------------------------------------- MACRO ---------------------------------------------------------

class renoise_instrument_macro_mappings:
	def __init__(self):
		self.DestChainType = None
		self.DestChainIndex = None
		self.DestDeviceIndex = 1
		self.DestParameterIndex = 1
		self.Min = 0
		self.Max = 1
		self.Scaling = "Linear"

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'DestChainType': self.DestChainType = xpart.text
			if xpart.tag == 'DestChainIndex': self.DestChainIndex = int(xpart.text)
			if xpart.tag == 'DestDeviceIndex': self.DestDeviceIndex = int(xpart.text)
			if xpart.tag == 'DestParameterIndex': self.DestParameterIndex = int(xpart.text)
			if xpart.tag == 'Min': self.Min = float(xpart.text)
			if xpart.tag == 'Max': self.Max = float(xpart.text)
			if xpart.tag == 'Scaling': self.Scaling = xpart.text

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'Mapping')
		if self.DestChainType is not None: 
			maketxtsub(tempd, 'DestChainType', str(self.DestChainType))
		if self.DestChainIndex is not None: 
			maketxtsub(tempd, 'DestChainIndex', str(self.DestChainIndex))
		maketxtsub(tempd, 'DestDeviceIndex', str(self.DestDeviceIndex))
		maketxtsub(tempd, 'DestParameterIndex', str(self.DestParameterIndex))
		maketxtsub(tempd, 'Min', str(self.Min))
		maketxtsub(tempd, 'Max', str(self.Max))
		maketxtsub(tempd, 'Scaling', str(self.Scaling))

class renoise_instrument_macro:
	def __init__(self):
		self.value = 0
		self.visualization = 'Device only'
		self.name = ''
		self.mappings = []

	def __getitem__(self, v):
		return self.mappings.__getitem__(v)
		
	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'Value': self.value = float(xpart.text) if '.' in xpart.text else int(xpart.text)
			if xpart.tag == 'Visualization': self.visualization = xpart.text
			if xpart.tag == 'Name': self.name = xpart.text
			if xpart.tag == 'Mappings':
				for xinpart in xpart:
					if xinpart.tag == 'Mapping':
						map_obj = renoise_instrument_macro_mappings()
						map_obj.read(xinpart)
						self.mappings.append(map_obj)

	def write(self, xmldata, name):
		tempd = ET.SubElement(xmldata, name)
		maketxtsub(tempd, 'Value', str(self.value))
		maketxtsub(tempd, 'Visualization', str(self.visualization))
		if self.name: maketxtsub(tempd, 'Name', str(self.name))
		if self.mappings:
			xmlmappings = ET.SubElement(tempd, 'Mappings')
			for map_obj in self.mappings: map_obj.write(xmlmappings)

# --------------------------------------------------------- MODULATIONSET ---------------------------------------------------------

class renoise_instrument_modulationset:
	def __init__(self):
		self.SelectedPresetName = ''
		self.SelectedPresetIsModified = False
		self.Name = ''
		self.Devices = []
		self.FilterType = 6
		self.FilterBankVersion = 2

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'SelectedPresetName': self.SelectedPresetName = xpart.text
			if xpart.tag == 'SelectedPresetIsModified': self.SelectedPresetIsModified = xpart.text=='true'
			if xpart.tag == 'Name': self.Name = xpart.text
			if xpart.tag == 'FilterType': self.FilterType = int(xpart.text)
			if xpart.tag == 'FilterBankVersion': self.FilterBankVersion = int(xpart.text)
			if xpart.tag == 'Devices':
				for xinpart in xpart:
					device_obj = device.renoise_device()
					device_obj.read(xinpart)
					self.Devices.append(device_obj)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'ModulationSet')
		maketxtsub(tempd, 'SelectedPresetName', str(self.SelectedPresetName))
		maketxtsub(tempd, 'SelectedPresetIsModified', strbool(self.SelectedPresetIsModified))
		xmldevices = ET.SubElement(tempd, 'Devices')
		for device_obj in self.Devices:
			device_obj.write(xmldevices)
		maketxtsub(tempd, 'Name', str(self.Name))
		maketxtsub(tempd, 'FilterType', str(self.FilterType))
		maketxtsub(tempd, 'FilterBankVersion', str(self.FilterBankVersion))

# --------------------------------------------------------- SAMPLE ---------------------------------------------------------

class renoise_instrument_sample_mapping:
	def __init__(self):
		self.Layer = ''
		self.BaseNote = 60
		self.NoteStart = 0
		self.NoteEnd = 127
		self.MapKeyToPitch = True
		self.VelocityStart = 0
		self.VelocityEnd = 127
		self.MapVelocityToVolume = True

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'Layer': self.Layer = xpart.text
			if xpart.tag == 'BaseNote': self.BaseNote = int(xpart.text)
			if xpart.tag == 'NoteStart': self.NoteStart = int(xpart.text)
			if xpart.tag == 'NoteEnd': self.NoteEnd = int(xpart.text)
			if xpart.tag == 'MapKeyToPitch': self.MapKeyToPitch = xpart.text=='true'
			if xpart.tag == 'VelocityStart': self.VelocityStart = int(xpart.text)
			if xpart.tag == 'VelocityEnd': self.VelocityEnd = int(xpart.text)
			if xpart.tag == 'MapVelocityToVolume': self.MapVelocityToVolume = xpart.text=='true'

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'Mapping')
		maketxtsub(tempd, 'Layer', str(self.Layer))
		maketxtsub(tempd, 'BaseNote', str(self.BaseNote))
		maketxtsub(tempd, 'NoteStart', str(self.NoteStart))
		maketxtsub(tempd, 'NoteEnd', str(self.NoteEnd))
		maketxtsub(tempd, 'MapKeyToPitch', strbool(self.MapKeyToPitch))
		maketxtsub(tempd, 'VelocityStart', str(self.VelocityStart))
		maketxtsub(tempd, 'VelocityEnd', str(self.VelocityEnd))
		maketxtsub(tempd, 'MapVelocityToVolume', strbool(self.MapVelocityToVolume))

class renoise_instrument_sample:
	def __init__(self):
		self.SelectedPresetName = 'Init'
		self.SelectedPresetIsModified = True
		self.Name = ''
		self.Volume = 1.0
		self.Panning = 0.5
		self.Transpose = 0
		self.Finetune = 0
		self.BeatSyncIsActive = False
		self.BeatSyncMode = 'Repitch'
		self.BeatSyncLines = 16
		self.OneShotTrigger = False
		self.NewNoteAction = 'Cut'
		self.Oversample = False
		self.InterpolationMode = 'Cubic'
		self.AutoSeek = False
		self.AutoFade = False
		self.LoopMode = 'Forward'
		self.LoopRelease = False
		self.LoopStart = 0
		self.LoopEnd = 337
		self.SingleSliceTriggerEnabled = True
		self.IsAlias = False
		self.MuteGroupIndex = -1
		self.ModulationSetIndex = 0
		self.DeviceChainIndex = 0
		self.DisplayStart = 0
		self.DisplayLength = 337
		self.SelectionRangeStart = -1
		self.SelectionRangeEnd = -1
		self.SelectedChannel = 'L+R'
		self.VZoomFactor = 1.0
		self.Mapping = renoise_instrument_sample_mapping()

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'SelectedPresetName': self.SelectedPresetName = xpart.text
			if xpart.tag == 'SelectedPresetIsModified': self.SelectedPresetIsModified = xpart.text=='true'
			if xpart.tag == 'Name': self.Name = xpart.text
			if xpart.tag == 'Volume': self.Volume = float(xpart.text)
			if xpart.tag == 'Panning': self.Panning = float(xpart.text)
			if xpart.tag == 'Transpose': self.Transpose = int(xpart.text)
			if xpart.tag == 'Finetune': self.Finetune = int(xpart.text)
			if xpart.tag == 'BeatSyncIsActive': self.BeatSyncIsActive = xpart.text=='true'
			if xpart.tag == 'BeatSyncMode': self.BeatSyncMode = xpart.text
			if xpart.tag == 'BeatSyncLines': self.BeatSyncLines = int(xpart.text)
			if xpart.tag == 'OneShotTrigger': self.OneShotTrigger = xpart.text=='true'
			if xpart.tag == 'NewNoteAction': self.NewNoteAction = xpart.text
			if xpart.tag == 'Oversample': self.Oversample = xpart.text=='true'
			if xpart.tag == 'InterpolationMode': self.InterpolationMode = xpart.text
			if xpart.tag == 'AutoSeek': self.AutoSeek = xpart.text=='true'
			if xpart.tag == 'AutoFade': self.AutoFade = xpart.text=='true'
			if xpart.tag == 'LoopMode': self.LoopMode = xpart.text
			if xpart.tag == 'LoopRelease': self.LoopRelease = xpart.text=='true'
			if xpart.tag == 'LoopStart': self.LoopStart = int(xpart.text)
			if xpart.tag == 'LoopEnd': self.LoopEnd = int(xpart.text)
			if xpart.tag == 'SingleSliceTriggerEnabled': self.SingleSliceTriggerEnabled = xpart.text=='true'
			if xpart.tag == 'IsAlias': self.IsAlias = xpart.text=='true'
			if xpart.tag == 'MuteGroupIndex': self.MuteGroupIndex = int(xpart.text)
			if xpart.tag == 'ModulationSetIndex': self.ModulationSetIndex = int(xpart.text)
			if xpart.tag == 'DeviceChainIndex': self.DeviceChainIndex = int(xpart.text)
			if xpart.tag == 'DisplayStart': self.DisplayStart = int(xpart.text)
			if xpart.tag == 'DisplayLength': self.DisplayLength = int(xpart.text)
			if xpart.tag == 'SelectionRangeStart': self.SelectionRangeStart = int(xpart.text)
			if xpart.tag == 'SelectionRangeEnd': self.SelectionRangeEnd = int(xpart.text)
			if xpart.tag == 'SelectedChannel': self.SelectedChannel = xpart.text
			if xpart.tag == 'VZoomFactor': self.VZoomFactor = float(xpart.text)
			if xpart.tag == 'Mapping': self.Mapping.read(xpart)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'Sample')
		maketxtsub(tempd, 'SelectedPresetName', str(self.SelectedPresetName))
		maketxtsub(tempd, 'SelectedPresetIsModified', strbool(self.SelectedPresetIsModified))
		maketxtsub(tempd, 'Name', str(self.Name))
		maketxtsub(tempd, 'Volume', str(self.Volume))
		maketxtsub(tempd, 'Panning', str(self.Panning))
		maketxtsub(tempd, 'Transpose', str(self.Transpose))
		maketxtsub(tempd, 'Finetune', str(self.Finetune))
		maketxtsub(tempd, 'BeatSyncIsActive', strbool(self.BeatSyncIsActive))
		maketxtsub(tempd, 'BeatSyncMode', str(self.BeatSyncMode))
		maketxtsub(tempd, 'BeatSyncLines', str(self.BeatSyncLines))
		maketxtsub(tempd, 'OneShotTrigger', strbool(self.OneShotTrigger))
		maketxtsub(tempd, 'NewNoteAction', str(self.NewNoteAction))
		maketxtsub(tempd, 'Oversample', strbool(self.Oversample))
		maketxtsub(tempd, 'InterpolationMode', str(self.InterpolationMode))
		maketxtsub(tempd, 'AutoSeek', strbool(self.AutoSeek))
		maketxtsub(tempd, 'AutoFade', strbool(self.AutoFade))
		maketxtsub(tempd, 'LoopMode', str(self.LoopMode))
		maketxtsub(tempd, 'LoopRelease', strbool(self.LoopRelease))
		maketxtsub(tempd, 'LoopStart', str(self.LoopStart))
		maketxtsub(tempd, 'LoopEnd', str(self.LoopEnd))
		maketxtsub(tempd, 'SingleSliceTriggerEnabled', strbool(self.SingleSliceTriggerEnabled))
		maketxtsub(tempd, 'IsAlias', strbool(self.IsAlias))
		maketxtsub(tempd, 'MuteGroupIndex', str(self.MuteGroupIndex))
		maketxtsub(tempd, 'ModulationSetIndex', str(self.ModulationSetIndex))
		maketxtsub(tempd, 'DeviceChainIndex', str(self.DeviceChainIndex))
		self.Mapping.write(tempd)
		maketxtsub(tempd, 'DisplayStart', str(self.DisplayStart))
		maketxtsub(tempd, 'DisplayLength', str(self.DisplayLength))
		maketxtsub(tempd, 'SelectionRangeStart', str(self.SelectionRangeStart))
		maketxtsub(tempd, 'SelectionRangeEnd', str(self.SelectionRangeEnd))
		maketxtsub(tempd, 'SelectedChannel', str(self.SelectedChannel))
		maketxtsub(tempd, 'VZoomFactor', str(self.VZoomFactor))

class renoise_instrument_splitmap:
	def __init__(self):
		self.SelectedPresetName = ""
		self.SelectedPresetIsModified = False

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'SelectedPresetName': self.SelectedPresetName = xpart.text
			if xpart.tag == 'SelectedPresetIsModified': self.SelectedPresetIsModified = xpart.text

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'SplitMap')
		maketxtsub(tempd, 'SelectedPresetName', str(self.SelectedPresetName))
		maketxtsub(tempd, 'SelectedPresetIsModified', str(self.SelectedPresetIsModified))

class renoise_instrument_samplegenerator:
	def __init__(self):
		self.SelectedSampleIndex = 0
		self.SelectedModulationSetIndex = 0
		self.Samples = []
		self.ModulationSets = []
		self.DeviceChains = []
		self.SelectedDeviceChainIndex = 0
		self.KeyzoneOverlappingMode = 'Play All'
		self.SplitMap = renoise_instrument_splitmap()

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'SelectedSampleIndex': self.SelectedSampleIndex = int(xpart.text)
			if xpart.tag == 'SelectedModulationSetIndex': self.SelectedModulationSetIndex = int(xpart.text)
			if xpart.tag == 'SelectedDeviceChainIndex': self.SelectedDeviceChainIndex = int(xpart.text)
			if xpart.tag == 'KeyzoneOverlappingMode': self.KeyzoneOverlappingMode = xpart.text
			if xpart.tag == 'SplitMap': self.SplitMap.read(xpart)

			if xpart.tag == 'Samples':
				for xinpart in xpart:
					if xinpart.tag == 'Sample':
						phrase_obj = renoise_instrument_sample()
						phrase_obj.read(xinpart)
						self.Samples.append(phrase_obj)

			if xpart.tag == 'ModulationSets':
				for xinpart in xpart:
					if xinpart.tag == 'ModulationSet':
						phrase_obj = renoise_instrument_modulationset()
						phrase_obj.read(xinpart)
						self.ModulationSets.append(phrase_obj)

			if xpart.tag == 'DeviceChains':
				for xinpart in xpart:
					if xinpart.tag == 'DeviceChain':
						phrase_obj = device.renoise_devicechain()
						phrase_obj.read(xinpart)
						self.DeviceChains.append(phrase_obj)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'SampleGenerator')
		xmlmappings = ET.SubElement(tempd, 'Samples')
		if self.Samples:
			for Sample in self.Samples: Sample.write(xmlmappings)
		maketxtsub(tempd, 'SelectedSampleIndex', str(self.SelectedSampleIndex))
		xmlmappings = ET.SubElement(tempd, 'ModulationSets')
		if self.ModulationSets:
			for ModulationSet in self.ModulationSets: ModulationSet.write(xmlmappings)
		maketxtsub(tempd, 'SelectedModulationSetIndex', str(self.SelectedModulationSetIndex))
		xmlmappings = ET.SubElement(tempd, 'DeviceChains')
		if self.DeviceChains:
			for DeviceChain in self.DeviceChains: DeviceChain.write(xmlmappings)
		maketxtsub(tempd, 'SelectedDeviceChainIndex', str(self.SelectedDeviceChainIndex))
		maketxtsub(tempd, 'KeyzoneOverlappingMode', self.KeyzoneOverlappingMode)
		self.SplitMap.write(tempd)

# --------------------------------------------------------- PLUGIN ---------------------------------------------------------

class renoise_instrument_plugingenerator_outputroutings:
	def __init__(self):
		self.Enabled = False
		self.Name = ''
		self.MixMode = ''
		self.AutoAssign = True
		self.AssignedTrack = ''

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'Enabled': self.Enabled = xpart.text=='true'
			if xpart.tag == 'Name': self.Name = xpart.text
			if xpart.tag == 'MixMode': self.MixMode = xpart.text
			if xpart.tag == 'AutoAssign': self.AutoAssign = xpart.text=='true'
			if xpart.tag == 'AssignedTrack': self.AssignedTrack = xpart.text

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'OutputRouting')
		maketxtsub(tempd, 'Enabled', strbool(self.Enabled))
		maketxtsub(tempd, 'Name', self.Name)
		maketxtsub(tempd, 'MixMode', self.MixMode)
		maketxtsub(tempd, 'AutoAssign', strbool(self.AutoAssign))
		maketxtsub(tempd, 'AssignedTrack', self.AssignedTrack)

class renoise_instrument_plugingenerator:
	def __init__(self):
		self.Channel = 0
		self.Transpose = 0
		self.Volume = 1.0
		self.MidiOutputRoutingIndex = -1
		self.AutoSuspend = True
		self.AliasInstrumentIndex = -1
		self.AliasFxIndices = [-1,-1]
		self.OutputRoutings = []

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'Channel': self.Channel = int(xpart.text)
			if xpart.tag == 'Transpose': self.Transpose = int(xpart.text)
			if xpart.tag == 'Volume': self.Volume = float(xpart.text)
			if xpart.tag == 'MidiOutputRoutingIndex': self.MidiOutputRoutingIndex = int(xpart.text)
			if xpart.tag == 'AutoSuspend': self.AutoSuspend = xpart.text=='true'
			if xpart.tag == 'AliasInstrumentIndex': self.AliasInstrumentIndex = int(xpart.text)
			if xpart.tag == 'AliasFxIndices': self.AliasFxIndices = get_int_comma(xpart.text)
			if xpart.tag == 'OutputRoutings':
				for xinpart in xpart:
					if xinpart.tag == 'OutputRouting':
						oroute_obj = renoise_instrument_plugingenerator_outputroutings()
						oroute_obj.read(xinpart)
						self.OutputRoutings.append(oroute_obj)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'PluginGenerator')
		maketxtsub(tempd, 'Channel', str(self.Channel))
		maketxtsub(tempd, 'Transpose', str(self.Transpose))
		maketxtsub(tempd, 'Volume', str(self.Volume))
		xmldevices = ET.SubElement(tempd, 'OutputRoutings')
		for oroute_obj in self.OutputRoutings:
			oroute_obj.write(xmldevices)
		maketxtsub(tempd, 'MidiOutputRoutingIndex', str(self.MidiOutputRoutingIndex))
		maketxtsub(tempd, 'AutoSuspend', strbool(self.AutoSuspend))
		maketxtsub(tempd, 'AliasInstrumentIndex', str(self.AliasInstrumentIndex))
		maketxtsub(tempd, 'AliasFxIndices', make_int_comma(self.AliasFxIndices))

# --------------------------------------------------------- MIDI ---------------------------------------------------------

class renoise_instrument_midigenerator:
	def __init__(self):
		self.Channel = 0
		self.InstrumentType = "ext. MIDI"
		self.Delay = 0
		self.Program = -1
		self.Bank = -1
		self.BankOrder = "MSB, LSB"
		self.Transpose = 0
		self.Length = 8000

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'Channel': self.Channel = int(xpart.text)
			if xpart.tag == 'InstrumentType': self.InstrumentType = xpart.text
			if xpart.tag == 'Delay': self.Delay = int(xpart.text)
			if xpart.tag == 'Program': self.Program = int(xpart.text)
			if xpart.tag == 'Bank': self.Bank = int(xpart.text)
			if xpart.tag == 'BankOrder': self.BankOrder = xpart.text
			if xpart.tag == 'Transpose': self.Transpose = int(xpart.text)
			if xpart.tag == 'Length': self.Length = int(xpart.text)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'MidiGenerator')
		maketxtsub(tempd, 'Channel', str(self.Channel))
		maketxtsub(tempd, 'InstrumentType', self.InstrumentType)
		maketxtsub(tempd, 'Delay', str(self.Delay))
		maketxtsub(tempd, 'Program', str(self.Program))
		maketxtsub(tempd, 'Bank', str(self.Bank))
		maketxtsub(tempd, 'BankOrder', self.BankOrder)
		maketxtsub(tempd, 'Transpose', str(self.Transpose))
		maketxtsub(tempd, 'Length', str(self.Length))

# --------------------------------------------------------- MAIN ---------------------------------------------------------

class renoise_instrument_globalproperties:
	def __init__(self):
		self.macro0 = renoise_instrument_macro()
		self.macro1 = renoise_instrument_macro()
		self.macro2 = renoise_instrument_macro()
		self.macro3 = renoise_instrument_macro()
		self.macro4 = renoise_instrument_macro()
		self.macro5 = renoise_instrument_macro()
		self.macro6 = renoise_instrument_macro()
		self.macro7 = renoise_instrument_macro()
		self.pitchbendmacro = renoise_instrument_macro()
		self.modulationwheelmacro = renoise_instrument_macro()
		self.channelpressuremacro = renoise_instrument_macro()

		self.MacrosVisible = True
		self.Volume = 1
		self.Transpose = 0
		self.Scale = None
		self.ScaleKey = 'C'
		self.Quantize = None
		self.Monophonic = True
		self.MonophonicGlide = 0
		self.ShowCommentsAfterLoading = False
		self.BeatsPerMin = 127

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'Macro0': self.macro0.read(xpart)
			if xpart.tag == 'Macro1': self.macro1.read(xpart)
			if xpart.tag == 'Macro2': self.macro2.read(xpart)
			if xpart.tag == 'Macro3': self.macro3.read(xpart)
			if xpart.tag == 'Macro4': self.macro4.read(xpart)
			if xpart.tag == 'Macro5': self.macro5.read(xpart)
			if xpart.tag == 'Macro6': self.macro6.read(xpart)
			if xpart.tag == 'Macro7': self.macro7.read(xpart)
			if xpart.tag == 'PitchbendMacro': self.pitchbendmacro.read(xpart)
			if xpart.tag == 'ModulationWheelMacro': self.modulationwheelmacro.read(xpart)
			if xpart.tag == 'ChannelPressureMacro': self.channelpressuremacro.read(xpart)
			if xpart.tag == 'MacrosVisible': self.MacrosVisible = xpart.text=='true'
			if xpart.tag == 'Volume': self.Volume = float(xpart.text)
			if xpart.tag == 'Transpose': self.Transpose = int(xpart.text)
			if xpart.tag == 'Scale': self.Scale = xpart.text
			if xpart.tag == 'ScaleKey': self.ScaleKey = xpart.text
			if xpart.tag == 'Quantize': self.Quantize = xpart.text
			if xpart.tag == 'Monophonic': self.Monophonic = xpart.text=='true'
			if xpart.tag == 'MonophonicGlide': self.MonophonicGlide = int(xpart.text)
			if xpart.tag == 'ShowCommentsAfterLoading': self.ShowCommentsAfterLoading = xpart.text
			if xpart.tag == 'BeatsPerMin': self.BeatsPerMin = xpart.text

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'GlobalProperties')
		self.macro0.write(tempd, 'Macro0')
		self.macro1.write(tempd, 'Macro1')
		self.macro2.write(tempd, 'Macro2')
		self.macro3.write(tempd, 'Macro3')
		self.macro4.write(tempd, 'Macro4')
		self.macro5.write(tempd, 'Macro5')
		self.macro6.write(tempd, 'Macro6')
		self.macro7.write(tempd, 'Macro7')
		self.pitchbendmacro.write(tempd, 'PitchbendMacro')
		self.modulationwheelmacro.write(tempd, 'ModulationWheelMacro')
		self.channelpressuremacro.write(tempd, 'ChannelPressureMacro')
		maketxtsub(tempd, 'MacrosVisible', strbool(self.MacrosVisible))
		maketxtsub(tempd, 'Volume', str(self.Volume))
		maketxtsub(tempd, 'Transpose', str(self.Transpose))
		maketxtsub(tempd, 'Scale', str(self.Scale))
		maketxtsub(tempd, 'ScaleKey', str(self.ScaleKey))
		maketxtsub(tempd, 'Quantize', str(self.Quantize))
		maketxtsub(tempd, 'Monophonic', strbool(self.Monophonic))
		maketxtsub(tempd, 'MonophonicGlide', str(self.MonophonicGlide))
		maketxtsub(tempd, 'ShowCommentsAfterLoading', str(self.ShowCommentsAfterLoading))
		maketxtsub(tempd, 'BeatsPerMin', str(self.BeatsPerMin))

class renoise_instrument_midiinputproperties:
	def __init__(self):
		self.Channel = 0
		self.NoteRangeStart = 0
		self.NoteRangeEnd = 0
		self.AssignedTrack = 0

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'Channel': self.Channel = int(xpart.text)
			if xpart.tag == 'NoteRangeStart': self.NoteRangeStart = int(xpart.text)
			if xpart.tag == 'NoteRangeEnd': self.NoteRangeEnd = int(xpart.text)
			if xpart.tag == 'AssignedTrack': self.AssignedTrack = int(xpart.text)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'MidiInputProperties')
		maketxtsub(tempd, 'Channel', str(self.Channel))
		maketxtsub(tempd, 'NoteRangeStart', str(self.NoteRangeStart))
		maketxtsub(tempd, 'NoteRangeEnd', str(self.NoteRangeEnd))
		maketxtsub(tempd, 'AssignedTrack', str(self.AssignedTrack))

class renoise_instrument:
	def __init__(self):
		self.selectedpresetname = 'Init'
		self.selectedpresetismodified = True
		self.name = ''
		self.copyintonewsamplenamecounter = 0
		self.copyintonewinstrumentnamecounter = 0
		self.activegeneratortab = 'Samples'
		self.globalproperties = renoise_instrument_globalproperties()
		self.midiinputproperties = renoise_instrument_midiinputproperties()
		self.phrasegenerator = renoise_instrument_phrasegenerator()
		self.samplegenerator = renoise_instrument_samplegenerator()
		self.plugingenerator = renoise_instrument_plugingenerator()
		self.midigenerator = renoise_instrument_midigenerator()

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'SelectedPresetName': self.selectedpresetname = xpart.text
			if xpart.tag == 'SelectedPresetIsModified': self.selectedpresetismodified = xpart.text=='true'
			if xpart.tag == 'Name': self.name = xpart.text
			if xpart.tag == 'CopyIntoNewSampleNameCounter': self.copyintonewsamplenamecounter = int(xpart.text)
			if xpart.tag == 'CopyIntoNewInstrumentNameCounter': self.copyintonewinstrumentnamecounter = int(xpart.text)
			if xpart.tag == 'ActiveGeneratorTab': self.activegeneratortab = xpart.text
			if xpart.tag == 'GlobalProperties': self.globalproperties.read(xpart)
			if xpart.tag == 'MidiInputProperties': self.midiinputproperties.read(xpart)
			if xpart.tag == 'PhraseGenerator': self.phrasegenerator.read(xpart)
			if xpart.tag == 'SampleGenerator': self.samplegenerator.read(xpart)
			if xpart.tag == 'PluginGenerator': self.plugingenerator.read(xpart)
			if xpart.tag == 'MidiGenerator': self.midigenerator.read(xpart)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'Instrument')
		maketxtsub(tempd, 'SelectedPresetName', str(self.selectedpresetname))
		maketxtsub(tempd, 'SelectedPresetIsModified', strbool(self.selectedpresetismodified))
		maketxtsub(tempd, 'Name', str(self.name))
		maketxtsub(tempd, 'CopyIntoNewSampleNameCounter', str(self.copyintonewsamplenamecounter))
		maketxtsub(tempd, 'CopyIntoNewInstrumentNameCounter', str(self.copyintonewinstrumentnamecounter))
		self.globalproperties.write(tempd)
		self.midiinputproperties.write(tempd)
		self.phrasegenerator.write(tempd)
		self.samplegenerator.write(tempd)
		self.plugingenerator.write(tempd)
		self.midigenerator.write(tempd)
		maketxtsub(tempd, 'ActiveGeneratorTab', self.activegeneratortab)
