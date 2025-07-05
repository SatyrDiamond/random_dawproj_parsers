from objects.data_bytes import bytereader

def valprint(tabv, txt, val, **k):
	print(('\t'*tabv)+txt.rjust(8), val, **k)

class massiva_clip:
	def __init__(self, byr_stream):
		self.chunks = []
		self.events = []
		if byr_stream: self.read(byr_stream)

	def read(self, byr_stream):
		self.name = byr_stream.c_string__int8()
		self.pos = byr_stream.uint32_b()
		self.dur = byr_stream.uint32_b()
		self.unk1 = byr_stream.uint32_b()
		self.unk2 = byr_stream.uint32_b()
		num_events = byr_stream.uint32_b()
		for x in range(num_events):
			dpos = byr_stream.uint32_b()
			eventdata = []
			eventdata.append(byr_stream.uint8())
			eventdata.append(byr_stream.uint8())
			eventdata.append(byr_stream.uint8())
			eventdata += byr_stream.bytesplit() # type, channel
			self.events.append([dpos,eventdata])

class massiva_track:
	def __init__(self, byr_stream, vers):
		self.clips = []
		if byr_stream: self.read(byr_stream, vers)

	def read(self, byr_stream, vers):
		if vers == 1: byr_stream.skip(4)
		self.name = byr_stream.c_string__int8()
		self.channel = byr_stream.uint32_b()
		self.bank = byr_stream.uint32_b()
		self.patch = byr_stream.uint32_b()
		self.unk4 = byr_stream.uint32_b()
		self.vol = byr_stream.uint32_b()
		self.pan = byr_stream.uint32_b()
		self.reverb = byr_stream.uint32_b()
		self.chorus = byr_stream.uint32_b()
		if vers == 1: byr_stream.skip(12)
		num_clips = byr_stream.uint32_b()
		self.clips = [massiva_clip(byr_stream) for x in range(num_clips)]

class massiva_area:
	def __init__(self, byr_stream):
		self.name = ''
		self.start = 0
		self.end = 0
		self.unk1 = 0
		if byr_stream: self.read(byr_stream)

	def read(self, byr_stream):
		self.name = byr_stream.c_string__int8()
		self.start = byr_stream.uint32_b()
		self.end = byr_stream.uint32_b()
		self.unk1 = byr_stream.uint32_b()

class massiva_proj:
	def __init__(self):
		self.name = ''
		self.tracks = []
		self.areas = []
		self.bpm = 120
		self.mastertempo = 120
		self.version = 0

	def load_from_file(self, input_file):
		byr_stream = bytereader.bytereader()
		byr_stream.load_file(input_file)
		size = byr_stream.raw( byr_stream.uint8() )
		while byr_stream.remaining():
			name = byr_stream.c_string__int8()
			#print('NAME', name)
			if name == 'Name':
				self.name = byr_stream.c_string__int8()
			elif name == 'Version':
				self.version = byr_stream.uint32_b()
			elif name == 'Tempo':
				self.bpm = byr_stream.uint32_b()
			elif name == 'MasterTempo':
				self.mastertempo = byr_stream.l_uint32_b(byr_stream.uint32_b())
			elif name == 'Tracks':
				num_tracks = byr_stream.uint32_b()
				self.tracks = [massiva_track(byr_stream, self.version) for x in range(num_tracks)]
			elif name == 'Area':
				num_areas = byr_stream.int32_b()+1
				self.areas = [massiva_area(byr_stream) for x in range(num_areas)]
			else:
				break
				#exit('unknown tag: '+name)

input_file = "G:\\winapps\\MASSIVA\\test.seq"
test_obj = massiva_proj()
test_obj.load_from_file(input_file)
