# Project Structure Documentation

## 📁 Complete Directory Structure

```
all-detection-system/
│
├── .github/                          # GitHub configuration
│   └── workflows/                    # CI/CD pipelines
│       ├── tests.yml                 # Automated testing
│       └── code_quality.yml          # Code quality checks
│
├── src/                              # Source code
│   ├── core/                         # Core detection algorithms
│   │   ├── __init__.py
│   │   └── fall_detector.py          # Main fall detection logic
│   │
│   ├── models/                       # ML models management
│   │   ├── __init__.py
│   │   ├── pose_estimator.py         # MediaPipe pose detection
│   │   └── multi_person_detector.py  # YOLOv8 multi-person detection
│   │
│   ├── utils/                        # Utility modules
│   │   ├── __init__.py
│   │   ├── error_handler.py          # Error handling & logging
│   │   ├── video_processor.py        # Video processing utilities
│   │   └── video_url_handler.py      # URL video handling
│   │
│   └── ui/                           # User interface
│       ├── __init__.py
│       └── streamlit_app.py          # Streamlit web interface
│
├── tests/                            # Unit tests
│   ├── __init__.py
│   ├── test_fall_detector.py         # Fall detector tests
│   ├── test_pose_estimator.py        # Pose estimation tests
│   └── test_integration.py           # Integration tests
│
├── benchmarks/                       # Performance benchmarks
│   ├── run_benchmarks.py             # Benchmark runner
│   ├── benchmark_results.json        # Results output
│   └── README.md                     # Benchmark documentation
│
├── examples/                         # Examples and demos
│   ├── README.md                     # Examples documentation
│   ├── RESULTS.md                    # Expected results
│   ├── screenshots/                  # UI screenshots
│   ├── results/                      # Sample test results
│   └── usage_examples/               # Code examples
│
├── docs/                             # Documentation
│   ├── API.md                        # API documentation
│   ├── ARCHITECTURE.md               # System architecture
│   ├── DEPLOYMENT.md                 # Deployment guide
│   └── FAQ.md                        # Frequently asked questions
│
├── configs/                          # Configuration files
│   ├── default_config.yaml           # Default configuration
│   └── production_config.yaml        # Production settings
│
├── logs/                             # Log files (git ignored)
│   └── fall_detection_YYYYMMDD.log   # Daily log files
│
├── models/                           # Pre-trained models
│   └── yolov8n-pose.pt               # YOLOv8 Nano Pose model
│
├── app_fast.py                       # Main application entry point
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
├── LICENSE                           # MIT License
├── README.md                         # Main documentation (Turkish)
├── README_ACADEMIC.md                # Academic documentation (Turkish)
├── CONTRIBUTING.md                   # Contribution guidelines
└── CHANGELOG.md                      # Version history
```

## 📦 Module Organization

### Core Modules (`src/core/`)
**Purpose**: Core fall detection algorithms
- `fall_detector.py`: Main fall detection logic
  - Multi-criteria analysis
  - Confidence scoring
  - History tracking

### Models (`src/models/`)
**Purpose**: Machine learning model integrations
- `pose_estimator.py`: MediaPipe wrapper
  - Single-person pose detection
  - 35+ FPS performance
  - 33 body landmarks

- `multi_person_detector.py`: YOLOv8 wrapper
  - Multi-person tracking
  - 20+ FPS performance
  - Bounding box detection

### Utilities (`src/utils/`)
**Purpose**: Helper functions and utilities
- `error_handler.py`: Centralized error handling
  - Logging system
  - Error recovery
  - User-friendly messages

- `video_processor.py`: Video processing
  - Frame validation
  - Quality checks
  - Error recovery

- `video_url_handler.py`: URL video support
  - YouTube/URL processing
  - Stream handling

### UI (`src/ui/`)
**Purpose**: User interface components
- `streamlit_app.py`: Web interface
  - Real-time display
  - Controls and settings
  - Statistics dashboard

## 🔧 Configuration Management

### Configuration Files
- `default_config.yaml`: Development settings
- `production_config.yaml`: Production settings

### Configuration Structure
```yaml
detection:
  angle_threshold: 60.0
  confidence_threshold: 60.0
  velocity_threshold: 0.5

performance:
  max_fps: 30
  buffer_size: 1
  use_gpu: false

logging:
  level: INFO
  directory: logs/
  max_files: 30
```

## 🧪 Testing Structure

### Unit Tests (`tests/`)
- **test_fall_detector.py**: Core algorithm tests
  - Angle calculation
  - Aspect ratio
  - Fall detection logic
  
- **test_pose_estimator.py**: Model integration tests
  - MediaPipe functionality
  - YOLOv8 functionality
  - Error handling

### Benchmarks (`benchmarks/`)
- **run_benchmarks.py**: Performance benchmarking
  - Accuracy metrics
  - Speed benchmarks
  - Edge case testing

## 📊 Output Structure

### Logs (`logs/`)
```
logs/
└── fall_detection_20251217.log
```

### Results (`examples/results/`)
```
results/
├── benchmark_results.json
├── confusion_matrix.png
└── performance_graph.png
```

## 🚀 Entry Points

### Main Application
```bash
streamlit run app_fast.py
```

### Tests
```bash
python -m pytest tests/ -v
```

### Benchmarks
```bash
python benchmarks/run_benchmarks.py
```

## 🔄 Data Flow

```
User Input → Video Source
    ↓
Video Processor (validation, error handling)
    ↓
Pose Detection (MediaPipe/YOLOv8)
    ↓
Fall Detector (multi-criteria analysis)
    ↓
UI Display + Logging
```

## 📝 File Naming Conventions

- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case()`
- **Constants**: `UPPER_SNAKE_CASE`
- **Tests**: `test_*.py`
- **Configs**: `*_config.yaml`

## 🎯 Best Practices

1. **Modularity**: Each file has a single responsibility
2. **Error Handling**: Comprehensive try-catch blocks
3. **Logging**: All important events logged
4. **Testing**: Unit tests for all core functions
5. **Documentation**: Docstrings for all public functions
6. **Type Hints**: Type annotations where applicable

## 🔐 Security

- Sensitive data not committed (`.gitignore`)
- Logs excluded from repository
- Configuration files validated
- Input sanitization implemented

## 📚 Related Documentation

- [README.md](../README.md) - Main documentation
- [README_ACADEMIC.md](../README_ACADEMIC.md) - Academic details
- [CONTRIBUTING.md](../CONTRIBUTING.md) - How to contribute
- [API.md](API.md) - API documentation
