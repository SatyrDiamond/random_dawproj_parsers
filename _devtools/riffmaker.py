
import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 

from objects.data_bytes import riff_chunks

input_file = "Sample Playlist.mmp"

itemlist = []
grouplist = []
chunk_items_root = {}
chunk_items_inside = {}

def ci(acidchunks, byr_stream, t, insidename):
	for x in acidchunks.iter_wseek(byr_stream):
		print('\t'*t+('ITEM  -' if not x.is_list else 'GROUP -'), x.name, end='')
		if x.is_list:
			if not insidename:
				chunk_items_root[x.name] = 'group'
			else:
				if insidename not in chunk_items_inside: chunk_items_inside[insidename] = {}
				chunk_items_inside[insidename][x.name] = 'group'
			if x.name not in grouplist: grouplist.append(x.name)
			print()
			ci(x, byr_stream, t+1, x.name)
		else:
			if not insidename:
				chunk_items_root[x.name] = 'item'
			else:
				if insidename not in chunk_items_inside: chunk_items_inside[insidename] = {}
				chunk_items_inside[insidename][x.name] = 'item'
			if x.name not in itemlist: itemlist.append(x.name)
			print(' ', x.size, '>', byr_stream.raw( min(30, x.size) ).hex() )

filelist = [
input_file,
]

for x in filelist:
	if os.path.exists(x):
		print(x)
		acidchunks = riff_chunks.riff_chunk()
		byr_stream = acidchunks.load_from_file(x, False)
		ci(acidchunks, byr_stream, 0, None)

print('')
print('--------------------- ROOT ITEMS ---------------------')

for d,f in chunk_items_root.items():
	print(d,f)


print('')
print('--------------------- INSIDE ITEMS ---------------------')

for insidename, x in chunk_items_inside.items():
	print(insidename, 'contains:')
	for d,f in x.items():
		print('\t',d,f)


def outline(f, t, writetxt):
	f.write(('\t'*t+writetxt).encode()+b'\n')

f = open('out.py', 'wb')


outline(f, 0, '# ---------------------- ITEMS ----------------------')

for i in itemlist:
	ddn = i.decode().lower()
	outline(f, 0, 'class item_%s:' % (ddn))
	outline(f, 1, 'def __init__(self):')
	outline(f, 2, 'self.data = None')
	outline(f, 0, '')

	outline(f, 1, '@classmethod')
	outline(f, 1, 'def from_byr_stream(cls, byr_stream, size):')
	outline(f, 2, 'cls = cls()')
	outline(f, 2, 'with byr_stream.isolate_size(size, False) as bye_stream:')
	outline(f, 3, 'cls.data = bye_stream.raw(size)')
	outline(f, 2, 'return cls')
	outline(f, 0, '')
	outline(f, 0, '')

	#@classmethod
	#def fromxml(cls, xmldata):
	#	cls = cls()
	#	if "td" in xmldata.attrib: cls.td = int(xmldata.attrib['td'])
	#	if "k-end-time" in xmldata.attrib: cls.k_end_time = int(xmldata.attrib['k-end-time'])
	#	if "k-type" in xmldata.attrib: cls.k_type = int(xmldata.attrib['k-type'])
	#	if "k-root" in xmldata.attrib: cls.k_root = int(xmldata.attrib['k-root'])
	#	if "k-lo-bits" in xmldata.attrib: cls.k_lo_bits = int(xmldata.attrib['k-lo-bits'])
	#	if "k-hi-bits" in xmldata.attrib: cls.k_hi_bits = int(xmldata.attrib['k-hi-bits'])
	#	if "k-label" in xmldata.attrib: cls.k_label = xmldata.attrib['k-label']
	#	return cls


outline(f, 0, 'from objects.data_bytes import riff_chunks')


outline(f, 0, '# ---------------------- ROOT ----------------------')

outline(f, 0, 'class root_group:')
outline(f, 1, 'def __init__(self):')
for dn, dt in chunk_items_root.items():
	ddn = dn.decode().lower()
	outline(f, 2, 'self.data_%s = []' % ddn)

