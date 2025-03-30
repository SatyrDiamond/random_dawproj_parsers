# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from objects.data_bytes import bytereader
import logging

class recomposer_event:
	names = {
		0x90: "UsrExc0",
		0x91: "UsrExc1",
		0x92: "UsrExc2",
		0x93: "UsrExc3",
		0x94: "UsrExc4",
		0x95: "UsrExc5",
		0x96: "UsrExc6",
		0x97: "UsrExc7",
		0x98: "TrExcl",
		0x99: "ExtCmd",
		0xc0: "DX7FUNC",
		0xc1: "DX_PARA",
		0xc2: "DX_PERF",
		0xc3: "TX_FUNC",
		0xc5: "FB_01_P",
		0xc6: "FB_01_S",
		0xc7: "TX81Z_V",
		0xc8: "TX81Z_A",
		0xc9: "TX81Z_P",
		0xca: "TX81Z_S",
		0xcb: "TX81Z_E",
		0xcc: "DX7_2_R",
		0xcd: "DX7_2_A",
		0xce: "DX7_2_P",
		0xcf: "TX802_P",
		0xd0: "YamBase",
		0xd1: "YamDev",
		0xd2: "YamPara",
		0xd3: "XGPara",
		0xdc: "MKS_7",
		0xdd: "RolBase",
		0xde: "RolPara",
		0xdf: "RolDev",
		0xe1: "BankPrgL",
		0xe2: "BankPrg",
		0xe5: "KeyScan",
		0xe6: "MIDI_CH",
		0xe7: "TEMPO",
		0xea: "AFTER_C",
		0xeb: "CONTROL",
		0xec: "PROGRAM",
		0xed: "AFTER_K",
		0xee: "PITCH",
		0xf5: "MusicKey",
		0xf6: "Comment",
		0xf7: "SecondEvt",
		0xf8: "LoopEnd",
		0xf9: "LoopStart",
		0xfc: "SameMeas",
		0xfd: "MeasEnd",
		0xfe: "TrackEnd"
	}

	def __init__(self):
		self.note = 0
		self.p0 = 0
		self.p1 = 0
		self.p2 = 0

	def __repr__(self):
		outtxt = '<RCP Event: "'
		if self.note in recomposer_event.names: outtxt += recomposer_event.names[self.note].ljust(10)
		else: outtxt += 'Note'.ljust(10)
		outtxt += '",{0},{1},{2}>'.format(str(self.p0).rjust(4), str(self.p1).rjust(4), str(self.p2).rjust(4))
		return outtxt

	def read(self, byr_stream):
		self.note = byr_stream.uint8()
		self.p0 = byr_stream.uint8()
		self.p1 = byr_stream.uint8()
		self.p2 = byr_stream.uint8()

class recomposer_track:
	def __init__(self):
		self.length = 0
		self.track_id = 0
		self.rhythm_mode = 0 
		self.midi_channel = 0
		self.key = 0
		self.tick_offset = 0
		self.mute = 0
		self.events = []

	def read(self, byr_stream):
		self.length = byr_stream.uint16()
		self.track_id = byr_stream.uint8()
		self.rhythm_mode = byr_stream.uint8()
		self.midi_channel = byr_stream.uint8()
		self.key = byr_stream.uint8()
		self.tick_offset = byr_stream.uint8()
		self.mute = byr_stream.uint8()
		self.name = byr_stream.raw(36)

		while byr_stream.remaining():
			event_obj = recomposer_event()
			event_obj.read(byr_stream)
			if event_obj.note == 254: break
			self.events.append(event_obj)

class recomposer_song:
	def __init__(self):
		self.title = ''
		self.comment = []
		self.ticksq_low = 0
		self.tempo = 0
		self.beat_numerator = 0
		self.beat_denominator = 0
		self.key_signature = 0
		self.playbias = 0
		self.cm6_file = ''
		self.gsd_file = ''
		self.num_tracks = 0
		self.ticksq_high = 0
		self.unkd = None
		self.rhythm_defs = []
		self.user_sysex = []
		self.tracks = []

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)
		byr_stream.magic_check(b'RCM-PC98V2.0(C)COME ON MUSIC\r\n\x00\x00')
		self.title = byr_stream.string(64, encoding='SHIFT_JIS')
		self.comment = [byr_stream.string(28, encoding='SHIFT_JIS') for x in range(12)]
		byr_stream.skip(16)

		self.ticksq_low = byr_stream.uint8()
		self.tempo =  byr_stream.uint8()
		self.beat_numerator = byr_stream.uint8()
		self.beat_denominator = byr_stream.uint8()
		self.key_signature = byr_stream.uint8()
		self.playbias = byr_stream.uint8()

		self.cm6_file = byr_stream.string(10, encoding='SHIFT_JIS')
		self.gsd_file = byr_stream.string(10, encoding='SHIFT_JIS')
		self.num_tracks = byr_stream.uint8()
		self.ticksq_high = byr_stream.uint8()
		self.unkd = byr_stream.raw(0x1E)

		byr_stream.seek(0x206)
		self.rhythm_defs = [[byr_stream.raw(14), byr_stream.uint8(), byr_stream.uint8()] for x in range(32)]
		self.user_sysex = [[byr_stream.raw(24), byr_stream.raw(24)] for x in range(8)]

		while byr_stream.remaining():
			track_obj = recomposer_track()
			track_obj.read(byr_stream)
			self.tracks.append(track_obj)


apeinst_obj = recomposer_song()
apeinst_obj.load_from_file("G:\\RandomMusicFiles\\midi\\recomposer\\OnlyMIDIs\\BEYOND.RCP")
