import unittest
from ml_time_series import generate_envelope
import numpy as np

class TestMlTimeSeries(unittest.TestCase):
    def test_generate_envelope_one_chanel(self):
        v1 = np.array([1,2,3])
        r1 = generate_envelope(v1, 2)
        expeted = np.array([[1,2],[2,3]])
        self.assertTrue((r1 == expeted).all())

    def test_generate_evnelop_two_channels(self):
        v1 = np.array([[1,2],[3,4],[5,6]])
        r1 = generate_envelope(v1, 2)
        #expected = np.array([[1,3, 2, 4],[3,5, 4,6]])
        expected = np.array([[1,2,3,4],[3,4,5,6]])
        self.assertTrue((r1 == expected).all())
