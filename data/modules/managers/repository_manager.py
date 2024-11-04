import requests
import json
import os

class RepositoryManager:
    def __init__(self, base_classes, constants):
        self.repository_class = base_classes.get("Repository")
        self.constants = constants

    def printAutoDeleteHeadStatus(self, repositories):
        for repository in repositories:
            repository_name = repository.name
            repository_id = repository.id
            repository_auto_delete_head_bool = repository.auto_delete_head_bool
    
            if repository_auto_delete_head_bool:
                print(f"  > Head branches are automatically deleted in repository '{repository_name}' (ID: {repository_id}).")
            elif not repository_auto_delete_head_bool:
                print(f"  > Head branches are NOT automatically deleted in repository '{repository_name}' (ID: {repository_id}).")
            else:
                print(f"The boolean 'delete_branch_on_merge' could not be found in repository '{repository_name}' (ID: {repository_id}).")
                sys.exit(1)
    
    def setAutoDeleteHeadStatus(self, token, auto_delete_head_bool, repository_ids):
        for repository_id in repository_ids:
            body_dict = {"delete_branch_on_merge": auto_delete_head_bool}
            json_body_string = json.dumps(body_dict)

            response = requests.patch(f"{self.constants.API_URL}/repositories/{repository_id}", json_body_string, auth=(None, token))

    def fetchRepositories(self, token, repository_ids):
        repositories = list()

        for repository_id in repository_ids:
            main_response = requests.get(f"{self.constants.API_URL}/repositories/{repository_id}", auth=(None, token))
            main_response.raise_for_status()

            main_repository_info = main_response.json()
            username = main_repository_info.get("owner").get("login")
            repository_name = main_repository_info.get("name")

            protection_response = requests.get(f"{self.constants.API_URL}/repos/{username}/{repository_name}/branches/main/protection", auth=(None, token))

            repository = self.repository_class(
            repository_name, 
            main_repository_info.get("id"), 
            main_repository_info.get("delete_branch_on_merge"),
            protection_response.json() if str(protection_response.status_code).startswith("2") else None)

            repositories.append(repository)
    
        return repositories 

    def getRepositoriesIDs(self, token, repository_names = None):
        repository_ids = list()

        response = requests.get(f"{self.constants.API_URL}/user/repos", auth=(None, token))
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

    def saveRepositories(self, repositories):
        with open(self.constants.REPOSITORIES_JSON_FILE_PATH, "w") as repositories_datafile:
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
        if os.path.isfile(self.constants.REPOSITORIES_JSON_FILE_PATH):
            repositories = list()

            try:
                with open(self.constants.REPOSITORIES_JSON_FILE_PATH, "r") as repositories_datafile:
                    repository_jsonstring = repositories_datafile.read()
                    repositories_list = json.loads(repository_jsonstring)
                
                    for repository_dict in repositories_list:
                        repository = self.repository_class(
                        repository_dict.get("name"), 
                        repository_dict.get("id"),
                        repository_dict.get("auto_delete_head_bool"),
                        repository_dict.get("protection_rule"))
                        
                        repositories.append(repository)
                
                    return repositories
            except:
                return None

                