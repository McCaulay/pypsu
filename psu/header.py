import struct
from datetime import datetime

class Header:
    """Header binary structure

    struct timestamp
    {
        uint8_t zero;    // 0x00
        uint8_t seconds; // 0x01
        uint8_t minutes; // 0x02
        uint8_t hours;   // 0x03
        uint8_t days;    // 0x04
        uint8_t months;  // 0x05
        uint16_t year;   // 0x06
    }; // 0x08

    struct header
    {
        uint16_t type;      // 0x00
        uint16_t unk1;      // 0x02
        uint32_t size;      // 0x04
        timestamp created;  // 0x08
        uint16_t sector;    // 0x10
        uint16_t unk2;      // 0x12
        uint32_t unk3;      // 0x14
        timestamp modified; // 0x18
    }; // 0x20
    """
    FORMAT = '<HHI6BHHHI6BH'
    SIZE = 0x20

    @staticmethod
    def deserialize(data):
        """Deserialized the header bytes from the given data stream into a header instance.

        Args:
            data (bytes): The data stream of bytes containing the entry header.

        Returns:
            Header: The deserialized header instance.
        """
        header = struct.unpack(Header.FORMAT, data)
        return Header(
            header[0], # type
            header[2], # size
            datetime(header[9], header[8], header[7], header[6], header[5], header[4]), # created
            datetime(header[19], header[18], header[17], header[16], header[15], header[14]), # modified
            header[10], # sector
            header[1],  # unk1
            header[11], # unk2
            header[12], # unk3
        )

    def __init__(self,
        type,
        size,
        created = datetime.now(),
        modified = datetime.now(),
        sectorAddress = 0,
        unk1 = 0,
        unk2 = 0,
        unk3 = 0
    ):
        """Initializes an Entry Header instance.

        Args:
            type (Type): The entry type.
            size (int): The entry size. For a directory this is the number of files and directories. For a file this is the content size.
            created (datetime, optional): The date and time the entry was created. Defaults to datetime.now().
            modified (datetime, optional): The date and time the entry was last modified. Defaults to datetime.now().
            sectorAddress (int, optional): The start sector address to write the file content to in the memory card. Defaults to 0.
            unk1 (int, optional): Unknown, but always appear to be 0. Defaults to 0.
            unk2 (int, optional): Unknown. Defaults to 0.
            unk3 (int, optional): Unknown. Defaults to 0.
        """
        self.type = type
        self.size = size
        self.created = created
        self.modified = modified
        self.sectorAddress = sectorAddress
        self.unk1 = unk1
        self.unk2 = unk2
        self.unk3 = unk3

    def serialize(self):
        """Serializes the header into a bytes data stream.

        Returns:
            bytes: The serialized header in a byte stream.
        """
        return struct.pack(
            Header.FORMAT,
            self.type,
            self.unk1,
            self.size,
            0,
            self.created.second,
            self.created.minute,
            self.created.hour,
            self.created.day,
            self.created.month,
            self.created.year,
            self.sectorAddress,
            self.unk2,
            self.unk3,
            0,
            self.modified.second,
            self.modified.minute,
            self.modified.hour,
            self.modified.day,
            self.modified.month,
            self.modified.year
        )
