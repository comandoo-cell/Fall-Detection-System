"""
Enhanced Error Handling Module
Provides comprehensive logging and error management
"""

import logging
import traceback
from datetime import datetime
from pathlib import Path
from typing import Optional
import sys


class ErrorHandler:
    """Centralized error handling and logging"""
    
    def __init__(self, log_dir: str = "logs"):
        """Initialize error handler with logging"""
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Setup logging
        log_file = self.log_dir / f"fall_detection_{datetime.now().strftime('%Y%m%d')}.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger('FallDetectionSystem')
    
    def log_info(self, message: str):
        """Log informational message"""
        self.logger.info(message)
    
    def log_warning(self, message: str):
        """Log warning message"""
        self.logger.warning(message)
    
    def log_error(self, message: str, exception: Optional[Exception] = None):
        """Log error with optional exception details"""
        self.logger.error(message)
        if exception:
            self.logger.error(f"Exception: {str(exception)}")
            self.logger.error(f"Traceback: {traceback.format_exc()}")
    
    def log_critical(self, message: str, exception: Optional[Exception] = None):
        """Log critical error"""
        self.logger.critical(message)
        if exception:
            self.logger.critical(f"Exception: {str(exception)}")
            self.logger.critical(f"Traceback: {traceback.format_exc()}")
    
    @staticmethod
    def handle_camera_error() -> str:
        """Handle camera connection errors"""
        return """
        ⚠️ Kamera Hatası Tespit Edildi
        
        Olası Çözümler:
        1. Kamera bağlantısını kontrol edin
        2. Başka bir uygulama kamerayı kullanıyor olabilir - kapatın
        3. Kamera sürücülerini güncelleyin
        4. Bilgisayarı yeniden başlatın
        5. Farklı bir video kaynağı deneyin
        """
    
    @staticmethod
    def handle_model_load_error(model_name: str) -> str:
        """Handle model loading errors"""
        return f"""
        ⚠️ Model Yükleme Hatası: {model_name}
        
        Olası Çözümler:
        1. Model dosyasının mevcut olduğundan emin olun
        2. Gerekli kütüphanelerin yüklendiğini kontrol edin
        3. requirements.txt dosyasından tüm bağımlılıkları yükleyin
        4. Disk alanını kontrol edin
        """
    
    @staticmethod
    def handle_processing_error() -> str:
        """Handle frame processing errors"""
        return """
        ⚠️ İşleme Hatası
        
        Sistem bir sonraki kareyi işlemeye devam edecek.
        Sorun devam ederse lütfen uygulamayı yeniden başlatın.
        """
    
    @staticmethod
    def handle_low_light_warning() -> str:
        """Handle low light conditions"""
        return """
        ⚠️ Düşük Işık Algılandı
        
        Tespit doğruluğu düşük ışıkta azalabilir.
        Daha iyi sonuçlar için ışığı artırın.
        """
    
    @staticmethod
    def handle_no_person_detected() -> str:
        """Handle no person in frame"""
        return """
        ℹ️ Kişi Tespit Edilmedi
        
        Kameranın görüş alanında kişi bulunmuyor.
        """


# Global error handler instance
error_handler = ErrorHandler()
