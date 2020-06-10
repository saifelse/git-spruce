import keyring

from .git import get_git_handle
from github import Github


def get_github_api_token(username):
	return keyring.get_password("im.h4k.git-spruce", username)


def store_github_api_token(username, password):
	keyring.set_password("im.h4k.git-spruce", username, password)


def get_prs_for_branch():
	token = get_github_api_token(get_git_handle())
	g = Github(token)
	return g
