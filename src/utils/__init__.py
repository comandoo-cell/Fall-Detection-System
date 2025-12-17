"""
Utilities Module
================

This module contains utility functions for error handling,
video processing, and other helper functions.
"""

from .error_handler import ErrorHandler, error_handler
from .video_processor import VideoProcessor, CameraManager

__all__ = [
    'ErrorHandler',
    'error_handler',
    'VideoProcessor',
    'CameraManager'
]
