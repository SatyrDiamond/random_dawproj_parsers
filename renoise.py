# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from _renoise import instrument
from _renoise import pattern
import xml.etree.ElementTree as ET
import logging

from _renoise import func
from _renoise import device
strbool = func.strbool
maketxtsub = func.maketxtsub
get_int_comma = func.get_int_comma
make_int_comma = func.make_int_comma

class renoise_track:
	def __init__(self):
		self.tag = ''
		self.Name = None
		self.Color = [0,0,0]
		self.ColorBlend = 0.0
		self.State = 'Active'
		self.Soloed = False
		self.NoteColumnNames = []
		self.NoteColumnStates = []

		self.NumberOfVisibleNoteColumns = 3
		self.NumberOfVisibleEffectColumns = 1
		self.VolumeColumnIsVisible = True
		self.PanningColumnIsVisible = False
		self.DelayColumnIsVisible = False
		self.SampleEffectColumnIsVisible = False
		self.TrackRouting = 0
		self.GroupNestingLevel = 0
		self.TrackDelay = 0.0
		self.Collapsed = False
		self.Visible = True
		self.FilterDevices = device.renoise_devicechain()

	def read(self, xmldata):
		self.tag = xmldata.tag
		for xpart in xmldata:
			if xpart.tag == 'Name': self.Name = xpart.text
			elif xpart.tag == 'Color': self.Color = get_int_comma(xpart.text)
			elif xpart.tag == 'ColorBlend': self.ColorBlend = float(xpart.text)
			elif xpart.tag == 'State': self.State = xpart.text
			elif xpart.tag == 'Soloed': self.Soloed = xpart.text=='true'

			elif xpart.tag == 'VolumeColumnIsVisible': self.VolumeColumnIsVisible = xpart.text=='true'
			elif xpart.tag == 'PanningColumnIsVisible': self.PanningColumnIsVisible = xpart.text=='true'
			elif xpart.tag == 'DelayColumnIsVisible': self.DelayColumnIsVisible = xpart.text=='true'
			elif xpart.tag == 'SampleEffectColumnIsVisible': self.SampleEffectColumnIsVisible = xpart.text=='true'
			elif xpart.tag == 'Collapsed': self.Collapsed = xpart.text=='true'
			elif xpart.tag == 'Visible': self.Visible = xpart.text=='true'

			elif xpart.tag == 'NumberOfVisibleNoteColumns': self.NumberOfVisibleNoteColumns = int(xpart.text)
			elif xpart.tag == 'NumberOfVisibleEffectColumns': self.NumberOfVisibleEffectColumns = int(xpart.text)
			elif xpart.tag == 'TrackRouting': self.TrackRouting = int(xpart.text)
			elif xpart.tag == 'GroupNestingLevel': self.GroupNestingLevel = int(xpart.text)

			elif xpart.tag == 'TrackDelay': self.TrackDelay = float(xpart.text)

			elif xpart.tag == 'NoteColumnNames': 
				for xinpart in xpart:
					if xinpart.tag == 'NoteColumnName': 
						self.NoteColumnNames.append(xinpart.text)
			elif xpart.tag == 'NoteColumnStates': 
				for xinpart in xpart:
					if xinpart.tag == 'NoteColumnState': 
						self.NoteColumnStates.append(xinpart.text)
			elif xpart.tag == 'FilterDevices':
				self.FilterDevices.read(xpart)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, self.tag)
		tempd.set('type', self.tag)
		maketxtsub(tempd, 'Name', self.Name)
		maketxtsub(tempd, 'Color', make_int_comma(self.Color))
		maketxtsub(tempd, 'ColorBlend', str(self.ColorBlend))
		maketxtsub(tempd, 'State', self.State)
		maketxtsub(tempd, 'Soloed', strbool(self.Soloed))
		NoteColumnStates = ET.SubElement(tempd, 'NoteColumnStates')
		for x in self.NoteColumnStates: maketxtsub(NoteColumnStates, 'NoteColumnState', x)
		NoteColumnNames = ET.SubElement(tempd, 'NoteColumnNames')
		for x in self.NoteColumnNames: 
			part = ET.SubElement(NoteColumnNames, 'NoteColumnName')
			part.text = x

		maketxtsub(tempd, 'NumberOfVisibleNoteColumns', str(self.NumberOfVisibleNoteColumns))
		maketxtsub(tempd, 'NumberOfVisibleEffectColumns', str(self.NumberOfVisibleEffectColumns))
		maketxtsub(tempd, 'VolumeColumnIsVisible', strbool(self.VolumeColumnIsVisible))
		maketxtsub(tempd, 'PanningColumnIsVisible', strbool(self.PanningColumnIsVisible))
		maketxtsub(tempd, 'DelayColumnIsVisible', strbool(self.DelayColumnIsVisible))
		maketxtsub(tempd, 'SampleEffectColumnIsVisible', strbool(self.SampleEffectColumnIsVisible))
		maketxtsub(tempd, 'TrackRouting', str(self.TrackRouting))
		maketxtsub(tempd, 'GroupNestingLevel', str(self.GroupNestingLevel))
		maketxtsub(tempd, 'TrackDelay', str(self.TrackDelay))
		maketxtsub(tempd, 'Collapsed', strbool(self.Collapsed))
		maketxtsub(tempd, 'Visible', strbool(self.Visible))
		self.FilterDevices.write_tag(tempd, 'FilterDevices')

