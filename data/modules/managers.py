import sys, requests, json, os

class ErrorManager:

    SUBCOMMAND_NOT_PASSED_ERROR = "A subcommand has not been passed. To check the list of available subcommands for the command entered, run 'help'."
    INVALID_SUBCOMMAND_ERROR = "Invalid subcommand. To check the list of available subcommands for the command entered, run 'help'."

    def printErrorAndExit(self, error_text):
        print(f"Something has went wrong. Error: {error_text}")
        sys.exit(1)

    def handleRequestExceptions(self, func):
        def wrapper(*args, **kwargs): 
            try:
                return func(*args, **kwargs)
            except requests.exceptions.ConnectionError as connection_error:
                self.printErrorAndExit("There was a problem establishing a connection with the GitHub API. This may happen due to a network or server-side issue.")
            except requests.exceptions.HTTPError as http_error:
                self.printErrorAndExit(f"HTTP request was not successful - {http_error}")
            except Exception as exception:
                self.printErrorAndExit(f"An unexpected error occurred - {exception}")
        
        return wrapper  
                
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

class RequestsManager:
    
    API_URL = "https://api.github.com"

    def makeRequest(self, method, path, token = None, body = None):
        full_path = self.API_URL + path
        _auth = (None, token)

        if method == 'get':
            return requests.get(full_path, auth = _auth)
        if method == 'patch':
            return requests.patch(full_path, body, auth = _auth)

    def fetchRepositoriesIDs(self, token, repository_names = None):
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

    REPOSITORIES_JSON_FILE_PATH = "data/repository_data.json"
    HELP_FILE_PATH = "data/help.txt"

    def readFile(self, path):
        if os.path.isfile(path):
            with open(path, "r") as file:
                return file.read()
    
    def writeFile(self, path, string):
        with open(path, "w") as file:
            file.write(string)

    def saveRepositories(self, repositories):
        repositories_jsonstring = str()
        repositories_jsonstring += "["

        for repository in repositories:
            repository_dict = repository.__dict__
            repositories_jsonstring += json.dumps(repository_dict)

            if repositories.index(repository) + 1 < len(repositories):
                repositories_jsonstring += ","
        
        repositories_jsonstring += "]"
        self.writeFile(self.REPOSITORIES_JSON_FILE_PATH, repositories_jsonstring)

    def readRepositories(self):
        repository_jsonstring = self.readFile(self.REPOSITORIES_JSON_FILE_PATH)
       
        if repository_jsonstring  != None:
            try:
                repositories_list = json.loads(repository_jsonstring)
            except:
                return None
                
            for repository_dict in repositories_list:
                repository_name = repository_dict.get("name")
                repository_id = repository_dict.get("id")

                if repository_name == None or repository_id == None:
                    return None
                    
            return repositories_list

    def readHelpFile(self):
        return self.readFile(self.HELP_FILE_PATH)
            
        
class ParseManager:

    def dictToJsonString(self, dictionary):
        return json.dumps(dictionary)

    def jsonStringToDict(self, json_string):
        return json.loads(json_string)
                