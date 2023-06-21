"""
utils.py

Several python utils used with Gitea scripts. It serves as module library file
"""
import os


def gitea_true_false_string(value):
    """
    Returns text string true/false according boolean result of value

    Gitea vyzaduje True/False parametry v datech malymi pismeny

    :param value: Any value - will be boolean avaluated
    :return:
    """
    if value:
        return "true"
    else:
        return "false"


def create_gitea_url(protocol, host, port, base_api, user_api):
    """
    Create URL string used by requests defined by parameters

    :param protocol:
    :param host:
    :param port:
    :param base_api:
    :param user_api:
    :return:
    """
    if port:
        url_string = "{0}://{1}:{2}{3}{4}".format(
            protocol,
            host,
            port,
            base_api,
            user_api
        )
    else:
        url_string = "{0}://{1}{2}{3}".format(
            protocol,
            host,
            base_api,
            user_api
        )
    return url_string


def true_false_answer(value):
    """
    Decide if True or False kind of answer was written...

    :param value:
    :return:    True if ['Y', 'y', 'A', 'a', 't', 'T', 'yes', 'True', 'true', 'ano', 'Ano'],
                False if other choice
    """
    if str(value) in ['Y', 'y', 'A', 'a', 't', 'T', 'yes', 'True', 'true', 'ano', 'Ano']:
        return True
    else:
        return False


def set_user_defined_parameters(actual_parameteres, true_false_params=[]):
    """
    User can change most of the parameteres from shell script by questions/answers

    :param actual_parameteres:  existing parameters - some defined defaults
                                {'par1': value, ...}
    :param true_false_params:   list of parameter names which expects to result boolean True/False
    :return:
    """
    new_definition = {}
    # Go through each parameter to change it or leav defaults
    for each in actual_parameteres.keys():
        params = input("Change parameter {0} (enter to default: {1}):"
                       "".format(each, actual_parameteres[each])) or actual_parameteres[each]
        if each not in true_false_params:
            new_definition[each] = params
        else:
            new_definition[each] = true_false_answer(params)
    return new_definition


def create_clone_new_repo_script(clone_url, token, name):
    """
    Create bash script to initialize new created repository inside current working directory

        git clone http://token@10.1.222.222:3000/pvlcek/POKUS1.git
        mv POKUS1/ src/
        cd src
        git remote add lobogit http://"a48eafaaa5a2ac6c4a993b49a5f04ee385ab2b3d"@10.1.222.222:3000/pvlcek/POKUS1.git
        git pull lobogit master


    :param name:
    :param token:
    :type clone_url: object
    :return:
    """
    working_dir = os.getcwd()
    script_name = "init_new_repository.sh"
    command_list = []

    split_url = clone_url.split("//")
    if token:
        token_string = "{0}@".format(token)
    else:
        token_string = ""
    git_clone_command = "git clone {0}//{1}{2}".format(split_url[0], token_string, split_url[1])
    git_remote_command = "git remote add lobogit {0}//{1}{2}".format(split_url[0], token_string, split_url[1])
    rename_command = "mv {}/ src/".format(name)

    # create command list
    command_list.append("#!/bin/bash\n")
    command_list.append(git_clone_command+'\n')
    command_list.append(rename_command+'\n')
    command_list.append('cd src'+'\n')
    command_list.append(git_remote_command+'\n')
    command_list.append('git pull lobogit master'+'\n')

    f = open(working_dir+"/"+script_name, "w")
    f.writelines(command_list)
    f.close()
