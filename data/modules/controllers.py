
class CommandController:
    def __init__(self, requests_manager, data_manager, error_manager, user_input_manager, parse_manager):
        self.requests_manager = requests_manager
        self.data_manager = data_manager
        self.error_manager = error_manager
        self.user_input_manager = user_input_manager
        self.parse_manager = parse_manager

    def executeCommand(self, arguments, flags):
        command = arguments[0] if arguments else "help"
        subcommand = None
        left_arguments = None
        arguments_length = len(arguments)

        if arguments_length > 1:
            subcommand = arguments[1]
        if arguments_length > 2:
            left_arguments = list(set(arguments) - {command, subcommand})
        
        if command == "status":
            self.printStatus()

        elif command == "update":
            token = self.user_input_manager.getAccessToken()
            self.updateStatus(token)

        elif command == "help":
            self.printHelp()

        elif command == "auto-delete-head":
            token = self.user_input_manager.getAccessToken()
            self.setAutoDeleteHeadStatus(token, subcommand, left_arguments)

        else:
            self.error_manager.printErrorAndExit("Invalid command. To check the list of available commands, run 'help'")

    def printStatus(self):
        repositories = self.data_manager.readRepositories()

        if repositories is None:
            token = self.user_input_manager.getAccessToken()
            self.updateStatus(token)
            repositories = self.data_manager.readRepositories()

        for repository in repositories:
            repository_name = repository.name
            repository_id = repository.id
            repository_auto_delete_head_bool = repository.auto_delete_head_bool
    
            if repository_auto_delete_head_bool:
                print(f"  > Head branches are automatically deleted in repository '{repository_name}' (ID: {repository_id}).")
            elif not repository_auto_delete_head_bool:
                print(f"  > Head branches are NOT automatically deleted in repository '{repository_name}' (ID: {repository_id}).")
            else:
                self.error_manager.printErrorAndExit(f"The boolean 'delete_branch_on_merge' could not be found in repository '{repository_name}' (ID: {repository_id}).")

    def updateStatus(self, token):
        repository_ids = self.requests_manager.getRepositoriesIDs(token)
        repositories = self.requests_manager.fetchRepositories(token, repository_ids)
        self.data_manager.saveRepositories(repositories)
        print("-- Repositories' status updated successfully --")

    def setAutoDeleteHeadStatus(self, token, subcommand, repository_names = None):
        if not subcommand:
            self.error_manager.printErrorAndExit(self.error_manager.SUBCOMMAND_NOT_PASSED_ERROR)

        auto_delete_head_bool = None
        
        if subcommand == "enable":
            auto_delete_head_bool = True
        elif subcommand == "disable":
            auto_delete_head_bool = False
        
        if auto_delete_head_bool == None:
            self.error_manager.printErrorAndExit(self.error_manager.INVALID_SUBCOMMAND_ERROR)

        repository_ids = self.requests_manager.getRepositoriesIDs(token, repository_names)

        body_dict = {"delete_branch_on_merge": auto_delete_head_bool}
        json_body_string = self.parse_manager.dictToJsonString(body_dict)
        
        for repository_id in repository_ids:
            response = self.requests_manager.makeRequest("patch", f"/repositories/{repository_id}", token, json_body_string) # requests.patch(f"{self.constants.API_URL}/repositories/{repository_id}", json_body_string, auth=(None, token))
        
        print("-- Repositories' status altered successfully --")  
        self.updateStatus(token)

    def printHelp(self):
        try:
            self.data_manager.readHelpFile()
        except:
            self.error_manager.printErrorAndExit("The Help file could not be found. Please make sure that the 'help.txt' file is located in the 'data' directory.")


