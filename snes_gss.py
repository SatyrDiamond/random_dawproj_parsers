# SPDX-FileCopyrightText: 2024 SatyrDiamond
# SPDX-License-Identifier: GPL-3.0-or-later

#from objects.data_bytes import bytereader

import numpy as np

class gss_song:
	def __init__(self):
		self.data_other = {}
		self.data_instrument = {}
		self.data_song = {}
		self.data_pattern = {}

	def load_from_file(self, input_file):
		f = open(input_file, 'r')

		scat = None
		songnum = 0

		for line in f.readlines():
			line = line.strip()
			if line:
				if line[0] == '[': 
					scat = line[1:-1]
					if scat.startswith('Song'):
						songnum = int(scat[4:])
						self.data_pattern[songnum] = {}
				else:
					if scat == 'SNESGSS Module':
						if '=' in line:
							splitl = line.split('=', 1)
							if len(splitl) == 2:
								k_name, k_data = splitl
								if k_name.startswith('Instrument'):
									self.data_instrument[k_name[10:]] = k_data
								elif k_name.startswith('Song'):
									self.data_song[k_name[4:]] = k_data
								else:
									self.data_other[k_name] = k_data
					if scat.startswith('Song'):
						splitl = line.split(' ', 1)
						if len(splitl) == 2:
							k_pos, k_data = splitl
							k_data = k_data.replace('.', ' ')
							speed = k_data[0:2]
							notedata = k_data[2:]
							o = []
							for x in range(len(notedata)//8):
								d = notedata[x*8:8+(x*8)] 
								n, i, e, p = d[0:3], d[3:5], d[5], d[6:8]
								o.append([
									(n if n != '   ' else None),
									(int(i) if i != '  ' else None),
									(e if e != ' ' else None),
									(int(p) if p != '  ' else None),
									])
							self.data_pattern[songnum][int(k_pos)] = o


apeinst_obj = gss_song()
apeinst_obj.load_from_file("G:\\RandomMusicFiles\\tracker_sampler\\snesgss\\test_projects\\test_808.gsm")
