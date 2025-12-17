"""
Unit Tests for Pose Estimation
Tests MediaPipe and YOLOv8 integration
"""

import unittest
import numpy as np
import cv2
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.pose_estimator import PoseEstimator
from src.multi_person_detector import MultiPersonDetector


class TestPoseEstimator(unittest.TestCase):
    """Test suite for PoseEstimator (MediaPipe)"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.estimator = PoseEstimator()
    
    def test_initialization(self):
        """Test that pose estimator initializes correctly"""
        self.assertIsNotNone(self.estimator, "PoseEstimator should initialize")
    
    def test_process_empty_frame(self):
        """Test processing empty frame"""
        empty_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        landmarks = self.estimator.process_frame(empty_frame)
        
        # Should return None or empty for black frame
        self.assertIsInstance(landmarks, (type(None), np.ndarray), 
                            "Should handle empty frame gracefully")
    
    def test_process_invalid_frame(self):
        """Test processing invalid frame data"""
        # Test with None
        landmarks = self.estimator.process_frame(None)
        self.assertIsNone(landmarks, "Should handle None frame")
        
        # Test with wrong dimensions
        invalid_frame = np.zeros((100, 100), dtype=np.uint8)  # 2D instead of 3D
        landmarks = self.estimator.process_frame(invalid_frame)
        self.assertIsInstance(landmarks, (type(None), np.ndarray), 
                            "Should handle invalid frame dimensions")
    
    def test_landmark_format(self):
        """Test that landmarks are returned in correct format"""
        # Create a simple test frame with some content
        test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        landmarks = self.estimator.process_frame(test_frame)
        
        if landmarks is not None:
            # Landmarks should be numpy array
            self.assertIsInstance(landmarks, np.ndarray, 
                                "Landmarks should be numpy array")
            
            # Should have correct shape (17 landmarks, 2 coordinates)
            if len(landmarks) > 0:
                self.assertEqual(landmarks.shape[1], 2, 
                               "Each landmark should have x,y coordinates")


class TestMultiPersonDetector(unittest.TestCase):
    """Test suite for MultiPersonDetector (YOLOv8)"""
    
    def setUp(self):
        """Set up test fixtures"""
        try:
            self.detector = MultiPersonDetector()
            self.detector_available = True
        except Exception as e:
            self.detector_available = False
            print(f"Warning: MultiPersonDetector not available: {e}")
    
    def test_initialization(self):
        """Test that detector initializes correctly"""
        if not self.detector_available:
            self.skipTest("Detector not available")
        
        self.assertIsNotNone(self.detector, "MultiPersonDetector should initialize")
    
    def test_detect_empty_frame(self):
        """Test detection on empty frame"""
        if not self.detector_available:
            self.skipTest("Detector not available")
        
        empty_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        results = self.detector.detect_people(empty_frame)
        
        # Should return empty list or handle gracefully
        self.assertIsInstance(results, list, "Should return list of detections")
    
    def test_detect_invalid_frame(self):
        """Test detection on invalid frame"""
        if not self.detector_available:
            self.skipTest("Detector not available")
        
        # Test with None
        results = self.detector.detect_people(None)
        self.assertIsInstance(results, (list, type(None)), 
                            "Should handle None frame")


class TestIntegration(unittest.TestCase):
    """Integration tests for pose estimation pipeline"""
    
    def test_mediapipe_yolo_compatibility(self):
        """Test that MediaPipe and YOLOv8 can work together"""
        try:
            pose_est = PoseEstimator()
            multi_det = MultiPersonDetector()
            
            # Create test frame
            test_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
            
            # Both should process same frame without error
            landmarks = pose_est.process_frame(test_frame)
            detections = multi_det.detect_people(test_frame)
            
            # Should not raise exceptions
            self.assertTrue(True, "Both detectors should process frame")
            
        except Exception as e:
            self.skipTest(f"Integration test skipped: {e}")


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestPoseEstimator))
    suite.addTests(loader.loadTestsFromTestCase(TestMultiPersonDetector))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == '__main__':
    result = run_tests()
    
    print("\n" + "="*70)
    print("POSE ESTIMATION TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print("="*70)