# --------------------------------------------------------- PATTERNSEQ ---------------------------------------------------------

class renoise_pattern_sequenceentry_selection:
	def __init__(self):
		self.CursorPos = -1
		self.RangePos = -1

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'CursorPos': self.CursorPos = int(xpart.text)
			if xpart.tag == 'RangePos': self.RangePos = int(xpart.text)

	def write(self, xmldata, tagname):
		tempd = ET.SubElement(xmldata, tagname)
		maketxtsub(tempd, 'CursorPos', str(self.CursorPos))
		maketxtsub(tempd, 'RangePos', str(self.RangePos))

class renoise_pattern_sequenceentry:
	def __init__(self):
		self.Pattern = 0
		self.IsSectionStart = False
		self.SectionName = ''
		self.MutedTracks = []

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'Pattern': self.Pattern = int(xpart.text)
			if xpart.tag == 'IsSectionStart': self.IsSectionStart = xpart.text=='true'
			if xpart.tag == 'SectionName': self.SectionName = xpart.text
			if xpart.tag == 'MutedTracks': 
				for xinpart in xpart:
					if xinpart.tag == 'MutedTrack': self.MutedTracks.append(int(xinpart.text))

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'SequenceEntry')
		maketxtsub(tempd, 'Pattern', str(self.Pattern))
		maketxtsub(tempd, 'IsSectionStart', strbool(self.IsSectionStart))
		maketxtsub(tempd, 'SectionName', str(self.SectionName))
		if self.MutedTracks:
			mutexml = ET.SubElement(tempd, 'MutedTracks')
			for x in self.MutedTracks: maketxtsub(mutexml, 'MutedTrack', str(x))

