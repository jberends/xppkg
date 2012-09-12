import os
import shutil
import subprocess
import unittest
import sys

class TestDistribution(unittest.TestCase):
    DIST_DIR = 'dist'
    def setUp(self):
        self.cwd = os.getcwd()
        # if we can find the dist dir, remove it
        self.dist_dir = os.path.join(self.cwd, self.DIST_DIR)

        if os.path.isdir(self.dist_dir):
            shutil.rmtree(self.dist_dir)


    def test_sdist(self):
        # test if there is a setup.py
        self.assertTrue(os.path.isfile(os.path.join(self.cwd, 'setup.py')))
        # test if dist directory is removed
        self.assertFalse(os.path.isdir(self.dist_dir))
        # test if python setup.py dist return 0

        returncode = subprocess.call([sys.executable, 'setup.py','sdist'])
        self.assertEqual(returncode,0)
        self.assertTrue(os.path.isdir(self.dist_dir))
        filenames = os.listdir(self.dist_dir)
        self.assertGreaterEqual(len(filenames),1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
