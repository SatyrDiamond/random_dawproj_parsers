import struct
import varint
import os
import numpy
import mmap
from io import BytesIO

class chunk_size:
    def __init__(self):
        self.size_id = 4
        self.size_chunk = 4
        self.endian = False
        self.unpackfunc = struct.Struct('<I').unpack

    def set_sizes(self, size_id, size_chunk, endian):
        self.size_id = size_id
        self.size_chunk = size_chunk
        self.endian = endian
        if self.size_chunk == 1: self.unpackfunc = struct.Struct('B').unpack
        if self.size_chunk == 2: self.unpackfunc = struct.Struct('>H' if self.endian else '<H').unpack
        if self.size_chunk == 4: self.unpackfunc = struct.Struct('>I' if self.endian else '<I').unpack

class chunk_loc:
    def __init__(self, byteread, sizedata):
        self.t_byteread = byteread
        self.t_sizedata = sizedata
        self.id = b''
        self.start = 0
        self.end = 0
        self.size = 0

    def iter(self, offset): 
        subchunk_obj = self.t_byteread.chunk_objmake()
        subchunk_obj.sizedata = self.t_sizedata
        return subchunk_obj.iter(self.start+offset, self.end)

    def debugtxt(self):
        print(self.id, self.start, self.end)

class iff_chunkdata:
    def __init__(self, byteread):
        self.byteread = byteread
        self.sizedata = chunk_size()

    def set_sizes(self, size_id, size_chunk, endian):
        self.sizedata.set_sizes(size_id, size_chunk, endian)

    def read(self, end):
        chunk_obj = chunk_loc(self.byteread, self.sizedata)
        chunk_obj.id = self.byteread.read(self.sizedata.size_id)
        chunk_obj.size = self.sizedata.unpackfunc(self.byteread.read(self.sizedata.size_chunk))[0]
        chunk_obj.start = self.byteread.tell()
        chunk_obj.end = chunk_obj.start+chunk_obj.size
        isvalid = chunk_obj.end <= end
        return isvalid, chunk_obj

    def iter(self, start, end):
        pos = self.byteread.tell()
        if start > -1: self.byteread.seek(start)
        while end > self.byteread.tell():
            isvalid, chunk_obj = self.read(end)
            if not isvalid: break
            bpos = self.byteread.tell()
            yield chunk_obj
            self.byteread.seek(bpos+chunk_obj.size)
        self.byteread.seek(pos)



def get_bitnums_int(x):
    return [i for i in range(x.bit_length()) if ((1 << i) & x)]

