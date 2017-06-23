import unittest
from ml_time_series import generate_envelope
import numpy as np

class TestMlTimeSeries(unittest.TestCase):
    def test_generate_envelope(self):
        v1 = np.array([1,2,3])
        r1 = generate_envelope(v1, 2)
        expeted = np.array([[1,2],[2,3]])
        self.assertTrue((r1 == expeted).all())
