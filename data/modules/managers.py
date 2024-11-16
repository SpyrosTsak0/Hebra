import sys, requests, json, os

class CommunicationManager:

    def printText(self, text = None):
        if text != None:
            print("\033[96m {}\033[00m".format(text))
        else:
            print()
    
    def printErrorAndExit(self, error_message):
        print("\033[91m {}\033[00m".format(error_message))
        sys.exit(1)
    
    def printAndGetInput(self, input_message):
        return input("\033[93m {}\033[00m".format(input_message))
    
    def fetchArguments(self):
        arguments = self.__getArguments()

        for argument in arguments:
            if argument.startswith("--"):
                arguments.remove(argument)
    
        return arguments

    def fetchFlags(self):
        arguments = self.__getArguments()
        flags = list()

        for argument in arguments:
            if argument.startswith("--"):
                flags.append(argument)
        
        return flags

    #-------------------------------

    def printSubcommandNotPassedAndExit(self):
        self.printErrorAndExit("A subcommand has not been passed. To check the list of available subcommands for the command entered, run 'help'.")
    
    def printInvalidSubcommandAndExit(self):
        self.printErrorAndExit("Invalid subcommand. To check the list of available subcommands for the command entered, run 'help'.")
    
    def printAndGetAccessToken(self):
        return self.printAndGetInput("Enter your GitHub access token: ")
    
    
    def handleRequestErrors(self, func):
        def wrapper(*args, **kwargs): 
            try:
                return func(*args, **kwargs)
            except requests.exceptions.ConnectionError:
                self.printErrorAndExit("There was a problem establishing a connection with the GitHub API. This may happen due to a network or server-side issue.}")
            except requests.exceptions.HTTPError as http_error:
                self.printErrorAndExit(f"HTTP request was not successful - {http_error}")
        
        return wrapper 

    #-------------------------------
    #-------------------------------

    def __getArguments(self):
        arguments = list(sys.argv)
        filename_string = arguments[0]
        arguments.remove(filename_string)
        return arguments

class RequestsManager:
    
    def makeRequest(self, method, path, token = None, body = None):
        api_url = "https://api.github.com"
        
        full_path = api_url + path
        _auth = (None, token)

        if method == 'get':
            return requests.get(full_path, auth = _auth)
        if method == 'patch':
            return requests.patch(full_path, body, auth = _auth)
    
    #-------------------------------

    def fetchRepositoryIDs(self, token, repository_names = None):
        repository_ids = list()

        response = self.makeRequest("get", "/user/repos", token)
        response.raise_for_status()
        repositories_info = response.json()

        if type(repositories_info) == dict:
            repositories_info = list().append(repositories_info)
    
        if repository_names == None:
            for repository_info in repositories_info:
                repository_id = repository_info.get("id")
                repository_ids.append(repository_id)
        else:
            for repository_info in repositories_info:
                _repository_name = repository_info.get("name")
            
                for repository_name in repository_names:
                     if repository_name == _repository_name:
                        repository_id = repository_info.get("id")
                        repository_ids.append(repository_id)

        return repository_ids 

class DataManager:

    paths = {
        "repository_data_file": "data/repository_data.json",
        "help_file": "data/help.txt"
    }

    def readFile(self, file_path):
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                return file.read()
    
    def writeFile(self, file_path, string):
        with open(file_path, "w") as file:
            file.write(string)
    
    #-------------------------------

    def writeJsonFile(self, json_file_path, dict_list):
        json_string = str()
        json_string += "["

        for dictionary in dict_list:
            json_string += json.dumps(dictionary)

            if dict_list.index(dictionary) + 1 < len(dict_list):
                json_string += ","
        
        json_string += "]"
        self.writeFile(json_file_path, json_string)

    def readJsonFile(self, json_file_path):
        json_string = self.readFile(json_file_path)
       
        if json_string  != None:
            try:
                return json.loads(json_string)
            except:
                return None
            
class ParseManager:

    def dictToJsonString(self, dictionary):
        return json.dumps(dictionary)

    def jsonStringToDict(self, json_string):
        return json.loads(json_string)
                