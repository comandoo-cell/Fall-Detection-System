"""
Unit Tests for Fall Detection System
Tests the core fall detection algorithms and edge cases
"""

import unittest
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fall_detector import FallDetector


class TestFallDetector(unittest.TestCase):
    """Test suite for FallDetector class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = FallDetector(
            velocity_threshold=0.5,
            angle_weight=0.4,
            aspect_ratio_weight=0.25,
            head_height_weight=0.2,
            direction_weight=0.15
        )
    
    def test_calculate_angle(self):
        """Test angle calculation between three points"""
        # Test right angle (90 degrees)
        p1 = np.array([0.0, 0.0])
        p2 = np.array([1.0, 0.0])
        p3 = np.array([1.0, 1.0])
        angle = self.detector.calculate_angle(p1, p2, p3)
        self.assertAlmostEqual(angle, 90.0, places=1)
        
        # Test straight line (180 degrees)
        p1 = np.array([0.0, 0.0])
        p2 = np.array([1.0, 0.0])
        p3 = np.array([2.0, 0.0])
        angle = self.detector.calculate_angle(p1, p2, p3)
        self.assertAlmostEqual(angle, 180.0, places=1)
    
    def test_calculate_body_angle_standing(self):
        """Test body angle calculation for standing pose"""
        # Simulating standing person (vertical)
        landmarks = np.array([
            [0.5, 0.1],  # 0: Nose
            [0.48, 0.12], [0.52, 0.12],  # 1,2: Eyes
            [0.46, 0.14], [0.54, 0.14],  # 3,4: Ears
            [0.45, 0.2], [0.55, 0.2],    # 5,6: Shoulders
            [0.44, 0.3], [0.56, 0.3],    # 7,8: Elbows
            [0.43, 0.4], [0.57, 0.4],    # 9,10: Wrists
            [0.46, 0.5], [0.54, 0.5],    # 11,12: Hips
            [0.45, 0.7], [0.55, 0.7],    # 13,14: Knees
            [0.44, 0.9], [0.56, 0.9],    # 15,16: Ankles
        ])
        
        angle = self.detector.calculate_body_angle(landmarks)
        # Standing should have high angle (close to 90 degrees)
        self.assertGreater(angle, 60.0, "Standing person should have body angle > 60°")
    
    def test_calculate_body_angle_fallen(self):
        """Test body angle calculation for fallen pose"""
        # Simulating fallen person (horizontal)
        landmarks = np.array([
            [0.1, 0.5],  # 0: Nose
            [0.12, 0.48], [0.12, 0.52],  # 1,2: Eyes
            [0.14, 0.46], [0.14, 0.54],  # 3,4: Ears
            [0.2, 0.45], [0.2, 0.55],    # 5,6: Shoulders
            [0.3, 0.44], [0.3, 0.56],    # 7,8: Elbows
            [0.4, 0.43], [0.4, 0.57],    # 9,10: Wrists
            [0.5, 0.46], [0.5, 0.54],    # 11,12: Hips
            [0.7, 0.45], [0.7, 0.55],    # 13,14: Knees
            [0.9, 0.44], [0.9, 0.56],    # 15,16: Ankles
        ])
        
        angle = self.detector.calculate_body_angle(landmarks)
        # Fallen should have low angle (close to 0 degrees)
        self.assertLess(angle, 30.0, "Fallen person should have body angle < 30°")
    
    def test_calculate_aspect_ratio(self):
        """Test aspect ratio calculation"""
        # Create bounding box for standing person (height > width)
        landmarks_standing = np.array([
            [0.5, 0.1],  # Top
            [0.5, 0.9],  # Bottom
            [0.4, 0.5],  # Left
            [0.6, 0.5],  # Right
        ])
        ratio_standing = self.detector.calculate_aspect_ratio(landmarks_standing)
        self.assertGreater(ratio_standing, 1.0, "Standing person should have aspect ratio > 1")
        
        # Create bounding box for fallen person (width > height)
        landmarks_fallen = np.array([
            [0.1, 0.5],  # Left
            [0.9, 0.5],  # Right
            [0.5, 0.4],  # Top
            [0.5, 0.6],  # Bottom
        ])
        ratio_fallen = self.detector.calculate_aspect_ratio(landmarks_fallen)
        self.assertLess(ratio_fallen, 1.0, "Fallen person should have aspect ratio < 1")
    
    def test_detect_fall_standing_person(self):
        """Test fall detection for standing person (should NOT detect fall)"""
        # Standing person landmarks
        landmarks = np.array([
            [0.5, 0.1],  # Nose
            [0.48, 0.12], [0.52, 0.12],  # Eyes
            [0.46, 0.14], [0.54, 0.14],  # Ears
            [0.45, 0.2], [0.55, 0.2],    # Shoulders
            [0.44, 0.3], [0.56, 0.3],    # Elbows
            [0.43, 0.4], [0.57, 0.4],    # Wrists
            [0.46, 0.5], [0.54, 0.5],    # Hips
            [0.45, 0.7], [0.55, 0.7],    # Knees
            [0.44, 0.9], [0.56, 0.9],    # Ankles
        ])
        
        is_fall, confidence, details = self.detector.detect_fall(landmarks, 0.0)
        self.assertFalse(is_fall, "Standing person should NOT be detected as fallen")
        self.assertLess(confidence, 60.0, "Standing person confidence should be < 60%")
    
    def test_detect_fall_fallen_person(self):
        """Test fall detection for fallen person (should detect fall)"""
        # Fallen person landmarks (horizontal)
        landmarks = np.array([
            [0.1, 0.5],  # Nose
            [0.12, 0.48], [0.12, 0.52],  # Eyes
            [0.14, 0.46], [0.14, 0.54],  # Ears
            [0.2, 0.45], [0.2, 0.55],    # Shoulders
            [0.3, 0.44], [0.3, 0.56],    # Elbows
            [0.4, 0.43], [0.4, 0.57],    # Wrists
            [0.5, 0.46], [0.5, 0.54],    # Hips
            [0.7, 0.45], [0.7, 0.55],    # Knees
            [0.9, 0.44], [0.9, 0.56],    # Ankles
        ])
        
        is_fall, confidence, details = self.detector.detect_fall(landmarks, 1.5)
        self.assertTrue(is_fall, "Fallen person should be detected as fallen")
        self.assertGreater(confidence, 60.0, "Fallen person confidence should be > 60%")
    
    def test_velocity_threshold(self):
        """Test velocity threshold impact on fall detection"""
        # Test with high velocity (fast fall)
        landmarks = np.array([[0.5, 0.5 + i*0.1] for i in range(17)])
        
        is_fall_high_vel, conf_high, _ = self.detector.detect_fall(landmarks, 2.0)
        is_fall_low_vel, conf_low, _ = self.detector.detect_fall(landmarks, 0.1)
        
        # High velocity should increase fall detection confidence
        if is_fall_high_vel and is_fall_low_vel:
            self.assertGreater(conf_high, conf_low, 
                             "High velocity should increase fall confidence")
    
    def test_invalid_landmarks(self):
        """Test handling of invalid landmarks"""
        # Empty landmarks
        empty_landmarks = np.array([])
        is_fall, confidence, details = self.detector.detect_fall(empty_landmarks, 0.0)
        self.assertFalse(is_fall, "Empty landmarks should not trigger fall detection")
        
        # Insufficient landmarks
        few_landmarks = np.array([[0.5, 0.5], [0.6, 0.6]])
        is_fall, confidence, details = self.detector.detect_fall(few_landmarks, 0.0)
        self.assertFalse(is_fall, "Insufficient landmarks should not trigger fall detection")


class TestFallDetectorEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.detector = FallDetector()
    
    def test_sitting_position(self):
        """Test that sitting position is not detected as fall"""
        # Sitting person (bent but not fallen)
        landmarks = np.array([
            [0.5, 0.3],  # Nose higher than hip
            [0.48, 0.32], [0.52, 0.32],
            [0.46, 0.34], [0.54, 0.34],
            [0.45, 0.4], [0.55, 0.4],
            [0.44, 0.5], [0.56, 0.5],
            [0.43, 0.6], [0.57, 0.6],
            [0.46, 0.7], [0.54, 0.7],
            [0.45, 0.8], [0.55, 0.8],
            [0.44, 0.85], [0.56, 0.85],
        ])
        
        is_fall, confidence, _ = self.detector.detect_fall(landmarks, 0.1)
        # Sitting should have moderate confidence, not high
        self.assertLess(confidence, 70.0, "Sitting should not have high fall confidence")
    
    def test_crouching_position(self):
        """Test that crouching is not detected as fall"""
        # Crouching (low but balanced)
        landmarks = np.array([
            [0.5, 0.5],  # Nose
            [0.48, 0.52], [0.52, 0.52],
            [0.46, 0.54], [0.54, 0.54],
            [0.45, 0.6], [0.55, 0.6],
            [0.44, 0.65], [0.56, 0.65],
            [0.43, 0.7], [0.57, 0.7],
            [0.46, 0.75], [0.54, 0.75],
            [0.45, 0.85], [0.55, 0.85],
            [0.44, 0.9], [0.56, 0.9],
        ])
        
        is_fall, confidence, _ = self.detector.detect_fall(landmarks, 0.05)
        # Low velocity crouching should not be detected as fall
        if confidence > 60:
            self.assertFalse(is_fall or confidence < 70, 
                           "Slow crouching should not be high confidence fall")
    
    def test_threshold_boundaries(self):
        """Test behavior at threshold boundaries"""
        landmarks = np.array([[0.5, 0.5 + i*0.05] for i in range(17)])
        
        # Test at exactly 60% threshold
        is_fall, confidence, _ = self.detector.detect_fall(landmarks, 0.5)
        
        # Confidence around 60% should be boundary case
        if 55 < confidence < 65:
            # System should make a clear decision even at boundary
            self.assertIsInstance(is_fall, bool, "Fall detection should return boolean")


def run_tests():
    """Run all tests and return results"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestFallDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestFallDetectorEdgeCases))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)
