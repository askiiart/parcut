import unittest
import os
from pathlib import Path
from natsort import natsorted

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


# NOTE: Add lists are wrapped in natsorted() so that they can be easily manually edited,
# rather than having to run and update them manually each time a test is updated
class Tests(unittest.TestCase):
    def test_run(self):
        create_test_data()
        # to run a click command - https://stackoverflow.com/questions/48619517/call-a-click-command-from-code
        repo_cleanup.run([repo_path, '--only-delete'], standalone_mode=False)
        result = natsorted(os.listdir(repo_path))
        expected = natsorted(
            [
                'example-program-8.4.3-5-x86_64.pkg.tar.zst',
                'example-program-10.2.1-2-x86_64.pkg.tar.zst',
                'example-program-debug-10.2.1-2-x86_64.pkg.tar.zst',
                'repo.db',
                'repo.db.tar.zst',
                'repo.files',
                'repo.files.tar.zst',
                'test-debug-r87.e176baf-1-x86_64.pkg.tar.zst',
                'test-debug-r100.ab937ef-1-x86_64.pkg.tar.zst',
                'test-r87.e176baf-1-x86_64.pkg.tar.zst',
                'test-r100.ab937ef-1-x86_64.pkg.tar.zst'
            ]
        )

    def test_list_old(self):
        create_test_data()
        result = repo_cleanup.get_old_packages(repo_path)
        expected = natsorted(
            [
                'example-program-8.4.3-5-x86_64.pkg.tar.zst',
                'test-debug-r87.e176baf-1-x86_64.pkg.tar.zst',
                'test-r87.e176baf-1-x86_64.pkg.tar.zst'
            ]
        )
        self.assertEqual(result, expected)

    def test_list_old_no_debug(self):
        create_test_data()
        result = repo_cleanup.get_old_packages(repo_path, list_debug=False)
        expected = natsorted(
            [
                'example-program-8.4.3-5-x86_64.pkg.tar.zst',
                'test-r87.e176baf-1-x86_64.pkg.tar.zst'
            ]
        )
        self.assertEqual(result, expected)

    def test_list_new(self):
        create_test_data()
        result = repo_cleanup.get_new_packages(repo_path)
        expected = natsorted(
            [
                'example-program-10.2.1-2-x86_64.pkg.tar.zst',
                'example-program-debug-10.2.1-2-x86_64.pkg.tar.zst',
                'test-debug-r100.ab937ef-1-x86_64.pkg.tar.zst',
                'test-r100.ab937ef-1-x86_64.pkg.tar.zst'
            ]
        )
        self.assertEqual(result, expected)

    def test_list_new_no_debug(self):
        create_test_data()
        result = repo_cleanup.get_new_packages(repo_path)
        expected = natsorted(
            [
                'example-program-10.2.1-2-x86_64.pkg.tar.zst',
                'example-program-debug-10.2.1-2-x86_64.pkg.tar.zst',
                'test-debug-r100.ab937ef-1-x86_64.pkg.tar.zst',
                'test-r100.ab937ef-1-x86_64.pkg.tar.zst'
            ]
        )
        self.assertEqual(result, expected)

    def test_package_map(self):
        create_test_data()
        result = repo_cleanup.HelperFunctions.package_map(repo_path)
        # only the lists are sorted, not the keys, so it should be manually run then verified it's correct if the keys are updated
        # you can change the items in the list safely, though
        expected = {
            'example-program': natsorted(
                [
                    'example-program-8.4.3-5-x86_64.pkg.tar.zst',
                    'example-program-10.2.1-2-x86_64.pkg.tar.zst',
                    'example-program-debug-10.2.1-2-x86_64.pkg.tar.zst'
                ]
            ),
            'test': natsorted(
                [
                    'test-debug-r87.e176baf-1-x86_64.pkg.tar.zst',
                    'test-debug-r100.ab937ef-1-x86_64.pkg.tar.zst',
                    'test-r87.e176baf-1-x86_64.pkg.tar.zst',
                    'test-r100.ab937ef-1-x86_64.pkg.tar.zst'
                ]
            )
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
