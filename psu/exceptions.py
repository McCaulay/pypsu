class PSUException(Exception):
    pass

class EntryNotFoundException(PSUException):
    def __init__(self, entryName, message = None):
        """Exception raised when a given entry name was not found.

        Args:
            entryName (str): The entry name which was searched for.
            message (string, optional): A custom message to be displayed in the exception. Defaults to None.
        """
        self.entryName = entryName

        message = message if message != None else f'Entry "{entryName}" not found'
        super().__init__(message)

class UnknownEntryTypeException(PSUException):
    def __init__(self, type, entryName, message = None):
        """Exception raised when an unknown entry type header value was found.

        Args:
            type (int): The type value found.
            entryName (str): The entry name which has an unknown type value.
            message (string, optional): A custom message to be displayed in the exception. Defaults to None.
        """
        self.type = type
        self.entryName = entryName

        message = message if message != None else f'Unknown type value "{type:04x}" found for entry "{entryName}"'
        super().__init__(message)

class EntryNotAFileException(PSUException):
    def __init__(self, entry, message = None):
        """Exception raised when an entry was required to be a file but was not.

        Args:
            entry (Entry): The entry which is not a file.
            message (string, optional): A custom message to be displayed in the exception. Defaults to None.
        """
        self.type = type
        self.entry = entry

        message = message if message != None else f'Entry "{entry.name}" is not a file'
        super().__init__(message)