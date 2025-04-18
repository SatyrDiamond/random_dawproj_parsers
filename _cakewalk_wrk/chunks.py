# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

from _cakewalk_wrk import events

# --------------------------------------------------------- DATA ---------------------------------------------------------

chunkids = {}

def make_chunk(intype):
	chunk_obj = cakewalk_wrk_chunk(None)
	chunk_obj.set_type(intype)
	return chunk_obj

class cakewalk_wrk_chunk:
	def __init__(self, byr_stream):
		self.id = -1
		self.data = None
		self.is_parsed = False
		if byr_stream: self.read(byr_stream)

	def __repr__(self):
		name = chunkids[self.id] if self.id in chunkids else 'UNKNOWN'
		return '<Cakewalk WRK Chunk #%s: %s>' % (str(self.id).ljust(3), name)

	def set_type(self, intype):
		self.id = intype
		self.data = chunkobjects[intype](None) if intype in chunkids else b''
		self.is_parsed = intype in chunkobjects

	def read(self, byr_stream):
		self.id = byr_stream.uint8()
		if self.id != 255: 
			csize = byr_stream.uint32()
			with byr_stream.isolate_size(csize, True) as bye_stream:
				if self.id in chunkobjects: 
					self.data = chunkobjects[self.id](bye_stream)
					self.is_parsed = True
				else: self.data = bye_stream.raw(csize)

	def write(self, byw_stream):
		byw_instream = bytewriter.bytewriter()
		if self.is_parsed: 
			self.data.write(byw_instream)
		else: 
			byw_instream.raw(self.data)
		byw_stream.uint8(self.id)
		outdata = byw_instream.getvalue()
		byw_stream.uint32(len(outdata))
		byw_stream.raw(outdata)

# --------------------------------------------------------- CHUNKS ---------------------------------------------------------

chunkobjects = {}

from _cakewalk_wrk import chunks_gen1

chunkids[3] = "Gen1:Global:Settings"
chunkobjects[3] = chunks_gen1.cakewalk_chunk_globalsettings

chunkids[4] = "V1_TEMPO_MAP"

chunkids[5] = "Gen1:Global:MeterMap"
chunkobjects[5] = chunks_gen1.cakewalk_chunk_meter_map

chunkids[6] = "Gen1:Global:SysEx"
chunkobjects[6] = chunks_gen1.cakewalk_chunk_sysex

chunkids[7] = "V1_MEM_REGION"

chunkids[8] = "Gen1:Global:Comment"
chunkobjects[8] = chunks_gen1.cakewalk_chunk_comment

chunkids[10] = "Gen1:Global:Timebase"
chunkobjects[10] = chunks_gen1.cakewalk_chunk_timebase

chunkids[11] = "Gen1:Global:SMPTE_Time"
chunkobjects[11] = chunks_gen1.cakewalk_chunk_smpte_time

chunkids[15] = "Gen1:Global:Auto:Tempo_V3"
chunkobjects[15] = chunks_gen1.cakewalk_chunk_tempo

chunkids[16] = "Gen1:Global:Ext_Thru"
chunkobjects[16] = chunks_gen1.cakewalk_chunk_ext_thru

chunkids[20] = "V1_SYSEX2"

chunkids[21] = "Gen1:Global:Markers"
chunkobjects[21] = chunks_gen1.cakewalk_chunk_markers

chunkids[22] = "Gen1:Global:StringTables"
chunkobjects[22] = chunks_gen1.cakewalk_chunk_stringtable

chunkids[23] = "Gen1:Global:MeterKey"
chunkobjects[23] = chunks_gen1.cakewalk_chunk_meter_key

chunkids[26] = "Gen1:Global:VariablePart"
chunkobjects[26] = chunks_gen1.cakewalk_chunk_variable





chunkids[27] = "Gen1:Track:Offset"
chunkobjects[27] = chunks_gen1.cakewalk_chunk_tracknewoffset

chunkids[1] = "Gen1:Track:Header"
chunkobjects[1] = chunks_gen1.cakewalk_chunk_track

chunkids[2] = "Gen1:Track:Events"
chunkobjects[2] = chunks_gen1.cakewalk_chunk_eventstream

chunkids[18] = "Gen1:Track:EventsExt"
chunkobjects[18] = chunks_gen1.cakewalk_chunk_eventsext

chunkids[19] = "Gen1:Track:Volume"
chunkobjects[19] = chunks_gen1.cakewalk_chunk_trackvol

chunkids[24] = "Gen1:Track:Name"
chunkobjects[24] = chunks_gen1.cakewalk_chunk_trackname

chunkids[30] = "Gen1:Track:Bank"
chunkobjects[30] = chunks_gen1.cakewalk_chunk_trackbank

chunkids[9] = "Gen1:Track:Offset"
chunkobjects[9] = chunks_gen1.cakewalk_chunk_trackoffset

chunkids[12] = "Gen1:Track:Repeats"

chunkids[14] = "Gen1:Track:Patch"
chunkobjects[14] = chunks_gen1.cakewalk_chunk_trackpatch




chunkids[44] = "Gen2:Global:NewSysEx"
chunkobjects[44] = chunks_gen1.cakewalk_chunk_newsysex

chunkids[74] = "Gen2:Global:Version"

chunkids[255] = "End"



from _cakewalk_wrk import chunks_gen2

chunkids[36] = "Gen2:Track:Header"
chunkobjects[36] = chunks_gen2.chunk_gen2_track_header

chunkids[45] = "Gen2:Track:Events"
chunkobjects[45] = chunks_gen2.chunk_gen2_track_events

chunkids[63] = "Gen2:Track:Effects"
chunkobjects[63] = chunks_gen2.chunk_gen2_track_effects

chunkids[49] = "Gen2:Track:Segment"
chunkobjects[49] = chunks_gen2.chunk_gen2_track_segment



chunkids[57] = "Gen2:AudioSource"
chunkobjects[57] = chunks_gen2.chunk_gen2_audiosource

chunkids[58] = "Gen2:MidiChanSource"
chunkobjects[58] = chunks_gen2.chunk_gen2_midichans

chunkids[59] = "Gen2:ConsoleParams"
#chunkobjects[59] = chunks_gen2.chunk_gen2_consoleparams






#chunkobjects[54] = chunks_gen1.cakewalk_chunk_test