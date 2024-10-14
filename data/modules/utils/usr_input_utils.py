import sys

def getArguments():
    _arguments = list(sys.argv)
    filename_string = _arguments[0]
    _arguments.remove(filename_string)

    for string in _arguments:
        if string.startswith("-"):
            _arguments.remove(string)

    return _arguments

def getOptions():
    _options = list(sys.argv)
    filename_string = _options[0]
    _options.remove(filename_string)

    for string in _options:
        if not string.startswith("-"):
            _options.remove(string)
    
    return _options