class bytereader:
    unpack_byte = struct.Struct('B').unpack
    unpack_s_byte = struct.Struct('b').unpack

    unpack_short = struct.Struct('<H').unpack
    unpack_short_b = struct.Struct('>H').unpack
    unpack_s_short = struct.Struct('<h').unpack
    unpack_s_short_b = struct.Struct('>h').unpack
    
    unpack_int = struct.Struct('<I').unpack
    unpack_int_b = struct.Struct('>I').unpack
    unpack_s_int = struct.Struct('<i').unpack
    unpack_s_int_b = struct.Struct('>i').unpack
    
    unpack_float = struct.Struct('<f').unpack
    unpack_float_b = struct.Struct('>f').unpack
    unpack_double = struct.Struct('<d').unpack
    unpack_double_b = struct.Struct('>d').unpack

    def __init__(self):
        self.buf = None
        self.end = 0

    def chunk_objmake(self): 
        return iff_chunkdata(self)

    def load_file(self, filename):
        if os.path.exists(filename):
            file_stats = os.stat(filename)
            self.end = file_stats.st_size
            f = open(filename)
            self.buf = mmap.mmap(f.fileno(), 0, access = mmap.ACCESS_READ)
            return True
        else:
            print('File Not Found', filename)
            return False

    def load_raw(self, rawdata):
        self.end = len(rawdata)
        self.buf = BytesIO(rawdata)

    def magic_check(self, headerbytes):
        if self.buf.read(len(headerbytes)) == headerbytes: return True
        else: raise ValueError

    def detectheader(self, startloc, headerbytes):
        pos = self.buf.tell()
        return self.buf.read(len(headerbytes)) == headerbytes
        self.buf.seek(pos)

    def read(self, num): return self.buf.read(num)

    def tell(self): return self.buf.tell()

    def seek(self, num): return self.buf.seek(num)

    def skip(self, num): return self.buf.seek(self.buf.tell()+num)

    def remaining(self): return max(0, self.end - self.buf.tell())

    def bytesplit(self):
        value = self.uint8()
        return value >> 4, value & 0x0F

    def bytesplit16(self):
        value1 = self.uint8()
        value2 = self.uint8()
        return value1 >> 4, value1 & 0x0F, value2 >> 4, value2 & 0x0F

    def uint8(self): return self.unpack_byte(self.buf.read(1))[0]
    def int8(self): return self.unpack_s_byte(self.buf.read(1))[0]

    def uint16(self): return self.unpack_short(self.buf.read(2))[0]
    def uint16_b(self): return self.unpack_short_b(self.buf.read(2))[0]
    def int16(self): return self.unpack_s_short(self.buf.read(2))[0]
    def int16_b(self): return self.unpack_s_short_b(self.buf.read(2))[0]

    def uint24(self): return self.unpack_int(b'\x00'+self.buf.read(3))[0]
    def uint24_b(self): return self.unpack_int_b(self.buf.read(3)+b'\x00')[0]

    def uint32(self): return self.unpack_int(self.buf.read(4))[0]
    def uint32_b(self): return self.unpack_int_b(self.buf.read(4))[0]
    def int32(self): return self.unpack_s_int(self.buf.read(4))[0]
    def int32_b(self): return self.unpack_s_int_b(self.buf.read(4))[0]

    def float(self): return self.unpack_float(self.buf.read(4))[0]
    def float_b(self): return self.unpack_float_b(self.buf.read(4))[0]

    def double(self): return self.unpack_double(self.buf.read(8))[0]
    def double_b(self): return self.unpack_double_b(self.buf.read(8))[0]

    def flags8(self): return get_bitnums_int(self.uint8())
    def flags16(self): return get_bitnums_int(self.uint16())
    def flags24(self): return get_bitnums_int(self.uint24())
    def flags32(self): return get_bitnums_int(self.uint32())

    def table8(self, tabledata):
        numbytes = numpy.prod(tabledata)
        return numpy.frombuffer(self.buf.read(numbytes), numpy.uint8).reshape(*tabledata)

    def table16(self, tabledata):
        numbytes = numpy.prod(tabledata)*2
        return numpy.frombuffer(self.buf.read(numbytes), numpy.uint16).reshape(*tabledata)

    def stable8(self, tabledata):
        numbytes = numpy.prod(tabledata)
        return numpy.frombuffer(self.buf.read(numbytes), numpy.int8).reshape(*tabledata)

    def stable16(self, tabledata):
        numbytes = numpy.prod(tabledata)*2
        return numpy.frombuffer(self.buf.read(numbytes), numpy.int16).reshape(*tabledata)

    def varint(self): return varint.decode_stream(self.buf)

    def raw(self, size): return self.buf.read(size)

    def rest(self): return self.buf.read()

    def string(self, size, **kwargs): return self.buf.read(size).split(b'\x00')[0].decode(**kwargs)
    def string16(self, size): return self.buf.read(size*2).decode("utf-16")

    def l_uint8(self, num): return [self.uint8() for _ in range(num)]
    def l_int8(self, num): return [self.int8() for _ in range(num)]

    def l_uint16(self, num): return [self.uint16() for _ in range(num)]
    def l_uint16_b(self, num): return [self.uint16_b() for _ in range(num)]
    def l_int16(self, num): return [self.int16() for _ in range(num)]
    def l_int16_b(self, num): return [self.int16_b() for _ in range(num)]

    def l_uint32(self, num): return [self.uint32() for _ in range(num)]
    def l_uint32_b(self, num): return [self.uint32_b() for _ in range(num)]
    def l_int32(self, num): return [self.int32() for _ in range(num)]
    def l_int32_b(self, num): return [self.int32_b() for _ in range(num)]

    def l_float(self, num): return [self.float() for _ in range(num)]
    def l_float_b(self, num): return [self.float_b() for _ in range(num)]

    def l_double(self, num): return [self.double() for _ in range(num)]
    def l_double_b(self, num): return [self.double_b() for _ in range(num)]

    def c_string__int8(self, **kwargs): return self.string(self.uint8(), **kwargs)
    def c_string__int16(self, endian, **kwargs): return self.string(self.uint16_b() if endian else self.uint16(), **kwargs)
    def c_string__int32(self, endian, **kwargs): return self.string(self.uint32_b() if endian else self.uint32(), **kwargs)

    def string_t(self, **kwargs):
        output = b''
        terminated = 0
        while terminated == 0:
            char = self.buf.read(1)
            if char not in [b'\x00', b'']: output += char
            else: terminated = 1
        return output.decode(**kwargs)
