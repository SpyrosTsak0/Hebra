from data.modules.utils.auth_utils import *
from data.modules.configs.default_configs import api_url, repositories_json_file_path
import requests
import json
import os

class _repository:
    def __init__(self, name, id, auto_delete_bool):
        self.name = name
        self.id = id
        self.auto_delete_bool = auto_delete_bool


def printRepositoriesStatus(repositories):
    for repository in repositories:
        repository_name = repository.name
        repository_id = repository.id
        repository_auto_delete_bool = repository.auto_delete_bool
    
        if repository_auto_delete_bool:
            print(f" > Head branches are automatically deleted in repository '{repository_name}' (ID: {repository_id}).")
        elif not repository_auto_delete_bool:
            print(f" > Head branches are NOT automatically deleted in repository '{repository_name}' (ID: {repository_id}).")
        else:
            print(f"Something has went wrong.\nError: The boolean 'delete_branch_on_merge' could not be found in repository '{repository_name}' (ID: {repository_id}).\nThis could happen due to an invalid or expired access token when accesing a public repository.")
            sys.exit(1)
    
def getRepositories(token, repository_ids):
    repositories = list()

    for repository_id in repository_ids:
        response = requests.get(f"{api_url}/repositories/{repository_id}", auth=(None, token))
        checkStatusCode(response.status_code)

        repository_info = response.json()

        repository_name = repository_info.get("name")
        repository_id = repository_info.get("id")
        repository_auto_delete_bool = repository_info.get("delete_branch_on_merge")

        repository = _repository(repository_name, repository_id, repository_auto_delete_bool)
        repositories.append(repository)
    
    return repositories 

def getRepositoriesIDs(token, repository_names = None):
    repository_ids = list()

    response = requests.get(f"{api_url}/user/repos", auth=(None, token))
    checkStatusCode(response.status_code)

    repositories_info = response.json()

    if type(repositories_info) == dict:
        _list = list().append(repositories_info)
        repositories_info = _list
    
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

def saveRepositories(repositories):

    with open(repositories_json_file_path, "w") as repositories_datafile:
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

def readRepositories():

    if os.path.isfile(repositories_json_file_path):
        repositories = list()

        with open(repositories_json_file_path, "r") as repositories_datafile:
            try:
                repository_jsonstring = repositories_datafile.read()
                repositories_list = json.loads(repository_jsonstring)
                
                for repository_dict in repositories_list:
                    repository_name = repository_dict.get("name")
                    repository_id = repository_dict.get("id")
                    repository_auto_delete_bool = repository_dict.get("auto_delete_bool")

                    repository = _repository(repository_name, repository_id, repository_auto_delete_bool)
                    repositories.append(repository)
                
                return repositories
 
            except:
                return None