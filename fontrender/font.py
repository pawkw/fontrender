from dataclasses import dataclass

@dataclass
class directory_entry:
    tag: str
    checksum: int
    offset: int
    length: int

    def __init__(self, bytes: bytearray):
        tag = ''
        for index in range(4):
            tag += chr(bytes[index])

        self.tag = tag
        self.checksum = int.from_bytes(bytes[4:8])
        self.offset = int.from_bytes(bytes[8:12])
        self.length = int.from_bytes(bytes[12:16])

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
            print(self.directory_entries[-1].tag)

        
    def get_offset_table(self):
        self.offset_table = {}
        self.offset_table['scaler_type'] = int.from_bytes(self.bytes[0:4], byteorder='big')
        self.offset_table['numTables'] = int.from_bytes(self.bytes[4:6], byteorder='big')
        self.offset_table['searchRange'] = int.from_bytes(self.bytes[6:8], byteorder='big')
        self.offset_table['entrySelector'] = int.from_bytes(self.bytes[8:10], byteorder='big')
        self.offset_table['rangeShift'] = int.from_bytes(self.bytes[10:12], byteorder='big')