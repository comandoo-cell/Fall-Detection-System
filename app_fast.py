import streamlit as st
import cv2
import numpy as np
import sys
import tempfile
import time
import os
import winsound
from pathlib import Path
from datetime import datetime
from typing import Optional
from collections import deque
sys.path.insert(0, str(Path(__file__).parent / 'src'))
from pose_estimator import PoseEstimator
from multi_person_detector import MultiPersonDetector
from fall_detector import FallDetector
from video_url_handler import VideoURLHandler
st.set_page_config(
    page_title="Dusme Tespit Sistemi",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        background-color: #1a1a1a;
        color: white;
    }
    .stApp {
        background-color: #1a1a1a;
    }
    [data-testid="stSidebar"] {
        background-color: #1a1a1a;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: white !important;
    }
    .stMarkdown {
        color: white !important;
    }
    .main-title {
        text-align: center;
        color: white;
        padding: 20px 0;
        margin-bottom: 30px;
    }
    .main-title h1 {
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 10px;
        color: white !important;
    }
    .main-title h3 {
        font-size: 24px;
        font-weight: normal;
        color: #cccccc !important;
    }
    .status-safe {
        background: linear-gradient(135deg, #4caf50, #45a049);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .status-danger {
        background: linear-gradient(135deg, #f44336, #da190b);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        animation: pulse 1s infinite;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    .stat-box {
        background-color: #2d2d2d;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .stat-number {
        font-size: 36px;
        font-weight: bold;
        color: #a5d6a7 !important;
    }
    .stat-label {
        font-size: 14px;
        color: #cccccc !important;
        margin-top: 5px;
    }
    .event-log {
        background: #2d2d2d;
        padding: 10px;
        margin: 5px 0;
        border-left: 3px solid #f44336;
        border-radius: 5px;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
    <h1>Dusme Tespit Sistemi</h1>
    <h3>Fall Detection System</h3>
</div>
""", unsafe_allow_html=True)

if 'fall_count' not in st.session_state:
    st.session_state.fall_count = 0
if 'fall_events' not in st.session_state:
    st.session_state.fall_events = []
if 'people_count' not in st.session_state:
    st.session_state.people_count = 0
if 'confidence_score' not in st.session_state:
    st.session_state.confidence_score = 0
if 'video_source' not in st.session_state:
    st.session_state.video_source = None
if 'current_status' not in st.session_state:
    st.session_state.current_status = 'safe'
if 'enable_sound' not in st.session_state:
    st.session_state.enable_sound = True
if 'enable_screenshot' not in st.session_state:
    st.session_state.enable_screenshot = True
if 'screenshot_taken' not in st.session_state:
    st.session_state.screenshot_taken = set()

screenshots_dir = Path("fall_screenshots")
screenshots_dir.mkdir(exist_ok=True)

@st.cache_resource
def load_yolo_model():
    return MultiPersonDetector()

@st.cache_resource
def load_mediapipe_model():
    return PoseEstimator()

def play_alert_sound():
    try:
        winsound.Beep(1000, 500)
    except:
        pass

def save_fall_screenshot(frame, person_id=None):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if person_id is not None:
            filename = f"fall_person{person_id}_{timestamp}.jpg"
        else:
            filename = f"fall_{timestamp}.jpg"
        filepath = screenshots_dir / filename
        cv2.imwrite(str(filepath), frame)
        return str(filepath)
    except Exception as e:
        print(f"Screenshot error: {e}")
        return None

with st.sidebar:
    st.header("⚙ Ayarlar")
    model_choice = st.radio(
        "Model:",
        ["MediaPipe (Hizli)", "YOLOv8 (Coklu Kisi)"],
        help="MediaPipe: Daha hizli | YOLOv8: Daha dogru"
    )
    use_yolo = "YOLOv8" in model_choice
    st.markdown("---")
    input_mode = st.selectbox(
        "Video Kaynagi:",
        ["📷 Kamera", "📁 Dosya", "🌐 URL"]
    )
    if "Kamera" in input_mode:
        camera_index = st.number_input("Kamera No:", 0, 5, 0)
        st.session_state.video_source = camera_index
    elif "Dosya" in input_mode:
        uploaded_file = st.file_uploader(
            "Video sec:",
            type=['mp4', 'avi', 'mov', 'mkv']
        )
        if uploaded_file:
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
            tfile.write(uploaded_file.read())
            tfile.close()
            st.session_state.video_source = tfile.name
            st.success(f"Video yuklendi: {uploaded_file.name}")
    elif "URL" in input_mode:
        url_input = st.text_input("URL:", placeholder="https://youtube.com/... or rtsp://...")
        if st.button("Yukle", disabled=not url_input):
            with st.spinner("Yukleniyor..."):
                try:
                    url_handler = VideoURLHandler()
                    processed_url, url_type = url_handler.process_url(url_input)
                    if processed_url:
                        st.session_state.video_source = processed_url
                        if url_type == 'youtube':
                            st.success(f"✅ YouTube yuklendi!")
                        elif url_type == 'ip_camera':
                            st.success(f"✅ IP kamera baglandi!")
                        else:
                            st.success(f"✅ Yuklendi: {url_type}")
                    else:
                        if url_type == 'youtube_error':
                            st.error("❌ YouTube yuklenmedi! Lutfen baglanti kontrol edin.")
                        elif url_type == 'unknown':
                            st.error("❌ Desteklenmeyen URL turu!")
                        else:
                            st.error("❌ Yuklenemedi! Lutfen URL kontrol edin.")
                except Exception as e:
                    st.error(f"❌ Hata: {str(e)}")
                    st.info("💡 YouTube videolari icin gecerli bir link girin veya IP kamera URL (rtsp://...)")
    st.markdown("---")
    st.subheader("🎯 Tespit Ayarlari")
    angle_threshold = st.slider("Aci Esigi:", 30, 90, 60, help="Vucut egim acisi esigi (derece)")
    st.markdown("---")
    st.subheader("🔔 Uyari Ayarlari")
    st.session_state.enable_sound = st.checkbox("Ses Uyarisi", value=True, help="Dusme tespit edildiginde ses calar")
    st.session_state.enable_screenshot = st.checkbox("Otomatik Ekran Goruntusu", value=True, help="Dusme aninda fotograf kaydeder")
    st.markdown("---")
    resize_width = st.select_slider(
        "Video Genisligi:",
        options=[480, 640, 960],
        value=640,
        help="640 = Dengeli kalite ve hiz | 960 = Yuksek kalite"
    )
    skip_frames = st.slider(
        "Kare Atlama (Her X kare):",
        1, 5, 3,
        help="3 = Cok hizli! (Yuklu videolar icin onerilen)"
    )
    st.markdown("---")
    show_skeleton = st.checkbox("Iskelet Goster", True)
    show_bbox = st.checkbox("Cerceve Goster", True)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        start_btn = st.button("▶ START", use_container_width=True, type="primary")
    with col2:
        if st.button("⏹ STOP", use_container_width=True):
            st.session_state.stop_processing = True
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.fall_events.clear()
        st.session_state.fall_count = 0
        st.session_state.people_count = 0
        st.rerun()
col1, col2, col3 = st.columns(3)
with col1:
    if st.session_state.current_status == 'safe':
        st.markdown('<div class="status-safe">GUVENLI</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-danger">DUSME!</div>', unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div class="stat-box">
        <div class="stat-number">{st.session_state.fall_count}</div>
        <div class="stat-label">Toplam Dusme</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="stat-box">
        <div class="stat-label">Guven Skoru</div>
    </div>
    """, unsafe_allow_html=True)
    
    confidence_color = "red" if st.session_state.confidence_score >= 60 else "green"
    st.progress(st.session_state.confidence_score / 100)
    st.markdown(f"**<span style='color:{confidence_color}; font-size:20px;'>{st.session_state.confidence_score:.1f}%</span>**", unsafe_allow_html=True)

screenshot_count = len(list(screenshots_dir.glob("*.jpg")))
if screenshot_count > 0:
    st.info(f"📸 {screenshot_count} adet ekran goruntusu kaydedildi (fall_screenshots klasorunde)")
st.markdown("---")
video_placeholder = st.empty()
fps_placeholder = st.empty()
with st.expander("📋 Olay Kayitlari", expanded=False):
    event_log_placeholder = st.empty()
def process_video_optimized():
    if st.session_state.video_source is None:
        st.warning("⚠ Video kaynagi secin!")
        return
    try:
        cap = cv2.VideoCapture(st.session_state.video_source)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
        if not cap.isOpened():
            st.error("❌ Video acilamadi! Lutfen baska bir dosya deneyin.")
            return
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_fps = int(cap.get(cv2.CAP_PROP_FPS))
        st.info(f"📹 Video: {total_frames} kare, {video_fps} FPS")
        with st.spinner("Model yukleniyor..."):
            if use_yolo:
                detector = load_yolo_model()
            else:
                detector = load_mediapipe_model()
        st.success("✅ Model yuklendi!")
        fall_detectors = {}
        frame_count = 0
        fps_start = time.time()
        fps = 0
        prev_processed_frame = None
        frame_buffer = deque(maxlen=2)
        st.session_state.stop_processing = False
        while not st.session_state.stop_processing:
            ret, frame = cap.read()
            if not ret:
                break
            frame_count += 1
            h, w = frame.shape[:2]
            new_height = int(h * (resize_width / w))
            frame = cv2.resize(frame, (resize_width, new_height))
            if frame_count % skip_frames != 0:
                if prev_processed_frame is not None:
                    video_placeholder.image(prev_processed_frame, channels="RGB", use_column_width=True)
                continue
            fall_detected = False
            if use_yolo:
                people = detector.detect_people(frame)
                st.session_state.people_count = len(people)
                for person_id, person in enumerate(people):
                    if person_id not in fall_detectors:
                        fall_detectors[person_id] = FallDetector(
                            angle_threshold=angle_threshold
                        )
                    keypoints = person['keypoints']
                    is_fallen = fall_detectors[person_id].detect_fall(keypoints)
                    confidence = fall_detectors[person_id].get_confidence_score()
                    if confidence > st.session_state.confidence_score:
                        st.session_state.confidence_score = confidence
                    if is_fallen:
                        fall_detected = True
                        event = f"{datetime.now().strftime('%H:%M:%S')} - Kisi {person_id+1} ({confidence:.0f}%)"
                        if event not in st.session_state.fall_events:
                            st.session_state.fall_events.append(event)
                            st.session_state.fall_count += 1
                            if st.session_state.enable_sound:
                                play_alert_sound()
                            person_key = f"yolo_{person_id}"
                            if st.session_state.enable_screenshot and person_key not in st.session_state.screenshot_taken:
                                saved_path = save_fall_screenshot(frame, person_id+1)
                                if saved_path:
                                    st.session_state.screenshot_taken.add(person_key)
                                    print(f"Ekran goruntusu kaydedildi: {saved_path}")
                    else:
                        person_key = f"yolo_{person_id}"
                        if person_key in st.session_state.screenshot_taken:
                            st.session_state.screenshot_taken.discard(person_key)
                    if show_bbox and person['bbox']:
                        x1, y1, x2, y2 = person['bbox']
                        color = (0, 0, 255) if is_fallen else (0, 255, 0)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
                        status = f"DUSME! {confidence:.0f}%" if is_fallen else f"Normal {confidence:.0f}%"
                        cv2.putText(frame, f"Kisi {person_id+1}: {status}",
                                   (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX,
                                   0.5, color, 2)
                    if show_skeleton:
                        important_points = ['nose', 'left_shoulder', 'right_shoulder', 
                                          'left_hip', 'right_hip', 'left_ankle', 'right_ankle']
                        color = (0, 0, 255) if is_fallen else (0, 255, 0)
                        for name in important_points:
                            if name in keypoints:
                                x, y = keypoints[name]
                                cv2.circle(frame, (x, y), 4, color, -1)
                        connections = [
                            ('left_shoulder', 'right_shoulder'),
                            ('left_shoulder', 'left_hip'),
                            ('right_shoulder', 'right_hip'),
                            ('left_hip', 'right_hip'),
                            ('left_hip', 'left_ankle'),
                            ('right_hip', 'right_ankle')
                        ]
                        for p1, p2 in connections:
                            if p1 in keypoints and p2 in keypoints:
                                cv2.line(frame, keypoints[p1], keypoints[p2], color, 2)
            else:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                person_detected = detector.process_frame(rgb_frame)
                if person_detected:
                    st.session_state.people_count = 1
                    h, w = frame.shape[:2]
                    keypoints = detector.get_all_keypoints(w, h)
                    if 0 not in fall_detectors:
                        fall_detectors[0] = FallDetector(
                            angle_threshold=angle_threshold
                        )
                    is_fallen = fall_detectors[0].detect_fall(keypoints)
                    confidence = fall_detectors[0].get_confidence_score()
                    st.session_state.confidence_score = confidence
                    if is_fallen:
                        fall_detected = True
                        event = f"{datetime.now().strftime('%H:%M:%S')} - Dusme! ({confidence:.0f}%)"
                        if event not in st.session_state.fall_events:
                            st.session_state.fall_events.append(event)
                            st.session_state.fall_count += 1
                            if st.session_state.enable_sound:
                                play_alert_sound()
                            person_key = "mediapipe_0"
                            if st.session_state.enable_screenshot and person_key not in st.session_state.screenshot_taken:
                                saved_path = save_fall_screenshot(frame)
                                if saved_path:
                                    st.session_state.screenshot_taken.add(person_key)
                                    print(f"Ekran goruntusu kaydedildi: {saved_path}")
                    else:
                        person_key = "mediapipe_0"
                        if person_key in st.session_state.screenshot_taken:
                            st.session_state.screenshot_taken.discard(person_key)
                    if show_skeleton:
                        frame = detector.draw_skeleton(frame)
                else:
                    st.session_state.people_count = 0
            st.session_state.current_status = 'danger' if fall_detected else 'safe'
            if fall_detected:
                cv2.rectangle(frame, (0, 0), (frame.shape[1], frame.shape[0]),
                             (0, 0, 255), 10)
            if frame_count % 30 == 0:
                fps = 30 / (time.time() - fps_start)
                fps_start = time.time()
            cv2.putText(frame, f"FPS: {int(fps)}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            prev_processed_frame = frame_rgb
            frame_buffer.append(frame_rgb)
            if len(frame_buffer) > 0:
                display_frame = frame_buffer[0]
                video_placeholder.image(display_frame, channels="RGB", use_column_width=True)
            if frame_count % 30 == 0:
                fps_placeholder.text(f"⚡ {int(fps)} FPS | Speed: {skip_frames}x")
            if frame_count % 20 == 0 and st.session_state.fall_events:
                events_html = "<br>".join([f'<div class="event-log">{event}</div>' 
                                          for event in list(st.session_state.fall_events)[-10:]])
                event_log_placeholder.markdown(events_html, unsafe_allow_html=True)
        cap.release()
        st.success("✅ Video isleme tamamlandi")
    except Exception as e:
        st.error(f"❌ Hata: {str(e)}")
if start_btn:
    process_video_optimized()
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: white; padding: 20px;'>
    <p>© 2025 Developed by [Your Name] | Dusme Tespit Sistemi</p>
</div>
""", unsafe_allow_html=True)