class renoise_pattern_patternsequence:
	def __init__(self):
		self.CurrentPosition = 0
		self.PatternNameWidth = 0
		self.PatternMatrixWidth = 314
		self.PatternSlotHeight = 34
		self.PatternSlotWidth = 34
		self.HighliteStep = 2
		self.HighliteOffset = 0
		self.KeepSequenceSorted = True
		self.SequenceEntries = []
		self.SequenceSelection = renoise_pattern_sequenceentry_selection()
		self.LoopSelection = renoise_pattern_sequenceentry_selection()


	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'CurrentPosition': self.CurrentPosition = int(xpart.text)
			if xpart.tag == 'PatternNameWidth': self.PatternNameWidth = int(xpart.text)
			if xpart.tag == 'PatternMatrixWidth': self.PatternMatrixWidth = int(xpart.text)
			if xpart.tag == 'PatternSlotHeight': self.PatternSlotHeight = int(xpart.text)
			if xpart.tag == 'PatternSlotWidth': self.PatternSlotWidth = int(xpart.text)
			if xpart.tag == 'HighliteStep': self.HighliteStep = int(xpart.text)
			if xpart.tag == 'HighliteOffset': self.HighliteOffset = int(xpart.text)
			if xpart.tag == 'KeepSequenceSorted': self.KeepSequenceSorted = xpart.text=='true'
			if xpart.tag == 'SequenceSelection': self.SequenceSelection.read(xpart)
			if xpart.tag == 'LoopSelection': self.LoopSelection.read(xpart)
			if xpart.tag == 'SequenceEntries': 
				for xinpart in xpart:
					if xinpart.tag == 'SequenceEntry':
						pattern_obj = renoise_pattern_sequenceentry()
						pattern_obj.read(xinpart)
						self.SequenceEntries.append(pattern_obj)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'PatternSequence')
		maketxtsub(tempd, 'CurrentPosition', str(self.CurrentPosition))
		patxml = ET.SubElement(tempd, 'SequenceEntries')
		for seqe_obj in self.SequenceEntries: seqe_obj.write(patxml)
		self.SequenceSelection.write(tempd, 'SequenceSelection')
		self.LoopSelection.write(tempd, 'LoopSelection')
		maketxtsub(tempd, 'PatternNameWidth', str(self.PatternNameWidth))
		maketxtsub(tempd, 'PatternMatrixWidth', str(self.PatternMatrixWidth))
		maketxtsub(tempd, 'PatternSlotHeight', str(self.PatternSlotHeight))
		maketxtsub(tempd, 'PatternSlotWidth', str(self.PatternSlotWidth))
		maketxtsub(tempd, 'HighliteStep', str(self.HighliteStep))
		maketxtsub(tempd, 'HighliteOffset', str(self.HighliteOffset))
		maketxtsub(tempd, 'KeepSequenceSorted', strbool(self.KeepSequenceSorted))

# --------------------------------------------------------- PROJECT ---------------------------------------------------------

