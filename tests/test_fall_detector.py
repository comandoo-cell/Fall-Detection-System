"""Tests for FallDetector aligned with current implementation.

Bu testler src/core/fall_detector.py dosyasındaki mevcut API'ye göre yazıldı:
- Girdi: isimlendirilmiş eklem noktaları (dict)
- detect_fall(keypoints: Dict) -> bool döner
"""

import unittest

from src.core.fall_detector import FallDetector


def make_standing_keypoints() -> dict:
    """Ayakta duran bir kişi için yaklaşık eklem noktaları."""

    return {
        "nose": (140, 60),
        "left_shoulder": (120, 100),
        "right_shoulder": (160, 100),
        "left_hip": (130, 200),
        "right_hip": (150, 200),
        "left_ankle": (135, 300),
        "right_ankle": (145, 300),
    }


def make_fallen_keypoints() -> dict:
    """Yerde yatan (düşmüş) bir kişi için yaklaşık eklem noktaları."""

    return {
        "nose": (180, 190),
        "left_shoulder": (120, 180),
        "right_shoulder": (220, 180),
        "left_hip": (140, 190),
        "right_hip": (260, 190),
        "left_ankle": (150, 200),
        "right_ankle": (250, 200),
    }


class TestFallDetectorGeometry(unittest.TestCase):
    """Açı ve en-boy oranı hesaplarının temel testleri."""

    def setUp(self):
        self.detector = FallDetector()

    def test_calculate_angle_vertical_horizontal(self):
        """Dikey çizgi ~90°, yatay çizgi ~0° olmalı."""

        angle_vertical = self.detector.calculate_angle((100, 50), (100, 150))
        self.assertGreater(angle_vertical, 80.0)
        self.assertLess(angle_vertical, 100.0)

        angle_horizontal = self.detector.calculate_angle((50, 100), (150, 100))
        self.assertLess(angle_horizontal, 10.0)

    def test_body_angle_standing_vs_fallen(self):
        """Ayakta vücut açısı yüksek, düşmüşte düşük olmalı."""

        standing = make_standing_keypoints()
        fallen = make_fallen_keypoints()

        angle_standing = self.detector.calculate_body_angle(standing)
        angle_fallen = self.detector.calculate_body_angle(fallen)

        self.assertIsNotNone(angle_standing)
        self.assertIsNotNone(angle_fallen)

        self.assertGreater(angle_standing, 60.0)
        self.assertLess(angle_fallen, 30.0)

    def test_aspect_ratio_standing_vs_fallen(self):
        """Ayakta kutu dar/uzun, düşmüşte geniş/alay yatay olmalı."""

        standing = make_standing_keypoints()
        fallen = make_fallen_keypoints()

        ratio_standing = self.detector.calculate_aspect_ratio(standing)
        ratio_fallen = self.detector.calculate_aspect_ratio(fallen)

        self.assertIsNotNone(ratio_standing)
        self.assertIsNotNone(ratio_fallen)

        self.assertLess(ratio_standing, 1.0)
        self.assertGreater(ratio_fallen, 1.2)


class TestFallDetectorLogic(unittest.TestCase):
    """Yüksek seviye düşme tespit davranışı."""

    def setUp(self):
        self.detector = FallDetector()

    def test_standing_never_confirms_fall(self):
        """Uzun süre ayakta pozlarda düşme onaylanmamalı."""

        standing = make_standing_keypoints()
        any_detected = False
        for _ in range(20):
            detected = self.detector.detect_fall(standing)
            any_detected = any_detected or detected

        self.assertFalse(any_detected)
        self.assertFalse(self.detector.get_fall_info()["is_fallen"])

    def test_fallen_after_standing_triggers_fall(self):
        """Önce ayakta, sonra birkaç kare düşme gelince algılanmalı."""

        standing = make_standing_keypoints()
        fallen = make_fallen_keypoints()

        # İlk karelerde kişi ayakta olsun (maksimum açı öğrenilsin)
        for _ in range(15):
            _ = self.detector.detect_fall(standing)

        fall_detected = False
        for _ in range(5):
            fall_detected = self.detector.detect_fall(fallen)

        self.assertTrue(fall_detected)
        self.assertTrue(self.detector.get_fall_info()["is_fallen"])

    def test_empty_keypoints_reset_confidence(self):
        """Boş keypoints sözlüğü, durum ve güven skorunu sıfırlamalı."""

        fallen = make_fallen_keypoints()
        for _ in range(10):
            _ = self.detector.detect_fall(fallen)

        self.assertGreater(self.detector.get_confidence_score(), 0.0)

        detected = self.detector.detect_fall({})
        self.assertFalse(detected)
        self.assertEqual(self.detector.get_confidence_score(), 0.0)


if __name__ == "__main__":  # pragma: no cover
    unittest.main(verbosity=2)
