import unittest
import os
from pathlib import Path

repo_cleanup = __import__('repo-cleanup')
repo_path = 'repo/'


def touch(path):
    Path(path).touch()


def create_test_data():
    try:
        os.mkdir(repo_path)
    except FileExistsError:
        pass

    files = [
        'test-r87.e176baf-1-x86_64.pkg.tar.zst',
        'test-debug-r87.e176baf-1-x86_64.pkg.tar.zst',
        'test-debug-r100.ab937ef-1-x86_64.pkg.tar.zst',
        'test-r100.ab937ef-1-x86_64.pkg.tar.zst',
        'repo.db',
        'repo.db.tar.zst',
        'repo.files',
        'repo.files.tar.zst',
        'example-program-10.2.1-2-x86_64.pkg.tar.zst',
        'example-program-8.4.3-5-x86_64.pkg.tar.zst',
        'example-program-debug-10.2.1-2-x86_64.pkg.tar.zst'
    ]
    for f in files:
        touch(f'{repo_path}/{f}')


class Tests(unittest.TestCase):
    def test_list_old(self):
        create_test_data()
        result = repo_cleanup.get_old_packages(repo_path)
        expected = [
            'example-program-8.4.3-5-x86_64.pkg.tar.zst',
            'test-debug-r87.e176baf-1-x86_64.pkg.tar.zst',
            'test-r87.e176baf-1-x86_64.pkg.tar.zst'
        ]
        self.assertEqual(result, expected)

    def test_list_new(self):
        create_test_data()
        result = repo_cleanup.get_new_packages(repo_path)
        expected = [
            'example-program-10.2.1-2-x86_64.pkg.tar.zst',
            'example-program-debug-10.2.1-2-x86_64.pkg.tar.zst',
            'test-debug-r100.ab937ef-1-x86_64.pkg.tar.zst',
            'test-r100.ab937ef-1-x86_64.pkg.tar.zst'
        ]
        self.assertEqual(result, expected)

    def test_package_map(self):
        create_test_data()
        result = repo_cleanup.HelperFunctions.package_map(repo_path)
        expected = {
            'example-program': [
                'example-program-8.4.3-5-x86_64.pkg.tar.zst',
                'example-program-10.2.1-2-x86_64.pkg.tar.zst',
                'example-program-debug-10.2.1-2-x86_64.pkg.tar.zst'
            ],
            'test': [
                'test-debug-r87.e176baf-1-x86_64.pkg.tar.zst',
                'test-debug-r100.ab937ef-1-x86_64.pkg.tar.zst',
                'test-r87.e176baf-1-x86_64.pkg.tar.zst',
                'test-r100.ab937ef-1-x86_64.pkg.tar.zst'
            ]
        }
        self.assertEqual(result, expected)

    def test_repo_name(self):
        create_test_data()
        result = repo_cleanup.HelperFunctions.get_repo_name(repo_path)
        expected = 'repo'
        self.assertEqual(result, expected)

    def test_package_list(self):
        create_test_data()
        result = repo_cleanup.HelperFunctions.get_package_list(repo_path)
        expected = [
            'example-program-8.4.3-5-x86_64.pkg.tar.zst',
            'example-program-10.2.1-2-x86_64.pkg.tar.zst',
            'example-program-debug-10.2.1-2-x86_64.pkg.tar.zst',
            'test-debug-r87.e176baf-1-x86_64.pkg.tar.zst',
            'test-debug-r100.ab937ef-1-x86_64.pkg.tar.zst',
            'test-r87.e176baf-1-x86_64.pkg.tar.zst',
            'test-r100.ab937ef-1-x86_64.pkg.tar.zst'
        ]
        self.assertEqual(result, expected)


create_test_data()