class renoise_globalsongdata:
	def __init__(self):
		self.octave = 4
		self.loopcoeff = 2
		self.beatspermin = 127
		self.linesperbeat = 4
		self.ticksperline = 12
		self.signaturenumerator = 4
		self.signaturedenominator = 4
		self.metronomebeatsperbar = 4
		self.metronomelinesperbeat = 0
		self.shuffleisactive = False
		self.songname = ''
		self.artist = ''
		self.shuffleamounts = []
		self.songcomments = []

		self.showsongcommentsafterloading = True
		self.showusedautomationsonly = False
		self.followautomations = True
		self.sampleoffsetcompatibilitymode = False
		self.pitcheffectscompatibilitymode = False
		self.globaltrackheadroom = 0
		self.playbackengineversion = 6
		self.renderselectionnamecounter = 0
		self.recordsamplenamecounter = 4
		self.newsamplenamecounter = 18

	def read(self, xmldata):
		for xpart in xmldata:
			if xpart.tag == 'Octave': self.octave = int(xpart.text)
			if xpart.tag == 'LoopCoeff': self.loopcoeff = int(xpart.text)
			if xpart.tag == 'BeatsPerMin': self.beatspermin = int(xpart.text)
			if xpart.tag == 'LinesPerBeat': self.linesperbeat = int(xpart.text)
			if xpart.tag == 'TicksPerLine': self.ticksperline = int(xpart.text)
			if xpart.tag == 'SignatureNumerator': self.signaturenumerator = int(xpart.text)
			if xpart.tag == 'SignatureDenominator': self.signaturedenominator = int(xpart.text)
			if xpart.tag == 'MetronomeBeatsPerBar': self.metronomebeatsperbar = int(xpart.text)
			if xpart.tag == 'MetronomeLinesPerBeat': self.metronomelinesperbeat = int(xpart.text)
			if xpart.tag == 'ShuffleIsActive': self.shuffleisactive = xpart.text=='true'
			if xpart.tag == 'SongName': self.songname = xpart.text
			if xpart.tag == 'Artist': self.artist = xpart.text
			if xpart.tag == 'ShuffleAmounts': 
				for xinpart in xpart:
					if xinpart.tag == 'ShuffleAmount': 
						self.shuffleamounts.append(int(xinpart.text))
			if xpart.tag == 'SongComments': 
				for xinpart in xpart:
					if xinpart.tag == 'SongComment': 
						self.songcomments.append(xinpart.text)

			if xpart.tag == 'ShowSongCommentsAfterLoading': self.showsongcommentsafterloading = xpart.text=='true'
			if xpart.tag == 'ShowUsedAutomationsOnly': self.showusedautomationsonly = xpart.text=='true'
			if xpart.tag == 'FollowAutomations': self.followautomations = xpart.text=='true'
			if xpart.tag == 'SampleOffsetCompatibilityMode': self.sampleoffsetcompatibilitymode = xpart.text=='true'
			if xpart.tag == 'PitchEffectsCompatibilityMode': self.pitcheffectscompatibilitymode = xpart.text=='true'
			if xpart.tag == 'GlobalTrackHeadroom': self.globaltrackheadroom = float(xpart.text)
			if xpart.tag == 'PlaybackEngineVersion': self.playbackengineversion = int(xpart.text)
			if xpart.tag == 'RenderSelectionNameCounter': self.renderselectionnamecounter = int(xpart.text)
			if xpart.tag == 'RecordSampleNameCounter': self.recordsamplenamecounter = int(xpart.text)
			if xpart.tag == 'NewSampleNameCounter': self.newsamplenamecounter = int(xpart.text)

	def write(self, xmldata):
		tempd = ET.SubElement(xmldata, 'GlobalSongData')
		maketxtsub(tempd, 'BeatsPerMin', str(self.beatspermin))
		maketxtsub(tempd, 'LinesPerBeat', str(self.linesperbeat))
		maketxtsub(tempd, 'TicksPerLine', str(self.ticksperline))
		maketxtsub(tempd, 'SignatureNumerator', str(self.signaturenumerator))
		maketxtsub(tempd, 'SignatureDenominator', str(self.signaturedenominator))
		maketxtsub(tempd, 'MetronomeBeatsPerBar', str(self.metronomebeatsperbar))
		maketxtsub(tempd, 'MetronomeLinesPerBeat', str(self.metronomelinesperbeat))
		maketxtsub(tempd, 'ShuffleIsActive', strbool(self.shuffleisactive))
		ShuffleAmounts = ET.SubElement(tempd, 'ShuffleAmounts')
		for x in self.shuffleamounts: maketxtsub(ShuffleAmounts, 'ShuffleAmount', str(x))
		maketxtsub(tempd, 'Octave', str(self.octave))
		maketxtsub(tempd, 'LoopCoeff', str(self.loopcoeff))
		maketxtsub(tempd, 'SongName', str(self.songname))
		maketxtsub(tempd, 'Artist', str(self.artist))
		SongComments = ET.SubElement(tempd, 'SongComments')
		for x in self.songcomments: maketxtsub(SongComments, 'SongComment', x)
		maketxtsub(tempd, 'ShowSongCommentsAfterLoading', strbool(self.showsongcommentsafterloading))
		maketxtsub(tempd, 'ShowUsedAutomationsOnly', strbool(self.showusedautomationsonly))
		maketxtsub(tempd, 'FollowAutomations', strbool(self.followautomations))
		maketxtsub(tempd, 'SampleOffsetCompatibilityMode', strbool(self.sampleoffsetcompatibilitymode))
		maketxtsub(tempd, 'PitchEffectsCompatibilityMode', strbool(self.pitcheffectscompatibilitymode))
		maketxtsub(tempd, 'GlobalTrackHeadroom', str(self.globaltrackheadroom))
		maketxtsub(tempd, 'PlaybackEngineVersion', str(self.playbackengineversion))
		maketxtsub(tempd, 'RenderSelectionNameCounter', str(self.renderselectionnamecounter))
		maketxtsub(tempd, 'RecordSampleNameCounter', str(self.recordsamplenamecounter))
		maketxtsub(tempd, 'NewSampleNameCounter', str(self.newsamplenamecounter))

