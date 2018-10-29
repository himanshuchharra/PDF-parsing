class InvalidBankNameException(Exception):
    """
    Invalid bank name exception
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class ScannedPDFException(Exception):
    """
    Unable to parse the scanned pdf
    """
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
