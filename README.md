# Parcut

**Pacman Repo Cleanup Tool**

A script to clean up pacman repos. This is primarily used for removing old versions of packages and adding new ones, but it has options to print old and new packages line-by-line so they can be parsed by other programs.

## Usage

First off, this depends on `natsort` and `click`, which you can install with `pip`.

```text
list-new-packages
├── --list-debug
└── repo_path*
list-old-packages
├── --list-debug
└── repo_path*
run
├── --dry-run
├── --only-delete
└── repo_path*

* = required
```

### `list-new-packages`

List the newest version of all packages.

- `--list-debug`: List debug symbol packages (default: true)

### `list-old-packages`

Lists old versions of packages.

- `--list-debug`: List debug symbol packages (default: true)

### `run`

Processes it all, runs `repo-remove` and deletes old packages, then runs `repo-add` on new packages.

Arguments:

- `--dry-run`: Do a dry run
- `--only-delete`: Only delete files, don't modify the repo files from them (default: false)
  - Without this argument, parcut will try to remove and add the relevant packages using `repo-add` and `repo-remove`, meaning it optionally depends on those programs.
    - <small>As long as you're on Arch, this will be installed, as it's part of pacman. Plus, if you're running a repo, you need these anyways.</small>

## Exit codes

- `0`: Completed successfully
- `10`: Failed to remove old package from repo - probably missing write perms on the database.
- `11`: Permission denied when trying to delete a package - missing write perms on the package.
- `12`: Failed to add new package to repo - again, probably missing write perms on the database.

## Notes and credits

This was inspired by [guydunigo/remove_old_arch_pkgs](https://github.com/guydunigo/remove_old_arch_pkgs), which I used at first, but ran into some bugs with.

I also ~~stole~~ borrowed and modified a bit of code from [blend-os/blend](https://github.com/blend-os/blend) for coloring the terminal.

## Notes and limitations

This requires a repo db file to already exist; if the repo doesn't already exist, you can just create an empty file like this instead: `touch reponame.db`

### Development

This uses `unittest` for testing; tests can be run by running `python3 -m unittest`. Running `test.py` normally will generate data to test the program, which is also generated automatically at the start of every test.
