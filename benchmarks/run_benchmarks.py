"""
Performance Benchmarks for Fall Detection System
Measures accuracy, precision, recall, F1-score, and FPS
"""

import sys
import os
import time
import numpy as np
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import json
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.fall_detector import FallDetector


class BenchmarkRunner:
    """Run comprehensive benchmarks on fall detection system"""
    
    def __init__(self):
        self.detector = FallDetector()
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'tests': [],
            'summary': {}
        }
    
    def generate_test_cases(self):
        """Generate synthetic test cases for benchmarking"""
        test_cases = []
        
        # Standing person cases (should NOT detect fall)
        for i in range(50):
            landmarks = np.array([
                [0.5 + np.random.uniform(-0.02, 0.02), 0.1 + i*0.01],  # Nose
                [0.48, 0.12], [0.52, 0.12],  # Eyes
                [0.46, 0.14], [0.54, 0.14],  # Ears
                [0.45, 0.2], [0.55, 0.2],    # Shoulders
                [0.44, 0.3], [0.56, 0.3],    # Elbows
                [0.43, 0.4], [0.57, 0.4],    # Wrists
                [0.46, 0.5], [0.54, 0.5],    # Hips
                [0.45, 0.7], [0.55, 0.7],    # Knees
                [0.44, 0.9], [0.56, 0.9],    # Ankles
            ])
            test_cases.append({
                'landmarks': landmarks,
                'velocity': np.random.uniform(0.0, 0.3),
                'label': 0,  # No fall
                'description': f'Standing person {i+1}'
            })
        
        # Fallen person cases (SHOULD detect fall)
        for i in range(50):
            landmarks = np.array([
                [0.1 + i*0.01, 0.5 + np.random.uniform(-0.02, 0.02)],  # Nose
                [0.12, 0.48], [0.12, 0.52],  # Eyes
                [0.14, 0.46], [0.14, 0.54],  # Ears
                [0.2, 0.45], [0.2, 0.55],    # Shoulders
                [0.3, 0.44], [0.3, 0.56],    # Elbows
                [0.4, 0.43], [0.4, 0.57],    # Wrists
                [0.5, 0.46], [0.5, 0.54],    # Hips
                [0.7, 0.45], [0.7, 0.55],    # Knees
                [0.9, 0.44], [0.9, 0.56],    # Ankles
            ])
            test_cases.append({
                'landmarks': landmarks,
                'velocity': np.random.uniform(0.8, 2.5),
                'label': 1,  # Fall
                'description': f'Fallen person {i+1}'
            })
        
        # Sitting cases (should NOT detect fall - edge case)
        for i in range(25):
            landmarks = np.array([
                [0.5, 0.3 + np.random.uniform(-0.05, 0.05)],  # Nose
                [0.48, 0.32], [0.52, 0.32],
                [0.46, 0.34], [0.54, 0.34],
                [0.45, 0.4], [0.55, 0.4],
                [0.44, 0.5], [0.56, 0.5],
                [0.43, 0.6], [0.57, 0.6],
                [0.46, 0.7], [0.54, 0.7],
                [0.45, 0.8], [0.55, 0.8],
                [0.44, 0.85], [0.56, 0.85],
            ])
            test_cases.append({
                'landmarks': landmarks,
                'velocity': np.random.uniform(0.0, 0.2),
                'label': 0,  # No fall
                'description': f'Sitting person {i+1}'
            })
        
        # Bending/Crouching cases (should NOT detect fall - edge case)
        for i in range(25):
            landmarks = np.array([
                [0.5, 0.5 + np.random.uniform(-0.05, 0.05)],
                [0.48, 0.52], [0.52, 0.52],
                [0.46, 0.54], [0.54, 0.54],
                [0.45, 0.6], [0.55, 0.6],
                [0.44, 0.65], [0.56, 0.65],
                [0.43, 0.7], [0.57, 0.7],
                [0.46, 0.75], [0.54, 0.75],
                [0.45, 0.85], [0.55, 0.85],
                [0.44, 0.9], [0.56, 0.9],
            ])
            test_cases.append({
                'landmarks': landmarks,
                'velocity': np.random.uniform(0.0, 0.5),
                'label': 0,  # No fall
                'description': f'Bending/Crouching {i+1}'
            })
        
        return test_cases
    
    def run_accuracy_benchmark(self):
        """Run accuracy benchmark on test cases"""
        print("\n" + "="*70)
        print("RUNNING ACCURACY BENCHMARK")
        print("="*70)
        
        test_cases = self.generate_test_cases()
        predictions = []
        ground_truth = []
        confidences = []
        
        start_time = time.time()
        
        for i, case in enumerate(test_cases):
            is_fall, confidence, _ = self.detector.detect_fall(
                case['landmarks'], 
                case['velocity']
            )
            
            predictions.append(1 if is_fall else 0)
            ground_truth.append(case['label'])
            confidences.append(confidence)
            
            if (i + 1) % 50 == 0:
                print(f"Processed {i+1}/{len(test_cases)} test cases...")
        
        total_time = time.time() - start_time
        
        # Calculate metrics
        accuracy = accuracy_score(ground_truth, predictions)
        cm = confusion_matrix(ground_truth, predictions)
        report = classification_report(ground_truth, predictions, 
                                      target_names=['No Fall', 'Fall'],
                                      output_dict=True)
        
        # Store results
        self.results['tests'].append({
            'test_name': 'Accuracy Benchmark',
            'total_cases': len(test_cases),
            'accuracy': float(accuracy),
            'confusion_matrix': cm.tolist(),
            'classification_report': report,
            'average_confidence': float(np.mean(confidences)),
            'total_time': float(total_time),
            'avg_time_per_case': float(total_time / len(test_cases))
        })
        
        # Print results
        print("\n" + "-"*70)
        print("ACCURACY RESULTS")
        print("-"*70)
        print(f"Total Test Cases: {len(test_cases)}")
        print(f"Overall Accuracy: {accuracy*100:.2f}%")
        print(f"\nConfusion Matrix:")
        print(f"                  Predicted No Fall  Predicted Fall")
        print(f"Actual No Fall         {cm[0][0]:5d}            {cm[0][1]:5d}")
        print(f"Actual Fall            {cm[1][0]:5d}            {cm[1][1]:5d}")
        print(f"\nDetailed Metrics:")
        print(f"Precision (No Fall): {report['No Fall']['precision']*100:.2f}%")
        print(f"Recall (No Fall):    {report['No Fall']['recall']*100:.2f}%")
        print(f"F1-Score (No Fall):  {report['No Fall']['f1-score']*100:.2f}%")
        print(f"\nPrecision (Fall):    {report['Fall']['precision']*100:.2f}%")
        print(f"Recall (Fall):       {report['Fall']['recall']*100:.2f}%")
        print(f"F1-Score (Fall):     {report['Fall']['f1-score']*100:.2f}%")
        print(f"\nAverage Confidence:  {np.mean(confidences):.2f}%")
        print(f"Processing Time:     {total_time:.2f}s")
        print(f"Avg Time per Case:   {total_time/len(test_cases)*1000:.2f}ms")
        print("-"*70)
    
    def run_performance_benchmark(self):
        """Run FPS and performance benchmark"""
        print("\n" + "="*70)
        print("RUNNING PERFORMANCE BENCHMARK")
        print("="*70)
        
        # Generate test landmarks
        test_landmarks = np.array([[0.5, 0.5 + i*0.05] for i in range(17)])
        
        iterations = 1000
        times = []
        
        print(f"Running {iterations} iterations...")
        
        for i in range(iterations):
            start = time.time()
            self.detector.detect_fall(test_landmarks, 1.0)
            times.append(time.time() - start)
            
            if (i + 1) % 200 == 0:
                print(f"Completed {i+1}/{iterations} iterations...")
        
        times = np.array(times)
        avg_time = np.mean(times)
        fps = 1.0 / avg_time
        
        self.results['tests'].append({
            'test_name': 'Performance Benchmark',
            'iterations': iterations,
            'avg_time_ms': float(avg_time * 1000),
            'min_time_ms': float(np.min(times) * 1000),
            'max_time_ms': float(np.max(times) * 1000),
            'std_time_ms': float(np.std(times) * 1000),
            'fps': float(fps)
        })
        
        print("\n" + "-"*70)
        print("PERFORMANCE RESULTS")
        print("-"*70)
        print(f"Iterations:     {iterations}")
        print(f"Avg Time:       {avg_time*1000:.2f}ms")
        print(f"Min Time:       {np.min(times)*1000:.2f}ms")
        print(f"Max Time:       {np.max(times)*1000:.2f}ms")
        print(f"Std Deviation:  {np.std(times)*1000:.2f}ms")
        print(f"Estimated FPS:  {fps:.1f}")
        print("-"*70)
    
    def run_edge_case_tests(self):
        """Test edge cases and boundary conditions"""
        print("\n" + "="*70)
        print("RUNNING EDGE CASE TESTS")
        print("="*70)
        
        edge_cases = []
        
        # Test 1: Very slow movement (crawling)
        crawling = np.array([[0.2 + i*0.05, 0.5] for i in range(17)])
        is_fall, conf, _ = self.detector.detect_fall(crawling, 0.05)
        edge_cases.append({
            'case': 'Crawling (slow horizontal movement)',
            'detected_as_fall': bool(is_fall),
            'confidence': float(conf),
            'expected': False
        })
        
        # Test 2: Quick sit down
        sitting_fast = np.array([[0.5, 0.3 + i*0.02] for i in range(17)])
        is_fall, conf, _ = self.detector.detect_fall(sitting_fast, 0.8)
        edge_cases.append({
            'case': 'Quick sit down',
            'detected_as_fall': bool(is_fall),
            'confidence': float(conf),
            'expected': False
        })
        
        # Test 3: Actual fast fall
        fast_fall = np.array([[0.1 + i*0.05, 0.5] for i in range(17)])
        is_fall, conf, _ = self.detector.detect_fall(fast_fall, 2.0)
        edge_cases.append({
            'case': 'Fast fall (high velocity)',
            'detected_as_fall': bool(is_fall),
            'confidence': float(conf),
            'expected': True
        })
        
        # Test 4: Lying down slowly (intentional)
        lying_slow = np.array([[0.5 + i*0.03, 0.5] for i in range(17)])
        is_fall, conf, _ = self.detector.detect_fall(lying_slow, 0.2)
        edge_cases.append({
            'case': 'Lying down slowly (intentional)',
            'detected_as_fall': bool(is_fall),
            'confidence': float(conf),
            'expected': False
        })
        
        self.results['tests'].append({
            'test_name': 'Edge Case Tests',
            'cases': edge_cases
        })
        
        print("\n" + "-"*70)
        print("EDGE CASE RESULTS")
        print("-"*70)
        for case in edge_cases:
            status = "✓ PASS" if case['detected_as_fall'] == case['expected'] else "✗ FAIL"
            print(f"{status} | {case['case']}")
            print(f"       Detected: {case['detected_as_fall']}, Confidence: {case['confidence']:.1f}%")
        print("-"*70)
    
    def generate_summary(self):
        """Generate overall summary"""
        accuracy_test = next((t for t in self.results['tests'] 
                            if t['test_name'] == 'Accuracy Benchmark'), None)
        perf_test = next((t for t in self.results['tests'] 
                         if t['test_name'] == 'Performance Benchmark'), None)
        
        if accuracy_test:
            self.results['summary']['overall_accuracy'] = accuracy_test['accuracy']
            self.results['summary']['precision_fall'] = accuracy_test['classification_report']['Fall']['precision']
            self.results['summary']['recall_fall'] = accuracy_test['classification_report']['Fall']['recall']
            self.results['summary']['f1_score_fall'] = accuracy_test['classification_report']['Fall']['f1-score']
        
        if perf_test:
            self.results['summary']['fps'] = perf_test['fps']
            self.results['summary']['avg_processing_time_ms'] = perf_test['avg_time_ms']
    
    def save_results(self, filename='benchmark_results.json'):
        """Save results to JSON file"""
        filepath = os.path.join(os.path.dirname(__file__), filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Results saved to: {filepath}")
    
    def run_all_benchmarks(self):
        """Run all benchmarks"""
        print("\n" + "="*70)
        print("FALL DETECTION SYSTEM - COMPREHENSIVE BENCHMARK")
        print("="*70)
        
        self.run_accuracy_benchmark()
        self.run_performance_benchmark()
        self.run_edge_case_tests()
        self.generate_summary()
        
        print("\n" + "="*70)
        print("OVERALL SUMMARY")
        print("="*70)
        print(f"Overall Accuracy:      {self.results['summary'].get('overall_accuracy', 0)*100:.2f}%")
        print(f"Fall Detection Precision: {self.results['summary'].get('precision_fall', 0)*100:.2f}%")
        print(f"Fall Detection Recall:    {self.results['summary'].get('recall_fall', 0)*100:.2f}%")
        print(f"Fall Detection F1-Score:  {self.results['summary'].get('f1_score_fall', 0)*100:.2f}%")
        print(f"Processing Speed:      {self.results['summary'].get('fps', 0):.1f} FPS")
        print(f"Avg Processing Time:   {self.results['summary'].get('avg_processing_time_ms', 0):.2f}ms")
        print("="*70)
        
        self.save_results()


def main():
    """Main benchmark execution"""
    runner = BenchmarkRunner()
    runner.run_all_benchmarks()
    
    print("\n✓ Benchmark completed successfully!")
    print("Check 'benchmark_results.json' for detailed results.")


if __name__ == '__main__':
    main()
