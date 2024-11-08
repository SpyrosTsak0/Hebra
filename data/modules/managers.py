from data.modules.base_classes import Repository
import sys, requests, json, os

class ErrorManager:

    SUBCOMMAND_NOT_PASSED_ERROR = "A subcommand has not been passed. To check the list of available subcommands for the command entered, run 'help'."
    INVALID_SUBCOMMAND_ERROR = "Invalid subcommand. To check the list of available subcommands for the command entered, run 'help'."

    def printErrorAndExit(self, error_text):
        print(f"Something has went wrong. Error: {error_text}")
        sys.exit(1)

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

    def fetchRepositories(self, token, repository_ids):
        repositories = list()

        for repository_id in repository_ids:
            main_response = self.makeRequest("get", f"/repositories/{repository_id}", token) # requests.get(f"{self.API_URL}/repositories/{repository_id}", auth=(None, token))
            main_response.raise_for_status()

            main_repository_info = main_response.json()
            username = main_repository_info.get("owner").get("login")
            repository_name = main_repository_info.get("name")

            protection_response = self.makeRequest("get", f"/repos/{username}/{repository_name}/branches/main/protection", token) #requests.get(f"{self.API_URL}/repos/{username}/{repository_name}/branches/main/protection", auth=(None, token))

            repository = Repository(
            repository_name, 
            main_repository_info.get("id"), 
            main_repository_info.get("delete_branch_on_merge"),
            protection_response.json() if str(protection_response.status_code).startswith("2") else None)

            repositories.append(repository)
    
        return repositories 

    def getRepositoriesIDs(self, token, repository_names = None):
        repository_ids = list()

        response = self.makeRequest("get", "/user/repos", token) # requests.get(f"{self.API_URL}/user/repos", auth=(None, token))
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

    def saveRepositories(self, repositories):
        with open(self.REPOSITORIES_JSON_FILE_PATH, "w") as repositories_datafile:
            repositories_datafile.write("[")
            repositories_length = len(repositories)

            for repository_count in range(repositories_length):
                repository = repositories[repository_count]
                repository_dict = repository.__dict__
                repository_jsonstring = json.dumps(repository_dict)

                repositories_datafile.write(repository_jsonstring)

                if repository_count + 1 < repositories_length:
                    repositories_datafile.write(",")
        
            repositories_datafile.write("]")

    def readRepositories(self):
        if os.path.isfile(self.REPOSITORIES_JSON_FILE_PATH):
            repositories = list()

            try:
                with open(self.REPOSITORIES_JSON_FILE_PATH, "r") as repositories_datafile:
                    repository_jsonstring = repositories_datafile.read()
                    repositories_list = json.loads(repository_jsonstring)
                
                    for repository_dict in repositories_list:
                        repository = Repository(
                        repository_dict.get("name"), 
                        repository_dict.get("id"),
                        repository_dict.get("auto_delete_head_bool"),
                        repository_dict.get("protection_rule"))
                        
                        repositories.append(repository)
                
                    return repositories
            except:
                return None
    
    def readHelpFile(self):
        with open(self.HELP_FILE_PATH, "r") as help_file:
            print(help_file.read())
        
class ParseManager:
    def dictToJsonString(self, dictionary):
        return json.dumps(dictionary)
    
    def jsonStringToDict(self, json_string):
        return json.loads(json_string)
                