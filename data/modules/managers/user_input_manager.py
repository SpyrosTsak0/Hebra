import sys

class UserInputManager:

    def getArguments(self):
        arguments = self.__getArguments()

        for argument in arguments:
            if argument.startswith("--"):
                arguments.remove(argument)
    
        return arguments

    def getFlags(self):
        arguments = self.__getArguments()
        flags = list()

        for argument in arguments:
            if argument.startswith("--"):
                flags.append(argument)
        
        return flags

    def getAccessToken(self):
        token = input("Enter your access token: ")
        return token

    def __getArguments(self):
        arguments = list(sys.argv)
        filename_string = arguments[0]
        arguments.remove(filename_string)
        return arguments