import os
import shutil
import unittest
import sys
from xppkg import util

class TestDistribution(unittest.TestCase):
    DIST_DIR = 'dist'
    DIST_DIR_BACKUP = '%s_backup' % DIST_DIR
    def setUp(self):
        self.cwd = os.getcwd()
        # if we can find the dist dir, remove it
        self.dist_dir = os.path.join(self.cwd, self.DIST_DIR)
        self.dist_dir_backup = os.path.join(self.cwd, self.DIST_DIR_BACKUP)

        if os.path.isdir(self.dist_dir):
            #shutil.rmtree(self.dist_dir)
            # move the dist out of the way, to move it back in the teardown process
            shutil.move(self.dist_dir, self.dist_dir_backup)


    def test_sdist(self):
        # test if there is a setup.py
        self.assertTrue(os.path.isfile(os.path.join(self.cwd, 'setup.py')))
        # test if dist directory is removed
        self.assertFalse(os.path.isdir(self.dist_dir))
        # test if python setup.py dist return 0

        returned_output = util.call_subprocess([sys.executable, 'setup.py','sdist'])
        #returned_output = subprocess.call([sys.executable, 'setup.py','sdist'])
        #self.assertEqual(returned_output,0)
        self.assertIsNone(returned_output)
        self.assertTrue(os.path.isdir(self.dist_dir))
        filenames = os.listdir(self.dist_dir)
        self.assertGreaterEqual(len(filenames),1)

    def tearDown(self):
        if os.path.isdir(self.dist_dir_backup) and os.path.isdir (self.dist_dir):
            shutil.rmtree(self.dist_dir)
            shutil.move(self.dist_dir_backup, self.dist_dir)

if __name__ == '__main__':
    unittest.main(verbosity=2)
