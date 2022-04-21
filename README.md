# git-relevant-history

Extract software component from git repo into a new repo, taking complete relevant history with it.

## Background

When software evolves, it is typical for a stable, established software component to be moved out of a git repository to facilitate more comprehensive reuse. One of the pain points of such a move would be losing git history, breaking the possibility of using `git blame` or `git log` to understand what led to the current design.

Historically git filter-branch was used for such extracting, and https://github.com/newren/git-filter-repo is a much faster alternative recommended by git now. Both tools work on a static list of path patterns to preserve, so file renames in the past are usually "cut point."

This tool also starts with "what is subcomponent in the current repo to extract?" but then analyzes the history of renames for any existing file. Such a list is used to create a list of patterns for `git filter-repo` so that effectively the old repo/component becomes standalone repo with a full history of every file, as long as git --follow catches the rename.

So from the extracted component perspective, the only history "lost" is one that would require manual analysis of commits to find file merging/splitting.


## Help
Usage documentation for the tool is available via cmdline:

git-relevant-history --help:

```
Extract enough git history to facilitate git blame and have each line correctly annotated

Wipe all history that has no connection to the current state of the repository.

The resulting repository is a drop-in replacement for the old directory and has all history needed for typical git history use.

Usage:
  git-relevant-history [options] --source=<source_repo> --subdir=<subdir> --target=<target_repo>

Where git repo at <source_repo> would be processed into <target_repo>, in a way that only files starting with
<subdir> would be preserved.


Options:
  --only-specs         Only print git filter-repo specs file as expected by git filter-repo --paths-from-file
  -h --help            show this help message and exit
  -f --force           remove <target_repo> if exists
  -v --verbose         print status messages
  ```
  Calling when that repo is cloned:
  
  ./gitrelevanthistory/main.py --source=<big-repo> --subdir=<subdir-of-big-repo> --target=<path-of-extracted-small-repo>