outline(f, 0, '')
outline(f, 1, 'def load_from_file(self, input_file):')
outline(f, 2, 'riffchunks = riff_chunks.riff_chunk()')
outline(f, 2, 'byr_stream = riffchunks.load_from_file(input_file, False)')
outline(f, 2, 'for x in riffchunks.iter_wseek(byr_stream):')
firstdata = True
for dn, dt in chunk_items_root.items():
	ddn = dn.decode().lower()
	ifd = 'if' if firstdata else 'elif'
	if dt == 'group':
		outline(f, 3, ifd+' x.name == %s:' % (str(dn)))
		outline(f, 4, 'if x.is_list:')
		outline(f, 5, 'self.data_%s.append(group_%s.from_riffchunks(x, byr_stream))' % (ddn, ddn))
		outline(f, 4, 'else:')
		outline(f, 5, "print(x.name, 'is not a group')")

	if dt == 'item':
		outline(f, 3, ifd+' x.name == %s:' % (str(dn)))
		outline(f, 4, 'if not x.is_list:')
		outline(f, 5, 'self.data_%s.append(item_%s.from_byr_stream(byr_stream, x.size))' % (ddn, ddn))
		outline(f, 4, 'else:')
		outline(f, 5, "print(x.name, 'is not an item')")
	firstdata = False
outline(f, 3, "else: print('unknown chunk in root: '+str(x.name))")
outline(f, 0, '')
outline(f, 0, '')


outline(f, 0, '# ---------------------- GROUP ----------------------')

for insidename, x in chunk_items_inside.items():
	grouplist.remove(insidename)

	outline(f, 0, 'class group_%s:' % (insidename.decode().lower()))
	outline(f, 1, 'def __init__(self):')
	for dn, dt in x.items():
		ddn = dn.decode().lower()
		outline(f, 2, 'self.data_%s = []' % (ddn))
	outline(f, 0, '')

	outline(f, 1, '@classmethod')
	outline(f, 1, 'def from_riffchunks(cls, riffchunks, byr_stream):')
	outline(f, 2, 'cls = cls()')
	outline(f, 2, 'for x in riffchunks.iter_wseek(byr_stream):')
	firstdata = True
	for dn, dt in x.items():
		ddn = dn.decode().lower()
		ifd = 'if' if firstdata else 'elif'
		if dt == 'group':
			outline(f, 3, ifd+' x.name == %s:' % (str(dn)))
			outline(f, 4, 'if x.is_list:')
			outline(f, 5, 'cls.data_%s.append(group_%s.from_riffchunks(x, byr_stream))' % (ddn, ddn))
			outline(f, 4, 'else:')
			outline(f, 5, "print(x.name, 'is not a group')")
		if dt == 'item':
			outline(f, 3, ifd+' x.name == %s:' % (str(dn)))
			outline(f, 4, 'if not x.is_list:')
			outline(f, 5, 'cls.data_%s.append(item_%s.from_byr_stream(byr_stream, x.size))' % (ddn, ddn))
			outline(f, 4, 'else:')
			outline(f, 5, "print(x.name, 'is not an item')")
		firstdata = False
	outline(f, 3, "else: print('unknown chunk in %s: '+str(x.name))" % insidename.decode())
	outline(f, 2, 'return cls')

	outline(f, 0, '')
	outline(f, 0, '')

for insidename in grouplist:
	outline(f, 0, 'class group_%s:' % (insidename.decode().lower()))
	outline(f, 1, 'def __init__(self):')
	outline(f, 2, 'self.data = []')
	outline(f, 0, '')

	outline(f, 1, '@classmethod')
	outline(f, 1, 'def from_riffchunks(cls, riffchunks, byr_stream):')
	outline(f, 2, 'cls = cls()')
	outline(f, 2, 'cls.data  = [x for x in riffchunks.iter_wseek(byr_stream)]')
	outline(f, 2, 'return cls')

	outline(f, 0, '')
	outline(f, 0, '')

outline(f, 0, 'input_file = "%s"' % input_file.replace('\\', '\\\\'))

outline(f, 0, 'test_obj = root_group()')
outline(f, 0, 'test_obj.load_from_file(input_file)')
