import data.modules.utils.repository_utils as repository_utils
import data.modules.utils.auth_utils as auth_utils
import data.modules.utils.usr_input_utils as usr_input_utils
import data.modules.configs.default_configs as default_configs
import requests
import json


def printStatus():
    repositories = repository_utils.readRepositories()

    if repositories != None:
        repository_utils.printRepositoriesStatus(repositories)
    
    else:
        token = usr_input_utils.getAccessToken()

        updateStatus(token)
        repositories = repository_utils.readRepositories()
        repository_utils.printRepositoriesStatus(repositories)

def updateStatus(token):
    repository_ids = repository_utils.getRepositoriesIDs(token)
    repositories = repository_utils.getRepositories(token, repository_ids)
    repository_utils.saveRepositories(repositories)

    print("-- Repositories' status updated --")

def alterStatus(token, auto_delete_bool, repository_names = None):
    
    repository_ids = repository_utils.getRepositoriesIDs(token, repository_names = repository_names)

    for repository_id in repository_ids:
        json_body_dict = {"delete_branch_on_merge": auto_delete_bool}
        json_body_string = json.dumps(json_body_dict)

        response = requests.patch(f"{default_configs.api_url}/repositories/{repository_id}", json_body_string, auth=(None, token))
        auth_utils.checkStatusCode(response.status_code)
    
    print("-- Repositories' status altered --")    

def printHelp():

    try:
        with open(default_configs.help_file_path, "r") as help_file:
            help_content = help_file.read()
            print(help_content)
    except:
        print("Something has went wrong.\nError: The Help file could not be found. Please make sure that the 'help.txt' file is located in the 'data' directory.")
