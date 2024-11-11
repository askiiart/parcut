#!/usr/bin/env python3
from natsort import natsorted
import click
import glob


@click.group('cli')
def cli():
    """Clean up and manage Pacman repos"""


@cli.command('run')
@click.option('--dry-run', is_flag=True, default=False, help="Do a dry run")
@click.option('--only-delete', is_flag=True, default=False, help="Only delete files, don't run repo-remove and repo-add on their old and new versions (default: false)")
@click.option('--delete-debug', is_flag=True, default=False, help="Delete debug symbol packages (default: false)")
@click.argument('repo_path')
def run(repo_path, dry_run=False, only_delete=False, delete_debug=False):
    get_old_packages_runner(repo_path)


@cli.command('list-old-packages')
@click.option('--list-debug', required=False, default=True, help="List debug symbol packages (default: true)")
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
            no_debug.append(item) if not item.startswith(
                f'{pkg_name}-debug') else False

        # skip in case there isn't an old version
        if len(no_debug) == 1:
            continue

        old_no_debug = natsorted(no_debug)[:1]
        old_packages.extend(old_no_debug)
        for item in old_no_debug:
            if list_debug and item.replace(pkg_name, f'{pkg_name}-debug') in pkg_map[pkg_name]:
                old_packages.append(item.replace(
                    pkg_name, f'{pkg_name}-debug'))

    return natsorted(old_packages)


@cli.command('list-new-packages')
@click.option('--list-debug', required=False, default=True, help="List debug symbol packages (default: true)")
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
            no_debug.append(item) if not item.startswith(
                f'{pkg_name}-debug') else False

        # add all in case there isn't an old version
        if len(no_debug) == 1:
            new_packages.append(no_debug[0])
            if list_debug and no_debug[0].replace(pkg_name, f'{pkg_name}-debug') in pkg_map[pkg_name]:
                new_packages.append(no_debug[0].replace(
                    pkg_name, f'{pkg_name}-debug'))
            continue

        new_no_debug = natsorted(no_debug)[1:]
        new_packages.extend(new_no_debug)
        for item in new_no_debug:
            if list_debug and item.replace(pkg_name, f'{pkg_name}-debug') in pkg_map[pkg_name]:
                new_packages.append(item.replace(
                    pkg_name, f'{pkg_name}-debug'))

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
            package_name = item[:item.rfind('-')]
            package_name = package_name[:package_name.rfind('-')]
            package_name = package_name[:package_name.rfind('-')]
            package_names.append(package_name)

        for item in files:
            package_name = item[:item.rfind('-')]
            package_name = package_name[:package_name.rfind('-')]
            package_name = package_name[:package_name.rfind('-')]

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
        repo_name = repo_name[repo_name.rfind('/')+1:]
        repo_name = repo_name[:repo_name.find('.')]
        return (repo_name)

    def get_package_list(repo_path):
        '''
        Lists all packages in repo_path, excluding the repo files (.db, .files)
        '''
        files = glob.glob(f'{repo_path}/*.tar.zst')
        files = [f[f.rfind('/')+1:] for f in files]
        repo_name = HelperFunctions.get_repo_name(repo_path)

        files.remove(
            f'{repo_name}.db.tar.zst')
        files.remove(
            f'{repo_name}.files.tar.zst')

        return natsorted(files)


if __name__ == '__main__':
    cli()


class colors:
    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

        rainbow = [lightred, orange, yellow,
                   lightgreen, lightcyan, blue, purple]

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


fg = colors.fg()
