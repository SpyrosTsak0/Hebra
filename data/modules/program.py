from data.modules.commands.main_commands import *
from data.modules.utils.usr_input import *

def run():

    arguments = getArguments()
    arguments_length = len(arguments)
    options = getOptions()

    
    if arguments_length > 0:
        command = arguments[0]

        match command:
        
            case "status":
            
                for option in options:
                    match option:
                        case "--update" | "-u":
                            token = getAccessToken()
                            updateStatus(token)

                printStatus()
                    
            case "--help":
                printHelp()
        
            case "alter":

                token = getAccessToken()
                auto_delete_bool = True

                for option in options:
                    match option:
                        case "--enable" | "-e":
                            auto_delete_bool = True
                        case "--disable" | "-d":
                            auto_delete_bool = False

                repository_names = None
            
                if arguments_length > 1:
                    repository_names = list()

                    for arguments_count in range(1, arguments_length):
                        argument = arguments[arguments_count]
                        repository_names.append(argument)
                

                alterStatus(token, auto_delete_bool, repository_names)

                printStatus()
            
            case _:
                printInvalidCommand()     
    else:
        printHelp()       
