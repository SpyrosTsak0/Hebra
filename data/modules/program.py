import data.modules.commands.main_commands as main_commands
import data.modules.utils.usr_input_utils as usr_input_utils

def run():

    arguments = usr_input_utils.getArguments()
    arguments_length = len(arguments)

    
    if arguments_length > 0:
        
        command = arguments[0]
        subcommand = None

        if arguments_length > 1:
            subcommand = arguments[1]

        match command:
        
            case "status":
            
                main_commands.printStatus()
            
            case "update":
                
                token = usr_input_utils.getAccessToken()
                main_commands.updateStatus(token)
                    
            case "help":
                main_commands.printHelp()
        
            case "auto-delete":

                auto_delete_bool = True
   
                match subcommand:
                    case "enable":
                        auto_delete_bool = True
                    case "disable":
                        auto_delete_bool = False
                    case _:
                        main_commands.printSubcommandNotSpecifiedAndExit("auto-delete")
                
                token = usr_input_utils.getAccessToken()
                repository_names = None
            
                if arguments_length > 2:
                    repository_names = list()

                    for arguments_count in range(2, arguments_length):
                        argument = arguments[arguments_count]
                        repository_names.append(argument)
                

                main_commands.alterRepositoriesAutoDeleteHeadStatus(token, auto_delete_bool, repository_names)
                main_commands.updateStatus(token)
            
            case _:
                main_commands.printInvalidCommandAndExit()     
    else:
        main_commands.printHelp()       
