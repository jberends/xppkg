"""
Tests the installation op OpensceneryX
http://www.opensceneryx.com/
"""

import unittest

class TestInstallOpensceneryX(unittest.TestCase):
    def setUp(self):
        self.cwd = os.getcwd()


    # remove opensceneryx first
    # if we can find the dist dir, remove it
    self.dist_dir = os.path.join(self.cwd, self.DIST_DIR)

    if os.path.isdir(self.dist_dir):
        shutil.rmtree(self.dist_dir)



    def test_something(self):
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()
