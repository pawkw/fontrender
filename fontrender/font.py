from dataclasses import dataclass
import struct
from typing import List

class ByteArrayBuffer:
    def __init__(self, buffer: bytearray) -> None:
        self.buffer = buffer
        self.pointer = 0

    def set_pointer(self, pointer):
        self.pointer = pointer

    def read(self, number_of_bytes):
        result = self.buffer[self.pointer:self.pointer + number_of_bytes]
        self.pointer += number_of_bytes
        return result
    
    def read_uint8(self):
        return struct.unpack('>B', self.read(1))
    
    def read_int16(self):
        return struct.unpack('>h', self.read(2))
    
    def read_uint16(self):
        return struct.unpack('>H', self.read(2))
    

@dataclass
class directory_entry:
    checksum: int
    offset: int
    length: int


flag_names = ['ON_CURVE_POINT', 'X_SHORT_VECTOR', 'Y_SHORT_VECTOR', 'REPEAT_FLAG', 'X_IS_SAME_OR_POSITIVE_X_SHORT_VECTOR',
              'Y_IS_SAME_OR_POSITIVE_Y_SHORT_VECTOR', 'OVERLAP_SIMPLE']
class GlyphFlags:
    def __init__(self, flag_byte: bytes) -> None:
        self.flags = flag_byte

    @property
    def ON_CURVE_POINT(self):
        return self.flags & 1 > 0
    
    @property
    def X_SHORT_VECTOR(self):
        return self.flags & (1 << 1) > 0
    
    @property
    def Y_SHORT_VECTOR(self):
        return self.flags & (1 << 2) > 0
    
    @property
    def REPEAT_FLAG(self):
        return self.flags & (1 << 3) > 0
    
    @property
    def X_IS_SAME_OR_POSITIVE(self):
        return self.flags & (1 << 4) > 0
    
    @property
    def Y_IS_SAME_OR_POSITIVE(self):
        return self.flags & (1 << 5) > 0
    
    @property
    def OVERLAP_SIMPLE(self):
        return self.flags & (1 << 6) > 0
        
@dataclass
class Glyph:
    numberOfContours: int
    xMin: int
    yMin: int
    xMax: int
    yMax: int
    endPtsOfContours: list
    instructionLength: int
    instructions: list
    flags: List[GlyphFlags]
    xCoordinates: List[int]
    yCoordinates: List[int]

    def __init__(self, buffer: ByteArrayBuffer):
        self.numberOfContours, self.xMin, self.yMin, self.xMax, self.yMax = struct.unpack('>hHHHH', buffer.read(12))
        self.compound = self.numberOfContours < 0
        
        if self.compound:
            self.get_compound_glyph(buffer)
        else:
            self.get_simple_glyph(buffer)

    def get_compound_glyph(self, buffer: ByteArrayBuffer):
        pass

    def get_simple_glyph(self, buffer: ByteArrayBuffer):
        for _ in range(self.numberOfContours):
            self.endPtsOfContours.append(struct.unpack(buffer.read_uint16()))

        self.instructionLength = struct.unpack(buffer.read_uint16())
        for _ in range(self.instructionLength):
            self.instructions.append(struct.unpack(buffer.read_uint8()))

        repeat_count = 0
        for _ in range(self.numberOfContours):
            if repeat_count > 0:
                self.flags.append(GlyphFlags(self.flags[-1].flags))
                repeat_count -= 1
                continue

            current_flag = GlyphFlags(buffer.read(1))
            if current_flag.REPEAT_FLAG:
                repeat_count = struct.unpack(buffer.read_uint8())
            self.flags.append(current_flag)
            
        for index in range(self.numberOfContours):
            delta_x = 0
            if self.flags[index].X_SHORT_VECTOR:
                delta_x = buffer.read_uint8()
                if not self.flags[index].X_IS_SAME_OR_POSITIVE:
                    delta_x = -delta_x
            else:
                if self.flags[index].X_IS_SAME_OR_POSITIVE:
                    delta_x = self.xCoordinates[-1]
                else:
                    delta_x = buffer.read_int16()
            self.xCoordinates.append(delta_x)

        for index in range(self.numberOfContours):
            delta_y = 0
            if self.flags[index].Y_SHORT_VECTOR:
                delta_y = buffer.read_uint8()
                if not self.flags[index].Y_IS_SAME_OR_POSITIVE:
                    delta_y = -delta_y
            else:
                if self.flags[index].Y_IS_SAME_OR_POSITIVE:
                    delta_y = self.yCoordinates[-1]
                else:
                    delta_y = buffer.read_int16()
            self.yCoordinates.append(delta_y)

        
            

class PWFont:
    def __init__(self, buffer: bytearray) -> None:
        self.buffer = ByteArrayBuffer(buffer)
        if not buffer:
            return
        
        self.get_offset_table()

        self.directory_entries = {}
        for _ in range(self.numTables):
            self.get_directory_entry()

        
    def get_offset_table(self):
        self.scaler_type, self.numTables, self.searchRange, self.entrySelector, self.rangeShift = struct.unpack('>IHHHH', self.buffer.read(12))

    def get_directory_entry(self):
        tag, checksum, offset, length = struct.unpack('>4sIII', self.buffer.read(16))
        tag = tag.decode('ascii')
        self.directory_entries[tag] = directory_entry(checksum, offset, length)
