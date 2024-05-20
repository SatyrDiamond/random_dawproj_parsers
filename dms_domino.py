import struct
import zlib
from objects import bytereader

def printchunk(num, trk_chunkid, trk_chunk_obj, song_data):
	print('\t'*num, trk_chunkid, trk_chunk_obj.size, song_data.raw(min(trk_chunk_obj.size, 16)))

class dms_project:
	def __init__(self):
		self.chunks = []

	def load_from_file(self, input_file):
		song_file = bytereader.bytereader()
		song_file.load_file(input_file)
		song_file.magic_check(b'PortalSequenceData\xcb\x13\x00\x00')
		song_data = bytereader.bytereader()
		song_data.load_raw(zlib.decompress(song_file.rest(), zlib.MAX_WBITS|32))

		main_iff_obj = song_data.chunk_objmake()
		main_iff_obj.set_sizes(2, 4, False)

		for chunk_obj in main_iff_obj.iter(0, song_data.end):
			chunkid = int.from_bytes(chunk_obj.id, 'little')

			printchunk(0, chunkid, chunk_obj, song_data)

			if chunkid in [1003, 1008]:
				for trk_chunk_obj in chunk_obj.iter():
					trk_chunkid = int.from_bytes(trk_chunk_obj.id, 'little')
					printchunk(1, trk_chunkid, trk_chunk_obj, song_data)
					if trk_chunkid in [2009, 1010, 2008, 2001]:
						for trk_subchunk_obj in trk_chunk_obj.iter():
							subchunkid = int.from_bytes(trk_subchunk_obj.id, 'little')
							printchunk(2, subchunkid, trk_subchunk_obj, song_data)


testin = dms_project()
testin.load_from_file(
'noname.dms' 
)

