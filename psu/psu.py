from .exceptions import EntryNotFoundException
from .entry import Entry, File, Directory, Type
import os

class PSU:
    @staticmethod
    def create(filepath):
        """Create a new PSU object.

        Args:
            filepath (str): The filepath where the PSU should be saved on disk.

        Returns:
            PSU: The newly created PSU object instance.
        """

        base = os.path.splitext(os.path.basename(filepath))[0]

        psu = PSU(filepath)
        psu.add(Directory(base))
        psu.add(Directory('.'))
        psu.add(Directory('..'))
        return psu

    @staticmethod
    def load(filepath):
        """Loads a PSU object from parsing a file on disk.

        Args:
            filepath (str): The filepath where the PSU exists on disk.

        Returns:
            PSU: The loaded PSU object instance.
        """
        psu = PSU(filepath)
        with open(psu.filepath, 'rb') as f:
            psu.__parse(f.read())
        return psu

    def __init__(self, filepath):
        """Initializes a new PSU instance.

        Args:
            filepath (str): The filepath where the PSU is located on disk.
        """
        self.filepath = filepath
        self.entries = []

    def __parse(self, data):
        """Parses the PSU entries within the given data stream.

        Args:
            data (bytes): The PSU file byte data stream.

        Returns:
            list(Entry): The parsed entries within the PSU instance.
        """
        self.entries = []

        offset = 0
        while offset < len(data):
            # Parse the next entry
            entry, size = Entry.deserialize(data[offset:])
            self.entries.append(entry)
            offset += size

        return self.entries

    def __index(self, entryName, type = None):
        """_summary_

        Args:
            entryName (str): The entry name to search for within the PSU.
            type (Type): Restrict the search to only find entries of the given type. Defaults to None.

        Raises:
            EntryNotFoundException: Exception is raised when the given entry name was not found in the PSU instance.

        Returns:
            integer: The array index the entry exists at.
        """
        for i in range(0, len(self.entries)):
            if self.entries[i].name == entryName and (type == None or self.entries[i].header.type == type):
                return i
        raise EntryNotFoundException(entryName)

    def add(self, entry):
        """Add an entry to the list of entries in the PSU.

        Args:
            entry (Entry): The entry to be added.
        """
        self.entries.append(entry)

    def write(self, entryName, data):
        """Write an existing or new entry to the PSU with the given data.

        Args:
            entryName (str): The entry file name to be wrote.
            data (bytes|str): The entry file contents to be wrote.

        Returns:
            Entry: The new or existing entry that has had the data wrote to it.
        """

        # Convert string to bytes
        if type(data) == str:
            data = data.encode('UTF-8')

        # Update existing file entry
        if self.has(entryName):
            entry = self.get(entryName)
            entry.content = data
            entry.header.size = len(data)
            return entry

        # Insert a new file entry
        entry = File(entryName, data)
        self.add(entry)
        return entry

    def read(self, entryName):
        """Read an existing entries file contents.

        Args:
            entryName (str): The entry file name to read.

        Returns:
            bytes: The entry file contents.
        """
        return self.get(entryName, Type.FILE).content

    def save(self, filepath = None):
        """Save the PSU instance to a file.

        Args:
            filepath (str, optional): The destination filepath to save the PSU to. If none is provided, then the instance property filepath is used. Defaults to None.
        """
        filepath = filepath if filepath != None else self.filepath

        # Generate PSU file
        data = b''
        for entry in self.entries:
            # Resolve directory sizes
            if entry.header.type == Type.DIRECTORY:
                if entry.name == '.' or entry.name == '..':
                    # "." and ".." directories have 0 size
                    entry.header.size = 0
                else:
                    # Other directories size are the number of entries
                    entry.header.size = len(self.entries) - 1

            # Serialize the entry
            data += entry.serialize()

        # Write data to file
        with open(filepath, 'wb') as f:
            f.write(data)

    def copy(self, filepath, entryName):
        """Import the given filepath file to the PSU instance identified by the entry name.

        Args:
            filepath (str): The filepath location for the entry to be imported from.
            entryName (str): The name of the entry to be imported.
        """
        # Read data from file
        with open(filepath, 'rb') as f:
            self.write(entryName, f.read())

    def export(self, entryName, filepath):
        """Export the entry identified by the entry name to the given filepath.

        Args:
            entryName (str): The name of the entry to be exported.
            filepath (str): The filepath location for the entry to be exported to.
        """
        # Write entry content to filepath
        with open(filepath, 'wb') as f:
            f.write(self.read(entryName))

    def delete(self, entryName):
        """Deletes the given entry from the list of entries.

        Args:
            entryName (str): The entry name to be deleted.
        """
        index = self.__index(entryName)
        del self.entries[index]

    def list(self):
        """Gets the entries associated with the PSU instance.

        Returns:
            list(Entry): The entries within the PSU instance.
        """
        return self.entries

    def get(self, entryName, type = None):
        """Gets the entry in the PSU instance for the given entry name.

        Args:
            entryName (str): The entry name to search for within the PSU.
            type (Type): Restrict the search to only find entries of the given type. Defaults to None.

        Raises:
            EntryNotFoundException: Exception is raised when the given entry name was not found in the PSU instance.

        Returns:
            Entry: The entry instance for the given entry name.
        """
        return self.entries[self.__index(entryName, type)]

    def has(self, entryName):
        """Checks if the PSU instance contains the given entry name.

        Args:
            entryName (str): The entry name to search for.

        Returns:
            bool: If the entry name exists within the PSU instance.
        """
        try:
            self.get(entryName)
            return True
        except EntryNotFoundException:
            return False

    def isFile(self, entryName):
        """Is the given entry name a file?

        Args:
            entryName (str): The entry name to search for within the PSU.

        Raises:
            EntryNotFoundException: Exception is raised when the given entry name was not found in the PSU instance.

        Returns:
            bool: Returns true if the given entry name is a file.
        """
        return self.get(entryName).isFile()

    def isDirectory(self, entryName):
        """Is the given entry name a directory?

        Args:
            entryName (str): The entry name to search for within the PSU.

        Raises:
            EntryNotFoundException: Exception is raised when the given entry name was not found in the PSU instance.

        Returns:
            bool: Returns true if the given entry name is a directory.
        """
        return self.get(entryName).isDirectory()

    def __str__(self):
        """Get the PSU in a unix style file listing string format.

        Returns:
            str: A string containing a list of files and directories within the PSU instance.
        """
        value = f'total {len(self.list())}\n'
        for entry in self.list():
            value += f'{entry}\n'
        return value