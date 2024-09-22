import os
import sys
import json
import requests


url = "https://api.github.com"
arguments = sys.argv
arguments.remove(arguments[0])
arguments_length = len(arguments)

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
    
def getRepositories(token, repository_ids):
    repositories = list()

    for repository_id in repository_ids:
        response = requests.get(f"{url}/repositories/{repository_id}", auth=(None, token))

        repository_info = response.json()

        repository_name = repository_info.get("name")
        repository_id = repository_info.get("id")
        repository_auto_delete_bool = repository_info.get("delete_branch_on_merge")

        repository = _repository(repository_name, repository_id, repository_auto_delete_bool)
        repositories.append(repository)
    
    return repositories 

def getRepositoriesIDs(token):
    repository_ids = list()

    response = requests.get(f"{url}/user/repos", auth=(None, token))
    repositories_info = response.json()

    if type(repositories_info) == dict:
        _list = list().append(repositories_info)
        repositories_info = _list

    for repository_info in repositories_info:
        repository_id = repository_info.get("id")
        repository_ids.append(repository_id)

    return repository_ids 

def saveRepositories(repositories):

    with open("repositories.json", "w") as repositories_datafile:
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

    if os.path.isfile("repositories.json"):
        repositories = list()

        with open("repositories.json", "r") as repositories_datafile:
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

def getAccessToken():
    token = input("Enter your access token: ")
    return token

def updateStatus():
    token = getAccessToken()

    repository_ids = getRepositoriesIDs(token)
    repositories = getRepositories(token, repository_ids)
    saveRepositories(repositories)

    print("-- Repositories' status updated --")

def printStatus():
    checkForToken()
    repositories = readRepositories()

    if repositories != None:
        printRepositoriesStatus(repositories)
    
    else:
        updateStatus()
        repositories = readRepositories()
        printRepositoriesStatus(repositories)
        

def printInvalidCommand():
    print("Invaild command. To check the list of available commands, run '--help'") 

def printHelp():
    print("--------------------\n\n\nHelp Page\n\n\n--------------------")


if len(arguments) > 0:
    match arguments[0]:
        case "status":
            
            if len(arguments) > 1:
                match arguments[1]:
                    case "--update" | "-u":
                        updateStatus()
                        printStatus()

                    case _:
                        printInvalidCommand()
            else:
                printStatus()
                    
        case "--help":
            printHelp()

        case _:
            printInvalidCommand()     
else:
    printHelp()       

