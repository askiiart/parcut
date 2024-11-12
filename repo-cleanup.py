#!/usr/bin/env python3
from natsort import natsorted
import click
import glob
from subprocess import getstatusoutput
from colors import colors
from os import remove


@click.group('cli')
def cli():
    """Clean up and manage Pacman repos"""


@cli.command('run')
@click.option('--dry-run', is_flag=True, default=False, help='Do a dry run')
@click.option(
    '--only-delete',
    is_flag=True,
    default=False,
    help="Only delete files, don't run repo-remove and repo-add on their old and new versions (default: false)"
)
@click.argument('repo_path')
def run(repo_path, dry_run=False, only_delete=False):
    if dry_run:
        print(
            f'{colors.bg.bright.blue}{colors.fg.black}Dry run mode enabled; no changes will be made{colors.reset}\n'
        )
    old_packages = get_old_packages(repo_path)
    repo_name = HelperFunctions.get_repo_name(repo_path)

    if not only_delete:
        print('=== Removing old packages ===')
        for pkg in old_packages:
            print(f'Removing {pkg}...')
            if not dry_run:
                output = getstatusoutput(
                    f'repo-remove {repo_path}/{repo_name}.db.tar.zst {repo_path}/{pkg}'
                )
                if output[0] != 0:
                    print(
                        f'{colors.bg.red}[ERROR]{colors.reset} failed to remove {pkg}'
                    )
                    print(f'Exit code: {output[0]}')
                    print(f'Command output:\n{output[1]}')
                    exit(10)

        print(
            f'{colors.fg.green}✅ Successfully removed old packages from repo{colors.reset}'
        )
        print()

    print('=== Deleting old packages ===')
    for pkg in old_packages:
        print(f'Deleting {pkg}...')
        if not dry_run:
            try:
                remove(f'{repo_path}/{pkg}')
            except Exception as e:
                print(f'{colors.bg.red}[ERROR]{colors.reset} failed to delete {pkg}')
                print(f'Error: {e}')
                exit(11)

    print(f'{colors.fg.green}✅ Successfully deleted packages{colors.reset}')
    print()

    new_packages = get_new_packages(repo_path)
    if not only_delete:
        print('=== Adding new packages ===')
        for pkg in new_packages:
            print(f'Adding {pkg}...')
            if not dry_run:
                output = getstatusoutput(
                    f'repo-add {repo_path}/{repo_name}.db.tar.zst {repo_path}/{pkg}'
                )
                if output[0] != 0:
                    print(f'{colors.bg.red}[ERROR]{colors.reset} failed to add {pkg}')
                    print(f'Exit code: {output[0]}')
                    print(f'Command output:\n{output[1]}')
                    exit(12)
        print(
            f'{colors.fg.green}✅ Successfully added new packages to repo{colors.reset}'
        )
        print()

    print(f'✨ {colors.bg.green}Repo successfully updated{colors.reset} ✨')


@cli.command('list-old-packages')
@click.option(
    '--list-debug',
    required=False,
    default=True,
    help='List debug symbol packages (default: true)'
)
@click.argument('repo_path')
def get_old_packages_runner(repo_path, list_debug=True):
    '''
    Lists old versions of packages
    '''
    for item in get_old_packages(repo_path, list_debug):
        click.echo(item)


def get_old_packages(repo_path, list_debug=True):
    pkg_map = HelperFunctions.package_map(repo_path)
    old_packages = []
    for pkg_name in pkg_map:
        no_debug = []
        for item in pkg_map[pkg_name]:
            # does nothing, but something needs to go here otherwise the linter complains about syntax; it needs the else for some reason
            no_debug.append(item) if not item.startswith(f'{pkg_name}-debug') else False

        # skip in case there isn't an old version
        if len(no_debug) == 1:
            continue

        old_no_debug = natsorted(no_debug)[:1]
        old_packages.extend(old_no_debug)
        for item in old_no_debug:
            debug_pkg = item.replace(pkg_name, f'{pkg_name}-debug')
            if list_debug and debug_pkg in pkg_map[pkg_name]:
                old_packages.append(debug_pkg)

    return natsorted(old_packages)


