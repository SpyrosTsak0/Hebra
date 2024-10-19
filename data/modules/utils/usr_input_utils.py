import sys

def getArguments():
    _arguments = list(sys.argv)
    filename_string = _arguments[0]
    _arguments.remove(filename_string)

    return _arguments

def getAccessToken():
    token = input("Enter your access token: ")
    return token