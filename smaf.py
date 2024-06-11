
from objects import bytereader

def calc_gatetime_2(song_file):
	t_durgate = []
	t_durgate_value = song_file.uint8()
	t_durgate.append(t_durgate_value&127)
	if bool(t_durgate_value&128) == True: 
		t_durgate_value = song_file.uint8()
		t_durgate.append(t_durgate_value&127)
	t_durgate.reverse()

	out_duration = 0
	for shift, note_durbyte in enumerate(t_durgate): out_duration += note_durbyte << shift*7
	return out_duration

def calc_gatetime_3(song_file):
	t_durgate = []
	t_durgate_value = song_file.uint8()
	t_durgate.append(t_durgate_value&127)
	if bool(t_durgate_value&128) == True: 
		t_durgate_value = song_file.uint8()
		t_durgate.append(t_durgate_value&127)
		if bool(t_durgate_value&128) == True: 
			t_durgate_value = song_file.uint8()
			t_durgate.append(t_durgate_value&127)
	t_durgate.reverse()

	out_duration = 0
	for shift, note_durbyte in enumerate(t_durgate): out_duration += note_durbyte << shift*7
	return out_duration

verbose = False

class smaf_track_ma3:
	def __init__(self, song_file, end):
		self.format_type = song_file.uint8()
		self.sequence_type = song_file.uint8()
		self.timebase_dur = song_file.uint8()
		self.timebase_gate = song_file.uint8()

		self.channel_stat = song_file.l_uint32(4)
		self.sequence = None
		self.setup = None
		self.audio = {}

		trk_iff_obj = song_file.chunk_objmake()
		trk_iff_obj.set_sizes(4, 4, True)
		for chunk_obj in trk_iff_obj.iter(song_file.tell(), end):
			print('MA3 chunk', chunk_obj.id)

			if chunk_obj.id == b'Mtsq':
				self.sequence = []
				while song_file.tell() <= chunk_obj.end:
					resttime = calc_gatetime_3(song_file)
					event_id, channel = song_file.bytesplit()
					if verbose: print(str(event_id).ljust(3), end=' ')

					if event_id == 0:
						null_durgate = calc_gatetime_3(song_file)
						if verbose: print('|	  NULL	', null_durgate)
						self.sequence.append([resttime, event_id])
			
					elif event_id == 8:
						note_note = song_file.uint8()
						note_durgate = calc_gatetime_3(song_file)
						if verbose: print('| '+str(channel).ljust(4), 'NOTE	   ', str(note_note).ljust(4), '     dur ', note_durgate)
						self.sequence.append([resttime, event_id, channel, note_note, note_durgate])
			
					elif event_id == 9:
						note_note = song_file.uint8()
						note_vol = song_file.uint8()
						note_durgate = calc_gatetime_3(song_file)
						if verbose: print('| '+str(channel).ljust(4), 'NOTE+V  ', str(note_note).ljust(4), str(note_vol).ljust(4), 'dur ', note_durgate)
						self.sequence.append([resttime, event_id, channel, note_note, note_vol, note_durgate])
			
					elif event_id == 11:
						cntltype = song_file.uint8()
						cntldata = song_file.uint8()
						if verbose: print('| '+str(channel).ljust(4), 'CONTROL ', str(cntltype).ljust(4), str(cntldata).ljust(4))
						self.sequence.append([resttime, event_id, channel, cntltype, cntldata])
			
					elif event_id == 12:
						prognumber = song_file.uint8()
						if verbose: print('| '+str(channel).ljust(4), 'PROGRAM ', prognumber)
						self.sequence.append([resttime, event_id, channel, prognumber])
			
					elif event_id == 14:
						pitch = song_file.uint16()
						if verbose: print('| '+str(channel).ljust(4), 'PITCH   ', str(pitch).ljust(4))
						self.sequence.append([resttime, event_id, channel, pitch])
			
					elif event_id == 15 and channel == 0:
						sysexdata = song_file.raw(song_file.uint8())
						if verbose: print('| '+str(channel).ljust(4), 'SYSEX   ', sysexdata.hex())
						self.sequence.append([resttime, event_id, sysexdata])
			
					elif event_id == 15 and channel == 15:
						if verbose: print('| '+str(channel).ljust(4), 'NOP	 ')
						self.sequence.append([resttime, 16])
			
					else:
						print('Unknown Command', event_id, "0x%X" % event_id)
						exit()

			if chunk_obj.id == b'Mtsu': self.setup = song_file.raw(chunk_obj.size)

			if chunk_obj.id == b'Mtsp': 
				for mtsp_chunk_obj in chunk_obj.iter(0):
					if mtsp_chunk_obj.id[:3] == b'Mwa':
						audnum = mtsp_chunk_obj.id[3:][0]
						self.audio[audnum] = song_file.raw(mtsp_chunk_obj.size)

