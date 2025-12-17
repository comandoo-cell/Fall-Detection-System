"""
Video URL Handler Module
========================"""

import yt_dlp
import cv2
import tempfile
import os
from typing import Optional, Tuple


class VideoURLHandler:
    """Video URL Handler"""
    
    def __init__(self):
        """Initialize handler"""
        self.temp_file = None
        
    def is_youtube_url(self, url: str) -> bool:
        """Check if URL is from YouTube"""
        youtube_domains = ['youtube.com', 'youtu.be', 'youtube-nocookie.com']
        return any(domain in url.lower() for domain in youtube_domains)
    
    def is_ip_camera_url(self, url: str) -> bool:
        """Check if URL is an IP camera"""
        ip_camera_protocols = ['rtsp://', 'rtmp://', 'http://', 'https://']
        return any(url.lower().startswith(protocol) for protocol in ip_camera_protocols) \
               and not self.is_youtube_url(url)
    
    def download_youtube_video(self, url: str, max_resolution: int = 720) -> Optional[str]:
        """Download YouTube video"""
        try:
            temp_dir = tempfile.gettempdir()
            output_template = os.path.join(temp_dir, 'fall_detection_%(id)s.%(ext)s')
            
            ydl_opts = {
                'format': f'best[height<={max_resolution}][ext=mp4]/best[ext=mp4]/best',
                'outtmpl': output_template,
                'quiet': True,
                'no_warnings': True,
                'extract_flat': False,
                'ignoreerrors': False,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Video indiriliyor: {url}")
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                if os.path.exists(filename):
                    self.temp_file = filename
                    print(f"Basariyla indirildi: {filename}")
                    return filename
                else:
                    print(f"Dosya indirmeden sonra bulunamadi: {filename}")
                    return None
                
        except Exception as e:
            print(f"YouTube video indirme hatasi: {e}")
            import traceback
            traceback.print_exc()
            return None
                
        except Exception as e:
            print(f"YouTube video indirme hatasi: {e}")
            return None
    
    def get_ip_camera_stream(self, url: str) -> Optional[cv2.VideoCapture]:
        """Open IP camera stream"""
        try:
            cap = cv2.VideoCapture(url)
            
            if cap.isOpened():
                return cap
            else:
                print(f"Kamera akisi acilamadi: {url}")
                return None
                
        except Exception as e:
            print(f"Kamera akisi acma hatasi: {e}")
            return None
    
    def process_url(self, url: str) -> Tuple[Optional[str], str]:
        """Process URL and return appropriate source"""
        url = url.strip()
        
        if self.is_youtube_url(url):
            print("YouTube videosu indiriliyor...")
            video_path = self.download_youtube_video(url)
            if video_path:
                return video_path, 'youtube'
            else:
                return None, 'youtube_error'
        
        elif self.is_ip_camera_url(url):
            print("IP kameraya baglaniliyor...")
            return url, 'ip_camera'
        
        else:
            print("Desteklenmeyen URL turu")
            return None, 'unknown'
    
    def cleanup(self):
        """Cleanup temporary files"""
        if self.temp_file and os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
                print(f"Gecici dosya silindi: {self.temp_file}")
            except Exception as e:
                print(f"Gecici dosya silme hatasi: {e}")
            finally:
                self.temp_file = None

