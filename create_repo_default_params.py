"""
Gitea API POST request defalt parameters to create new repository

These parameters coresponding with Gitea new repository create form.

It is good practise to auto initiate repository with .gitignore and README file.

Gitignore file name specification is taken from Gitea create repository form .gitignore line names
"""

# Params to initiate repo
create_repo_default_params = {
    'auto_init': True,
    'description': "",
    'gitignores': "Python",
    'issue_labels': "",
    'licence': "",
    'name': "",
    'private': True,
    'readme': "Default",
}
