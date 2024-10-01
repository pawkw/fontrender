from dataclasses import dataclass
import struct

@dataclass
class directory_entry:
    tag: str
    checksum: int
    offset: int
    length: int

    def __init__(self, bytes: bytearray):
        tag, checksum, offset, length = struct.unpack('>4sIII', bytes)

        self.tag = tag.decode('ascii')
        self.checksum = checksum
        self.offset = offset
        self.length = length

@dataclass
class Glyph:
    numberOfContours: int
    xMin: int
    yMin: int
    xMax: int
    yMax: int

    def __init__(self, bytes: bytearray):
        numberOfContours, xMin, yMin, xMax, yMax = struct.unpack('>IIIII', bytes[0:12])
        self.numberOfContours = numberOfContours
        self.xMin = xMin
        self.yMin = yMin
        self.xMax = xMax
        self.yMax = yMax


class PWFont:
    def __init__(self, bytes: bytearray) -> None:
        self.bytes = bytes
        if not bytes:
            return
        
        self.get_offset_table()

        self.directory_entries = []
        index = 12
        for entry in range(self.offset_table['numTables']):
            offset = index+(entry*16)
            self.directory_entries.append(directory_entry(self.bytes[offset:offset+16]))
            print(f'entry: {self.directory_entries[-1].tag} location: {self.directory_entries[-1].offset}')

        
    def get_offset_table(self):
        self.offset_table = {}
        
        self.offset_table['scaler_type'] = struct.unpack('>I', self.bytes[0:4])[0]
        self.offset_table['numTables'] = struct.unpack('>H', self.bytes[4:6])[0]
        self.offset_table['searchRange'] = struct.unpack('>H', self.bytes[6:8])[0]
        self.offset_table['entrySelector'] = struct.unpack('>H', self.bytes[8:10])[0]
        self.offset_table['rangeShift'] = struct.unpack('>H', self.bytes[10:12])[0]
