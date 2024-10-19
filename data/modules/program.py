import data.modules.commands.main_commands as main_commands
import data.modules.utils.usr_input_utils as usr_input_utils

def run():

    arguments = usr_input_utils.getArguments()
    arguments_length = len(arguments)
    options = usr_input_utils.getOptions()

    
    if arguments_length > 0:
        command = arguments[0]

        match command:
        
            case "status":
            
                for option in options:
                    match option:
                        case "--update" | "-u":
                            token = usr_input_utils.getAccessToken()
                            main_commands.updateStatus(token)

                main_commands.printStatus()
                    
            case "--help":
                main_commands.printHelp()
        
            case "alter":

                token = usr_input_utils.getAccessToken()
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
                

                main_commands.alterStatus(token, auto_delete_bool, repository_names)
                main_commands.updateStatus(token)
                main_commands.printStatus()
            
            case _:
                print("Invaild command. To check the list of available commands, run '--help'")
                sys.exit(1)     
    else:
        main_commands.printHelp()       
