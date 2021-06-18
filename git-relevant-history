#!/usr/bin/env python3

"""
Extract enough git history to facilitate git blame and have each line correctly annotated

Wipe all history that has no connection to the current state of the repository.

The resulting repository is a drop-in replacement for the old directory and has all history needed for typical git history use.

Usage:
  git-relevant-history [options] --source=<source_repo> --subdir=<subdir> --target=<target_repo>

Where git repo at <source_repo> would be processed into <target_repo>, in a way that only files starting with
<subdir> would be preserved (<subdir> is relative to <source_repo>).


Options:
  --only-specs         Only print git filter-repo specs file as expected by git filter-repo --paths-from-file
  -h --help            show this help message and exit
  -f --force           remove <target_repo> if exists
  -v --verbose         print status messages

"""
import glob
import logging
import os
import pathlib
import shutil
import subprocess
import tempfile
import typing

from docopt import docopt

log_format = "%(message)s"
logging.basicConfig(format=log_format, level=logging.DEBUG)

logger = logging.root


def remove_prefix_if_present(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def build_git_filter_path_spec(git_repo: pathlib.Path, str_subdir: str) -> typing.List[str]:
    git_repo_subdir = git_repo / str_subdir
    logger.debug(f"Processing files in {git_repo_subdir}")
    all_filter_paths = []
    all_rename_statements = []

    for strpath in git_repo_subdir.rglob('*'):
        path = pathlib.Path(strpath)

        if path.is_file():
            repo_path = path.relative_to(git_repo)
            all_rename_statements.append(f"{repo_path}==>{remove_prefix_if_present(str(repo_path), str_subdir)}")

            logger.debug(f"Including {repo_path} with history")

            unique_paths_of_current_file = {str(repo_path)}

            git_args = ["git",
                        "-C",
                        str(git_repo),
                        "log",
                        '--pretty=format:',
                        "--name-only",
                        "--follow",
                        "--",
                        str(repo_path)]
            try:
                gitlog = subprocess.check_output(git_args,
                                                 universal_newlines=True)

                for line in gitlog.splitlines(keepends=False):
                    if len(line) > 0:
                        unique_paths_of_current_file.add(line.strip())

                if logger.isEnabledFor(logging.DEBUG):
                    this_file_paths_newlines = '\n\t'.join(unique_paths_of_current_file)
                    logger.debug(f"\t{this_file_paths_newlines}\n")

                all_filter_paths.extend(unique_paths_of_current_file)

            except subprocess.CalledProcessError as e:
                logger.warning(f"Failed to get hystorical names of {repo_path}, stdout: {e.output}, stderr: {e.stderr}")
                logger.warning(f"Failed command: {' '.join(git_args)}")

    if logger.isEnabledFor(logging.DEBUG):
        all_rename_statements_newlines = '\n\t'.join(all_rename_statements)
        logger.debug(f"All renames:\n\t{all_rename_statements_newlines}")
    return all_filter_paths + all_rename_statements


def main():
    source_repo = pathlib.Path(arguments['--source']).expanduser().absolute()
    if not source_repo.is_dir():
        logger.critical(f"--source {source_repo} is not a directory")
        raise SystemExit(-1)

    if not (source_repo / '.git').is_dir():
        logger.critical(f"--source {source_repo} is missing .git subdir - it need to be root of existing git repo.")
        raise SystemExit(-1)

    subdir = arguments['--subdir']
    if not subdir.endswith('/'):
        subdir = subdir + '/'

    source_subdir = source_repo / subdir
    if not source_repo.is_dir():
        logger.critical(f"--source {source_repo / subdir} is not a directory")
        raise SystemExit(-1)

    target_repo = pathlib.Path(arguments['--target']).expanduser().absolute()
    if target_repo.exists() and not arguments['--only-specs']:
        if arguments['--force']:
            logger.info(f"Will remove existing target repo at {target_repo} to store result.")
        else:
            logger.critical(f"Target directory {target_repo} already exists. Use --force to override")
            raise SystemExit(-1)

    logger.info(f"Will convert repo at {source_repo / subdir} into {target_repo} preserving file history")

    with tempfile.TemporaryDirectory() as str_workdir:
        workdir = pathlib.Path(str_workdir)

        workclone = workdir / 'repo'
        logger.debug(f"All work would happen in fresh clone (under {workclone},"
                     " that is requirement from git-filter branch"
                     " and also protects current repo state and history.")

        workclone_cmd = ['git', 'clone',
                         '--branch', 'master',
                         '--single-branch',
                         'file://' + str(source_repo),
                         str(workclone)]
        logger.debug(f"Calling {' '.join(workclone_cmd)}")
        subprocess.check_call(workclone_cmd)

        filenameset = build_git_filter_path_spec(workclone, subdir)
        filter_repo_paths_file = workdir / "filter_path_specs.txt"
        with open(filter_repo_paths_file, "w") as outfile:
            for line in filenameset:
                outfile.write(line)
                outfile.write('\n')

        logger.debug(f"Stored filter repo specs in {filter_repo_paths_file}")

        if arguments['--only-specs']:
            logger.debug(f"Dumping contents of {filter_repo_paths_file}")
            print(filter_repo_paths_file.read_text())
            return

        filter_args = ["git",
                       "-C",
                       str(workclone),
                       "filter-repo",
                       "--paths-from-file",
                       str(filter_repo_paths_file)
                       ]
        logger.debug(f"Calling {' '.join(filter_args)}")
        subprocess.check_call(filter_args,
                              universal_newlines=True)

        logger.debug(f"Moving final result from {workclone} to {target_repo}")
        if target_repo.exists():
            shutil.rmtree(target_repo)
            shutil.move(workclone, target_repo)
            logger.info(f"Replaced {target_repo} with filtering result")
        else:
            shutil.move(workclone, target_repo)
            logger.info(f"Stored filtering result at {target_repo}")


if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['--verbose']:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    main()
