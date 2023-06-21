"""
Pokusy s Gitea API

TODO: Anable selection of Gitea URL (default gitea_url_params.py used)  and user Token - default is TOKENS[1]
"""

import requests
import sys
import json

# Gitea parameters
from utils import gitea_true_false_string, create_gitea_url, set_user_defined_parameters, create_clone_new_repo_script
import gitea_url_params
from tokens import TOKENS
from create_repo_default_params import create_repo_default_params

token = TOKENS[2]

headers = {
    "Authorization": "token {}".format(token),
    "Content-Type": "application/json"
}


url = create_gitea_url(gitea_url_params.gitea_protocol,
                       gitea_url_params.gitea_host,
                       gitea_url_params.gitea_port,
                       gitea_url_params.gitea_base_api_url,
                       gitea_url_params.user_api_request_url)


if __name__ == "__main__":
    print(sys.argv)
    # New repository parameters - defalut / user defined
    new_repository_parameters = {}
    given_repo_name = ""
    user_config = False
    print_results = False
    repo_init_script = False

    # check command line parameters number >=2
    if len(sys.argv) < 2:
        print("\n************************************************************")
        print("********** ERROR - Creating new Gitea repository ***********")
        print("************************************************************")
        print("Not enough parameters...\nMinimum is one: 'repository_name' or keyword 'config'")
        sys.exit(1)

    if len(sys.argv) == 2 and sys.argv[1] == 'config':
        user_config = True
    else:
        given_repo_name = sys.argv[1]

    if len(sys.argv) > 2:
        if 'config' in sys.argv:
            user_config = True
        if 'results' in sys.argv:
            print_results = True
        if 'initscript' in sys.argv:
            repo_init_script = True

    # Given ropository name?
    new_repository_parameters = create_repo_default_params
    if given_repo_name:
        new_repository_parameters['name'] = given_repo_name

    print("\n****************************************************")
    print("********** Creating new Gitea repository ***********")
    print("****************************************************")

    # set repo configuration default or user input
    if user_config:
        print("\n---------- Changing repository parameters ----------")
        new_repository_parameters = set_user_defined_parameters(create_repo_default_params,
                                                                ['auto_init', 'private'])

    # print(new_repository_parameters)
    if not new_repository_parameters['name']:
        print("\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print("++++++++++ ERROR: name for new repository not set! ++++++++++")
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        sys.exit(2)
    else:
        print("\n========== Cretaing new repository name: {} ==========".format(new_repository_parameters['name']))
        r = requests.post(url, headers=headers, json=new_repository_parameters)

    # Create repo initialize script if demanded
    response_json_data = r.json()
    print(response_json_data)
    if repo_init_script:
        print("\n====================================================")
        print("========== Creating repository init script ==========")
        print("====================================================")
        create_clone_new_repo_script(response_json_data['clone_url'],
                                     token,
                                     response_json_data['name'])
        print("Created repository init script: ")

    # Demand to print results
    if print_results:
        print("\n=======================================================")
        print("========== Printing crete repository results ==========")
        print("=======================================================")
        print(json.dumps(response_json_data, indent=4, sort_keys=True))

    print("========== Repository created ==========")