class renoise_song:
	def __init__(self):
		self.globalsongdata = renoise_globalsongdata()
		self.instruments = []
		self.SelectedInstrumentIndex = 0
		self.Tracks = []

		self.SelectedTrackIndex = 18
		self.SpectrumTrackDisplayA = -2
		self.SpectrumTrackDisplayB = -1

		self.PatternPool = pattern.renoise_pattern_patternpool()
		self.PatternSequence = renoise_pattern_patternsequence()

		self.LastSoloedOutMode = 'Off'

	def load_from_file(self, input_file):
		x_root = ET.parse(input_file).getroot()
		for xpart in x_root:
			if xpart.tag == 'GlobalSongData': self.globalsongdata.read(xpart)
			if xpart.tag == 'SelectedInstrumentIndex': self.SelectedInstrumentIndex = int(xpart.text)
			if xpart.tag == 'Instruments':
				for xinpart in xpart:
					if xinpart.tag == 'Instrument':
						inst_obj = instrument.renoise_instrument()
						inst_obj.read(xinpart)
						self.instruments.append(inst_obj)
			if xpart.tag == 'Tracks':
				for xinpart in xpart:
					track_obj = renoise_track()
					track_obj.read(xinpart)
					self.Tracks.append(track_obj)
			if xpart.tag == 'SelectedTrackIndex': self.SelectedTrackIndex = int(xpart.text)
			if xpart.tag == 'SpectrumTrackDisplayA': self.SpectrumTrackDisplayA = int(xpart.text)
			if xpart.tag == 'SpectrumTrackDisplayB': self.SpectrumTrackDisplayB = int(xpart.text)
			if xpart.tag == 'PatternPool': self.PatternPool.read(xpart)
			if xpart.tag == 'PatternSequence': self.PatternSequence.read(xpart)
			if xpart.tag == 'LastSoloedOutMode': self.LastSoloedOutMode = xpart.text

	def save_to_file(self, out_file):
		renoise_proj = ET.Element("RenoiseSong")
		self.globalsongdata.write(renoise_proj)
		xmlinstruments = ET.SubElement(renoise_proj, 'Instruments')
		for inst_obj in self.instruments: inst_obj.write(xmlinstruments)
		maketxtsub(renoise_proj, 'SelectedInstrumentIndex', str(self.SelectedInstrumentIndex))
		xmltracks = ET.SubElement(renoise_proj, 'Tracks')
		for track_obj in self.Tracks: track_obj.write(xmltracks)
		maketxtsub(renoise_proj, 'SelectedTrackIndex', str(self.SelectedTrackIndex))
		maketxtsub(renoise_proj, 'SpectrumTrackDisplayA', str(self.SpectrumTrackDisplayA))
		maketxtsub(renoise_proj, 'SpectrumTrackDisplayB', str(self.SpectrumTrackDisplayB))
		self.PatternPool.write(renoise_proj)
		self.PatternSequence.write(renoise_proj)
		maketxtsub(renoise_proj, 'LastSoloedOutMode', self.LastSoloedOutMode)

		outfile = ET.ElementTree(renoise_proj)
		ET.indent(outfile)
		outfile.write(out_file, xml_declaration = True)

apeinst_obj = renoise_song()
apeinst_obj.load_from_file("Song.xml")
apeinst_obj.save_to_file("out.xml")