@cli.command('list-new-packages')
@click.option(
    '--list-debug',
    required=False,
    default=True,
    help='List debug symbol packages (default: true)'
)
@click.argument('repo_path')
def get_new_packages_runner(repo_path, list_debug=True):
    for item in get_new_packages(repo_path, list_debug):
        click.echo(item)


def get_new_packages(repo_path, list_debug=True):
    '''
    Lists the newest version of all packages
    '''
    # this is pretty much just an inverted version of get_old_packages()
    # the different parts are the second and third blocks of code here
    pkg_map = HelperFunctions.package_map(repo_path)
    new_packages = []
    for pkg_name in pkg_map:
        no_debug = []
        for item in pkg_map[pkg_name]:
            # does nothing, but something needs to go here otherwise the linter complains about syntax; it needs the else for some reason
            no_debug.append(item) if not item.startswith(f'{pkg_name}-debug') else False

        # add all in case there isn't an old version
        if len(no_debug) == 1:
            new_packages.append(no_debug[0])
            if (
                list_debug
                and no_debug[0].replace(pkg_name, f'{pkg_name}-debug')
                in pkg_map[pkg_name]
            ):
                new_packages.append(no_debug[0].replace(pkg_name, f'{pkg_name}-debug'))
            continue

        new_no_debug = natsorted(no_debug)[1:]
        new_packages.extend(new_no_debug)
        for item in new_no_debug:
            if (
                list_debug
                and item.replace(pkg_name, f'{pkg_name}-debug') in pkg_map[pkg_name]
            ):
                new_packages.append(item.replace(pkg_name, f'{pkg_name}-debug'))

    return natsorted(new_packages)


class HelperFunctions:
    def package_map(repo_path):
        '''
        Returns a dictionary containing all the packages in the repo

        Example:
        {
            'swayfx': [
                'swayfx-0.4-3-x86_64.pkg.tar.zst',
                'swayfx-debug-0.4-3-x86_64.pkg.tar.zst',
                'swayfx-0.3.2-1-x86_64.pkg.tar.zst
            ]
        }
        '''
        files = HelperFunctions.get_package_list(repo_path)

        # contains all packages in the repo
        package_map = {}

        package_names = []
        for item in files:
            package_name = item[: item.rfind('-')]
            package_name = package_name[: package_name.rfind('-')]
            package_name = package_name[: package_name.rfind('-')]
            package_names.append(package_name)

        for item in files:
            package_name = item[: item.rfind('-')]
            package_name = package_name[: package_name.rfind('-')]
            package_name = package_name[: package_name.rfind('-')]

            # can't just do endswith(), since normal packages can also end in `-debug`, like `dosbox-debug` in the AUR
            # and if it still fails, that's a conflicting package failure, not an issue with the program
            if package_name.endswith('-debug') and package_name[:-6] in package_names:
                package_name = package_name[:-6]

            try:
                package_map[package_name].append(item)
            except KeyError:
                package_map[package_name] = []
                package_map[package_name].append(item)

        for pkgs in package_map:
            pkgs = natsorted(pkgs)

        return package_map

    def get_repo_name(repo_path):
        repo_name = glob.glob(f'{repo_path}/*.db')[0]
        repo_name = repo_name[repo_name.rfind('/') + 1 :]
        repo_name = repo_name[: repo_name.find('.')]
        return repo_name

    def get_package_list(repo_path):
        '''
        Lists all packages in repo_path, excluding the repo files (.db, .files)
        '''
        files = glob.glob(f'{repo_path}/*.tar.zst')
        files = [f[f.rfind('/') + 1 :] for f in files]
        repo_name = HelperFunctions.get_repo_name(repo_path)

        try:
            files.remove(f'{repo_name}.db.tar.zst')
            files.remove(f'{repo_name}.files.tar.zst')
        except FileNotFoundError:
            pass

        return natsorted(files)


if __name__ == '__main__':
    cli()
