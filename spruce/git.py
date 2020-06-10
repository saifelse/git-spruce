import re
import subprocess
import sys


REBASE_HEAD_NAME_FPATH = ".git/rebase-merge/head-name"

REBASE_DONE_FPATH = ".git/rebase-merge/done"


def get_rebase_head_name():
    with open(REBASE_HEAD_NAME_FPATH, "r") as f:
        full_name = f.read()
    match = re.match(r"refs/heads/(.+/)", full_name)
    if not match:
        assert "Unexpected branch name", full_name
    return match.group(1)


def extract_prefix(branch):
    return branch.rsplit("/", 1)[0] + "/"


def get_branch_by_commit(prefix):
    info = subprocess.check_output(["git", "branch", "-v", "--list", u"{}*".format(prefix)])
    mapping = {}
    keylen = 0
    for line in info.splitlines():
        if line.startswith("*"):  # TODO: This is hacky.
            continue
        branch, short_commit, _ = line.strip().split(None, 2)
        keylen = len(short_commit)
        if not branch.endswith("/head"):
            mapping[short_commit] = branch
    return mapping, keylen


def iter_picked_commits():
    with open(REBASE_DONE_FPATH, "r") as f:
        for line in reversed(f.readlines()):
            action, rest = (line + " ").split(" ", 1)
            if action not in ("pick", "reword", "edit"):
                continue
            commit, _ = rest.split(" ", 1)
            yield commit


def find_branch_to_update():
    current_branch = get_rebase_head_name()
    prefix = extract_prefix(current_branch)
    branch_mapping, keylen = get_branch_by_commit(prefix)
    for commit in iter_picked_commits():
        short_commit = commit[:keylen]
        try:
            return branch_mapping[short_commit]
        except KeyError:
            continue
    return None


def get_branch_name():
    return subprocess.check_output(["git", "branch", "--show-current"]).strip()


def get_git_handle():
    return subprocess.check_output(["git", "config", "user.email"]).strip()
