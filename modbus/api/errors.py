class UnexpectedInputSize(Exception):
    "Raised when the size value and the size of the values list does not match"
    pass

class MissingArgument(Exception):
    "Tried to call function but not all arguments needed were present"
    pass