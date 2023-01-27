from enum import IntEnum
from .header import Header
from .exceptions import UnknownEntryTypeException
from datetime import datetime
from abc import ABC

class Type(IntEnum):
    DIRECTORY = 0x8427
    FILE = 0x8497

class Entry(ABC):
    PADDING_SIZE = 32
    NAME_SIZE = 448

    @staticmethod
    def deserialize(data):
        """Deserialize the next entry from the byte data stream.

        Args:
            data (bytes): The byte data stream containing the remaining entries.

        Raises:
            UnknownEntryTypeException: Exception is raised when the given entry type was unknown.

        Returns:
            File|Directory: The deserialized file or directory entry instance.
        """
        offset = 0

        # Read header
        header = Header.deserialize(data[offset:offset + Header.SIZE])
        offset += Header.SIZE

        # Read padding
        padding = Entry.__getPadding(data[offset:offset + Entry.PADDING_SIZE])
        offset += Entry.PADDING_SIZE

        # Read name
        name = Entry.__getName(data[offset:offset + Entry.NAME_SIZE])
        offset += Entry.NAME_SIZE

        # Deserialize file entry
        if header.type == Type.FILE:
            entry, entrySize = File.deserialize(header, padding, name, data[offset:])
            return entry, offset + entrySize

        # Deserialize directory entry
        if header.type == Type.DIRECTORY:
            entry, entrySize = Directory.deserialize(header, padding, name, data[offset:])
            return entry, offset + entrySize

        # Unhandled entry
        raise UnknownEntryTypeException(header.type, name)

    @staticmethod
    def __getPadding(data):
        """Get the padding bytes from the given byte stream.

        Args:
            data (bytes): The data stream starting with the padding bytes.

        Returns:
            bytes: The padding bytes retrieved.
        """
        return data[0:Entry.PADDING_SIZE]

    @staticmethod
    def __getName(data):
        """Get the entry name from the data stream, right trimming NULL bytes.

        Args:
            data (bytes): The byte stream starting with the name.

        Returns:
            str: The name retrieved from the byte stream.
        """
        return data[0:Entry.NAME_SIZE].decode('UTF-8').rstrip('\x00')

    def __init__(self,
            name,
            header,
            padding = (b'\x00' * PADDING_SIZE)
        ):
        """Initializes an Entry instance.

        Args:
            name (str): The name of the entry.
            header (Header): The entry header instance.
            padding (bytes): A stream of bytes inserted into the padding section of an entry. Defaults to (b'\x00' * PADDING_SIZE).
        """
        self.name = name
        self.header = header
        self.padding = padding

    def serialize(self):
        """Serialize the entry instance to a byte data stream.

        Returns:
            bytes: The serialized entry instance in byte form.
        """
        data = self.header.serialize()
        data += self.padding
        data += self.name.encode('UTF-8').ljust(Entry.NAME_SIZE, b'\x00')
        return data

    def isFile(self):
        """Is the current entry a file?

        Returns:
            bool: Returns true if the current entry is a file.
        """
        return self.header.type == Type.FILE

    def isDirectory(self):
        """Is the current entry a directory?

        Returns:
            bool: Returns true if the current entry is a directory.
        """
        return self.header.type == Type.DIRECTORY

class Directory(Entry):
    @staticmethod
    def deserialize(header, padding, name, data = b''):
        """Deserialize the directory entry from the byte data stream.

        Args:
            header (Header): The deserialized directory entry header.
            padding (bytes): The padding bytes within the directory entry.
            name (str): The directory entry name.
            data (bytes, optional): The remaining data stream to be deserialized. Defaults to b''.

        Returns:
            Directory: The deserialized directory entry instance.
        """
        return Directory(
            name,
            header.size,
            header,
            padding
        ), 0

    def __init__(self,
            name,
            fileCount = 0,
            header = None,
            padding = (b'\x00' * Entry.PADDING_SIZE)
        ):
        """Initializes a Directory Entry instance.

        Args:
            name (str): The name of the directory.
            fileCount (int, optional): The number of files and directories within this directory. Defaults to 0.
            header (header, optional): The directory entry header instance. Defaults to None.
            padding (bytes, optional): A stream of bytes inserted into the padding section of an entry. Defaults to (b'\x00' * Entry.PADDING_SIZE).
        """
        header = header if header != None else Header(Type.DIRECTORY, fileCount)
        super().__init__(name, header, padding)

    def __str__(self):
        """Get the directory in a unix style file listing string format.

        Returns:
            str: A string containing the modified date and directory name.
        """
        modified = self.header.modified.strftime('%b %d %H:%M')
        if self.header.modified.year < datetime.now().year:
            modified = self.header.modified.strftime('%b %d %Y')
        return f'd {modified: <12} {0: <6} {self.name}'

class File(Entry):
    PAGE_SIZE = 1024

    @staticmethod
    def deserialize(header, padding, name, data = b''):
        """Deserialize the file entry from the byte data stream.

        Args:
            header (Header): The deserialized file entry header.
            padding (bytes): The padding bytes within the file entry.
            name (str): The file entry name.
            data (bytes, optional): The remaining data stream to be deserialized. Defaults to b''.

        Returns:
            File: The deserialized file entry instance.
        """
        # Read content
        content = data[:header.size]

        # Skip padding until alignment
        offset = header.size + File.getContentPaddingSize(header.size)

        # Create entry
        return File(
            name,
            content,
            header,
            padding
        ), offset

    @staticmethod
    def getContentPaddingSize(contentSize):
        """Gets the number of bytes remaining until the content aligns with the page alignment.

        Args:
            contentSize (int): The number of bytes in the file content.

        Returns:
            int: The number of bytes remaining until the end of the next page.
        """
        remaining = File.PAGE_SIZE - (contentSize % File.PAGE_SIZE)
        return 0 if remaining == File.PAGE_SIZE else remaining

    def __init__(self,
            name,
            content = b'', 
            header = None,
            padding = (b'\x00' * Entry.PADDING_SIZE)
        ):
        """Initializes a File Entry instance.

        Args:
            name (str): The name of the file.
            content (bytes, optional): The file binary contents. Defaults to b''.
            header (Header, optional): The file entry header instance. Defaults to None.
            padding (bytes, optional): A stream of bytes inserted into the padding section of an entry. Defaults to (b'\x00' * Entry.PADDING_SIZE).
        """
        header = header if header != None else Header(Type.FILE, len(content))
        self.content = content
        super().__init__(name, header, padding)

    def serialize(self):
        """Serialize the file entry instance to a byte data stream.

        Returns:
            bytes: The serialized file entry instance in byte form.
        """
        self.header.size = len(self.content)

        data = super().serialize()

        # Append content
        if self.header.size > 0:
            data += self.content
            # Page-align content with padding
            data += (b'\x00' * File.getContentPaddingSize(self.header.size))
        return data

    def __str__(self):
        """Get the file in a unix style file listing string format.

        Returns:
            str: A string containing the modified date, file size and file name.
        """
        modified = self.header.modified.strftime('%b %d %H:%M')
        if self.header.modified.year < datetime.now().year:
            modified = self.header.modified.strftime('%b %d %Y')
        return f'- {modified: <12} {self.header.size: <6} {self.name: <16}'