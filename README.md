# gitea_api_connection

Gitea - API connection set of scripts
- I use Gitea as my home GIT service
- Theese scripts make the way to work with gitea from commnad line easier

command_create_repository.py
- connect with Gitea settings in gitea_url_params.py
- using tokens in tokens.py (default TOKENS[1])
- I use then 'git_newrepo' shell command somewhere in 'PATH' (from its template) to call python 
script from any working directory  