class smaf_track_ma2:
	def __init__(self, song_file, end):
		self.format_type = song_file.uint8()
		self.sequence_type = song_file.uint8()
		self.timebase_dur = song_file.uint8()
		self.timebase_gate = song_file.uint8()

		self.channel_stat = song_file.bytesplit16()

		self.sequence = None
		self.setup = None

		trk_iff_obj = song_file.chunk_objmake()
		trk_iff_obj.set_sizes(4, 4, True)
		for chunk_obj in trk_iff_obj.iter(song_file.tell(), end):
			print('MA2 chunk', chunk_obj.id)

			if chunk_obj.id == b'Mtsu': self.setup = song_file.raw(chunk_obj.size)

			if chunk_obj.id == b'Mtsq':
				self.sequence = []
				while song_file.tell() <= chunk_obj.end:
					resttime = calc_gatetime_2(song_file)
					ch_oc, notenum = song_file.bytesplit()

					if (ch_oc, notenum) == (15, 15):
						self.sequence.append([resttime, 0])

					elif (ch_oc, notenum) == (0, 0):
						ch_b, p_type = song_file.bytesplit()
						param = song_file.uint8()
						self.sequence.append([resttime, 1, ch_b>>2, ch_b&3, p_type, param])

					else:
						self.sequence.append([resttime, 2, ch_oc>>2, ch_oc&3, notenum])


class smaf_song:
	def __init__(self):
		self.title = None
		self.comment = None
		self.software = None
		self.tracks2 = [None for _ in range(4)]
		self.tracks3 = [None for _ in range(4)]

	def load_from_file(self, input_file):
		song_file = bytereader.bytereader()
		song_file.load_file(input_file)

		song_file.magic_check(b'MMMD')
		end_file = song_file.uint32_b()

		main_iff_obj = song_file.chunk_objmake()
		main_iff_obj.set_sizes(4, 4, True)
		for chunk_obj in main_iff_obj.iter(8, end_file+6):
			print('MMMD chunk', chunk_obj.id)

			if chunk_obj.id == b'CNTI':
				self.cnti_class = song_file.uint8()
				self.cnti_type = song_file.uint8()
				self.cnti_codetype = song_file.uint8()
				self.cnti_status = song_file.uint8()
				self.cnti_counts = song_file.uint8()

			if chunk_obj.id == b'OPDA':
				for trk_subchunk_obj in chunk_obj.iter(0):
					opda_iff_obj = song_file.chunk_objmake()
					opda_iff_obj.set_sizes(2, 2, True)
					for opda_chunk_obj in opda_iff_obj.iter(trk_subchunk_obj.start, trk_subchunk_obj.end):
						if opda_chunk_obj.id == b'ST': self.title = song_file.raw(opda_chunk_obj.size)
						elif opda_chunk_obj.id == b'CR': self.comment = song_file.raw(opda_chunk_obj.size)
						elif opda_chunk_obj.id == b'VN': self.software = song_file.raw(opda_chunk_obj.size)
						else: print('OPDA chunk:', opda_chunk_obj.id, song_file.raw(opda_chunk_obj.size))

			if chunk_obj.id[:3] == b'MTR':
				mmf_tracknum = chunk_obj.id[3:][0]
				if mmf_tracknum in range(5, 8): self.tracks3[mmf_tracknum-5] = smaf_track_ma3(song_file, chunk_obj.end)
				if mmf_tracknum in range(1, 5): self.tracks2[mmf_tracknum-1] = smaf_track_ma2(song_file, chunk_obj.end)
