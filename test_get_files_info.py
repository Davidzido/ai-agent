import unittest
from functions.get_files_info import get_files_info

class TestGetFilesInfo(unittest.TestCase):

    def test_current_directory(self):
        result = get_files_info("calculator", ".")
        print("Result for current directory:")
        print(result)
    
    def test_pkg_directory(self):
        result = get_files_info("calculator", "pkg")
        print("Result for pkg:")
        print(result)

    def test_bin_directory(self):
        result = get_files_info("calculator", "/bin")
        print("Result for 'bin' directory:")
        print(result)

    def test_parent_directory(self):
        result = get_files_info("calculator", "../")
        print("Result for parent directory:")
        print(result)

if __name__ == "__main__":
    unittest.main()