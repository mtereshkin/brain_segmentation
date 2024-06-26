import unittest
from src.main import main
import os

class TestModule1(unittest.TestCase):
    def test_main(self):
        dirlist = os.listdir("png_overlays")
        self.assertEqual(len(dirlist), 3)
        for file in dirlist:
            self.assertTrue(file.endswith('png'))
        
        self.assertTrue(os.path.exists("CT2.nii.gz"))
        self.assertTrue(os.path.exists("outputBrainExtractionMask.nii.gz"))

if __name__ == "__main__":
    unittest.main()
