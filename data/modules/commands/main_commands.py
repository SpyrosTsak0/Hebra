from data.modules.utils.repository_utils import *
from data.modules.utils.auth_utils import getAccessToken
from data.modules.configs.default_configs import api_url
import requests

def printStatus():
    repositories = readRepositories()

    if repositories != None:
        printRepositoriesStatus(repositories)
    
    else:
        token = getAccessToken()

        updateStatus(token)
        repositories = readRepositories()
        printRepositoriesStatus(repositories)

def updateStatus(token):
    repository_ids = getRepositoriesIDs(token)
    repositories = getRepositories(token, repository_ids)
    saveRepositories(repositories)

    print("-- Repositories' status updated --")

def alterStatus(token, auto_delete_bool, repository_names = None):
    
    repository_ids = getRepositoriesIDs(token, repository_names = repository_names)

    for repository_id in repository_ids:
        json_body_dict = {"delete_branch_on_merge": auto_delete_bool}
        json_body_string = json.dumps(json_body_dict)

        response = requests.patch(f"{api_url}/repositories/{repository_id}", json_body_string, auth=(None, token))
        checkStatusCode(response.status_code)
    
    print("-- Repositories' status altered --")
    updateStatus(token)    


def printInvalidCommand():
    print("Invaild command. To check the list of available commands, run '--help'")
    sys.exit(1)

def printHelp():

    try:
        with open("data/help.txt", "r") as help_file:
            help_content = help_file.read()
            print(help_content)
    except:
        print("Something has went wrong.\nError: The Help file could not be found. Please make sure that the 'help.txt' file is located in the 'data' directory.")
