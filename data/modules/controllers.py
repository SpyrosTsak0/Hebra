
class CommandController:
    def __init__(self, base_classes, requests_manager, data_manager, error_manager, user_input_manager, parse_manager):
        self.base_classes = base_classes
        self.requests_manager = requests_manager
        self.data_manager = data_manager
        self.error_manager = error_manager
        self.user_input_manager = user_input_manager
        self.parse_manager = parse_manager

        self.updateStatus = self.error_manager.handleRequestExceptions(self.updateStatus)
        self.setAutoDeleteHeadStatus = self.error_manager.handleRequestExceptions(self.setAutoDeleteHeadStatus)

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

        elif command == "auto-delete-head":
            token = self.user_input_manager.getAccessToken()
            self.setAutoDeleteHeadStatus(token, subcommand, left_arguments)
        
        elif command == "help":
            self.printHelp()

        else:
            self.error_manager.printErrorAndExit("Invalid command. To check the list of available commands, run 'help'")

    def printStatus(self):
        repositories_list = self.data_manager.readRepositories()
        if repositories_list is None:
            token = self.user_input_manager.getAccessToken()
            self.updateStatus(token)
            repositories_list = self.data_manager.readRepositories()

        def print_nested(key, value, indent = 2):
            prefix = "  " * indent

            if isinstance(value, dict):  
                print(f"{prefix}> {key}:")
                for sub_key, sub_value in value.items():
                    print_nested(sub_key, sub_value, indent + 2)
            else:
                print(f"{prefix}> {key}: {value}")

        for repository_dict in repositories_list:
            print(f"-- For repository '{repository_dict.get('name')}' (ID: {str(repository_dict.get('id'))}) --")
        
            for key, value in repository_dict.items():
                if key == "protection_rules" or key == 'id' or key == 'name':
                    continue
                print_nested(key, value) 

            print("\n")

    def updateStatus(self, token):
        repository_ids = self.requests_manager.fetchRepositoriesIDs(token)
        
        repositories = list()

        for repository_id in repository_ids:
            main_response = self.requests_manager.makeRequest("get", f"/repositories/{repository_id}", token) 
            main_response.raise_for_status()

            main_repository_info = main_response.json()
            username = main_repository_info.get("owner").get("login")
            repository_name = main_repository_info.get("name")

            protection_response = self.requests_manager.makeRequest("get", f"/repos/{username}/{repository_name}/branches/main/protection", token) 

            repository = self.base_classes.Repository(
            repository_name, 
            main_repository_info.get("id"), 
            main_repository_info.get("delete_branch_on_merge"),
            protection_response.json() if str(protection_response.status_code).startswith("2") else None)
            
            repositories.append(repository)
            
        self.data_manager.saveRepositories(repositories)
        print("\n-- Repositories' status updated successfully --\n")

    def setAutoDeleteHeadStatus(self, token, subcommand, repository_names = None):
        if not subcommand:
            self.error_manager.printErrorAndExit(self.error_manager.SUBCOMMAND_NOT_PASSED_ERROR)

        auto_delete_head = None
        
        if subcommand == "enable":
            auto_delete_head = True
        elif subcommand == "disable":
            auto_delete_head = False
        
        if auto_delete_head == None:
            self.error_manager.printErrorAndExit(self.error_manager.INVALID_SUBCOMMAND_ERROR)

        repository_ids = self.requests_manager.fetchRepositoriesIDs(token, repository_names)

        body_dict = {"delete_branch_on_merge": auto_delete_head}
        json_body_string = self.parse_manager.dictToJsonString(body_dict)

        for repository_id in repository_ids:
            response = self.requests_manager.makeRequest("patch", f"/repositories/{repository_id}", token, json_body_string)
        
        print("-- Repositories' status altered successfully --")  
        self.updateStatus(token)

    def printHelp(self):
        try:
            print(self.data_manager.readHelpFile())
        except:
            self.error_manager.printErrorAndExit("The Help file could not be found. Please make sure that the 'help.txt' file is located in the 'data' directory.")


