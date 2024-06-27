import unittest
from src.measure_volume import calculate_volume
import os

class TestModule2(unittest.TestCase):
    def test_calculate_volume(self):
        volume = calculate_volume("outputBrainExtractionMask.nii.gz")
        self.assertFalse(isinstance(volume, str))
        self.assertTrue(volume >= 0)


if __name__ == "__main__":
    unittest.main()
