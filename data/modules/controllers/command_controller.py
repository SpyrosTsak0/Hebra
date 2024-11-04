
class CommandController:
    def __init__(self, base_classes, constants, repository_manager, error_manager, user_input_manager):
        self.base_classes = base_classes
        self.constants = constants
        self.repository_manager = repository_manager
        self.error_manager = error_manager
        self.user_input_manager = user_input_manager

    def executeCommand(self, arguments, flags):
        command = arguments[0] if arguments else "help"
        subcommand = None
        arguments = None
        arguments_length = len(arguments)

        if arguments_length > 1:
            subcommand = arguments[1]
        if arguments_length > 2:
            arguments = list(set(arguments) - {command, subcommand})
        
        if command == "status":
            self.printStatus()

        elif command == "update":
            token = self.user_input_manager.getAccessToken()
            self.updateStatus(token)

        elif command == "help":
            self.printHelp()

        elif command == "auto-delete-head":
            token = self.user_input_manager.getAccessToken()
            self.setAutoDeleteHeadStatus(token, subcommand, arguments)

        else:
            self.error_manager.printErrorAndExit("Invalid command. To check the list of available commands, run 'help'")

    def printStatus(self):
        repositories = self.repository_manager.readRepositories()

        if repositories is None:
            token = self.user_input_manager.getAccessToken()
            self.updateStatus(token)
            repositories = self.repository_manager.readRepositories()

        self.repository_manager.printAutoDeleteHeadStatus(repositories)

    def updateStatus(self, token):
        repository_ids = self.repository_manager.getRepositoriesIDs(token)
        repositories = self.repository_manager.fetchRepositories(token, repository_ids)
        self.repository_manager.saveRepositories(repositories)
        print("-- Repositories' status updated successfully --")

    def setAutoDeleteHeadStatus(self, token, subcommand, repository_names = None):
        if not subcommand:
            self.error_manager.printErrorAndExit(self.error_manager.subcommand_not_passed_error)

        auto_delete_head_bool = None
        
        if subcommand == "enable":
            auto_delete_head_bool = True
        elif subcommand == "disable":
            auto_delete_head_bool = False
        
        if auto_delete_head_bool == None:
            self.error_manager.printErrorAndExit(self.error_manager.invalid_subcommand_error)

        repository_ids = self.repository_manager.getRepositoriesIDs(token, repository_names)
        self.repository_manager.setAutoDeleteHeadStatus(token, auto_delete_head_bool, repository_ids)
        
        print("-- Repositories' status altered successfully --")  
        self.updateStatus(token)

    def printHelp(self):
        try:
            with open(self.constants.HELP_FILE_PATH, "r") as help_file:
                print(help_file.read())
        except:
            self.error_manager.printErrorAndExit("The Help file could not be found. Please make sure that the 'help.txt' file is located in the 'data' directory.")


