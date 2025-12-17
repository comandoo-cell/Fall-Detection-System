"""
Enhanced Video Processing Module with Error Handling
Handles camera issues, lighting problems, and frame processing errors
"""

import cv2
import numpy as np
from typing import Optional, Tuple
from src.error_handler import error_handler


class VideoProcessor:
    """Enhanced video processing with robust error handling"""
    
    def __init__(self):
        """Initialize video processor"""
        self.frame_count = 0
        self.error_count = 0
        self.max_consecutive_errors = 10
        self.last_valid_frame = None
    
    def check_camera_available(self, camera_id: int = 0) -> Tuple[bool, Optional[str]]:
        """Check if camera is available"""
        try:
            cap = cv2.VideoCapture(camera_id)
            if not cap.isOpened():
                error_handler.log_error(f"Camera {camera_id} not accessible")
                return False, error_handler.handle_camera_error()
            
            ret, frame = cap.read()
            cap.release()
            
            if not ret or frame is None:
                error_handler.log_error(f"Camera {camera_id} cannot read frames")
                return False, error_handler.handle_camera_error()
            
            error_handler.log_info(f"Camera {camera_id} is available")
            return True, None
            
        except Exception as e:
            error_handler.log_error(f"Camera check failed: {str(e)}", e)
            return False, error_handler.handle_camera_error()
    
    def validate_frame(self, frame: np.ndarray) -> Tuple[bool, Optional[str]]:
        """Validate frame quality and content"""
        if frame is None:
            return False, "Frame is None"
        
        if len(frame.shape) != 3:
            return False, "Invalid frame dimensions"
        
        if frame.shape[2] != 3:
            return False, "Frame must be RGB/BGR"
        
        # Check for very dark frames (low light)
        mean_brightness = np.mean(frame)
        if mean_brightness < 30:
            error_handler.log_warning("Low light detected")
            return True, error_handler.handle_low_light_warning()
        
        # Check for blank/corrupted frames
        if np.std(frame) < 5:
            return False, "Frame appears blank or corrupted"
        
        return True, None
    
    def process_frame_safe(self, frame: np.ndarray, 
                          processor_func, 
                          *args, **kwargs) -> Tuple[bool, any, Optional[str]]:
        """Safely process frame with error handling"""
        try:
            # Validate frame first
            is_valid, error_msg = self.validate_frame(frame)
            if not is_valid:
                self.error_count += 1
                if self.error_count > self.max_consecutive_errors:
                    error_handler.log_critical("Too many consecutive frame errors")
                    return False, None, "Çok fazla ardışık hata. Lütfen yeniden başlatın."
                return False, None, error_msg
            
            # Process frame
            result = processor_func(frame, *args, **kwargs)
            
            # Reset error count on success
            self.error_count = 0
            self.frame_count += 1
            self.last_valid_frame = frame.copy()
            
            return True, result, None
            
        except cv2.error as e:
            error_handler.log_error(f"OpenCV error in frame processing: {str(e)}", e)
            self.error_count += 1
            return False, None, error_handler.handle_processing_error()
            
        except Exception as e:
            error_handler.log_error(f"Unexpected error in frame processing: {str(e)}", e)
            self.error_count += 1
            return False, None, error_handler.handle_processing_error()
    
    def get_last_valid_frame(self) -> Optional[np.ndarray]:
        """Get last successfully processed frame"""
        return self.last_valid_frame
    
    def reset_error_count(self):
        """Reset error counter"""
        self.error_count = 0
        error_handler.log_info("Error count reset")
    
    def get_stats(self) -> dict:
        """Get processing statistics"""
        return {
            'total_frames': self.frame_count,
            'error_count': self.error_count,
            'success_rate': ((self.frame_count - self.error_count) / max(self.frame_count, 1)) * 100
        }


class CameraManager:
    """Manages camera connections with error recovery"""
    
    def __init__(self, camera_id: int = 0):
        """Initialize camera manager"""
        self.camera_id = camera_id
        self.cap = None
        self.is_opened = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 3
    
    def open(self) -> Tuple[bool, Optional[str]]:
        """Open camera with error handling"""
        try:
            self.cap = cv2.VideoCapture(self.camera_id)
            
            if not self.cap.isOpened():
                error_handler.log_error(f"Failed to open camera {self.camera_id}")
                return False, error_handler.handle_camera_error()
            
            # Set camera properties for better performance
            self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.cap.set(cv2.CAP_PROP_FPS, 30)
            
            self.is_opened = True
            self.reconnect_attempts = 0
            error_handler.log_info(f"Camera {self.camera_id} opened successfully")
            return True, None
            
        except Exception as e:
            error_handler.log_error(f"Camera open failed: {str(e)}", e)
            return False, error_handler.handle_camera_error()
    
    def read(self) -> Tuple[bool, Optional[np.ndarray], Optional[str]]:
        """Read frame with error handling and auto-reconnect"""
        if not self.is_opened or self.cap is None:
            return False, None, "Kamera açık değil"
        
        try:
            ret, frame = self.cap.read()
            
            if not ret or frame is None:
                error_handler.log_warning("Failed to read frame, attempting reconnect")
                
                if self.reconnect_attempts < self.max_reconnect_attempts:
                    self.reconnect_attempts += 1
                    self.release()
                    success, error_msg = self.open()
                    if success:
                        return self.read()
                
                return False, None, error_handler.handle_camera_error()
            
            return True, frame, None
            
        except Exception as e:
            error_handler.log_error(f"Frame read error: {str(e)}", e)
            return False, None, error_handler.handle_processing_error()
    
    def release(self):
        """Release camera resources"""
        try:
            if self.cap is not None:
                self.cap.release()
                self.is_opened = False
                error_handler.log_info(f"Camera {self.camera_id} released")
        except Exception as e:
            error_handler.log_error(f"Camera release error: {str(e)}", e)
    
    def __del__(self):
        """Cleanup on deletion"""
        self.release()
