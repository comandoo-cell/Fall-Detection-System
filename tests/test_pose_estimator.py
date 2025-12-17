"""Pose Estimation ve Multi-Person Detector testleri.

Mevcut implementasyonlara göre sadeleştirilmiş smoke testler:
- PoseEstimator.process_frame -> bool döner
- MultiPersonDetector.detect_people -> list döner
"""

import unittest
import numpy as np

from src.models.pose_estimator import PoseEstimator
from src.models.multi_person_detector import MultiPersonDetector


class TestPoseEstimator(unittest.TestCase):
    """PoseEstimator (MediaPipe) için basit testler."""

    def setUp(self):
        self.estimator = PoseEstimator()

    def test_initialization(self):
        self.assertIsNotNone(self.estimator)

    def test_process_frame_returns_bool(self):
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        result = self.estimator.process_frame(frame)
        self.assertIsInstance(result, bool)

    def test_get_all_keypoints_format(self):
        frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        _ = self.estimator.process_frame(frame)

        keypoints = self.estimator.get_all_keypoints(frame_width=640, frame_height=480)
        self.assertIsInstance(keypoints, dict)
        for name, coords in keypoints.items():
            self.assertIsInstance(name, str)
            self.assertIsInstance(coords, tuple)
            self.assertEqual(len(coords), 2)


class TestMultiPersonDetector(unittest.TestCase):
    """MultiPersonDetector (YOLOv8) için hafif testler.

    Model yüklenemezse testler fail olmasın diye skip edilir.
    """

    def setUp(self):
        try:
            self.detector = MultiPersonDetector()
            self.available = True
        except Exception as e:  # pragma: no cover
            self.available = False
            self.skip_reason = str(e)

    def test_initialization(self):
        if not self.available:
            self.skipTest(f"YOLO modeli yok: {self.skip_reason}")

        self.assertIsNotNone(self.detector)

    def test_detect_empty_frame(self):
        if not self.available:
            self.skipTest(f"YOLO modeli yok: {self.skip_reason}")

        frame = np.zeros((240, 320, 3), dtype=np.uint8)
        people = self.detector.detect_people(frame)
        self.assertIsInstance(people, list)


if __name__ == "__main__":  # pragma: no cover
    unittest.main(verbosity=2)
