# git-relevant-history

Extract software component from git repo into anew repo, taking complete relevant history with it.

## Background

When software evolves its common for stable, established software component to be moved out of a git repository to facilitate wider reuse. One of the pain points of such move would be loosing git history, breaking possibility to use `git blame` or `git log` to uderstand what lead to current design.

Historically git filter-branch was used for such extracting, and https://github.com/newren/git-filter-repo is much faster alternative recomended by git now. Both tools work on static list of path patterns to preserve, so file renames in the past are usually "cut point"

This tool also starts with "what is subcomponent in current repo to extract?", but then it analyzes history of renames for any existing file, and creates a list of patterns for `git filter-repo` so that effectively the oldrepo/component becomes standalone repo with full history of every file, as long as git --follow catches the rename.

So from extracted component perspective the only history "lost" is the one that would require manual analysis of commits to find file merging / splitting.


## Help
For the tools is available via cmdline:

git-relevant-history --help :

```
Extract enough git history to facilitate git blame and have each line correctly annotated

Wipe all history that has no connection to current state of repository.

Resulting repository is drop in replacement for the old dir, and has all history needed for
typical git history use.

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
  
