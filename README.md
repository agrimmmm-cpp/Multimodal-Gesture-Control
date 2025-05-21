# Multimodal-Gesture-Control


# =====================================================
# 🎯 FaceUI++: Multimodal Gesture-Controlled UI System
# =====================================================
# Author        : Agrim Joshi
# Description   : A real-time computer vision-based interface using 
#                 facial and hand gestures to control mouse actions, 
#                 volume, media playback, and tab navigation.
# Technologies  : Python, OpenCV, MediaPipe, PyAutoGUI, osascript (macOS)
#
# -------------------
# ✅ FEATURES
# -------------------
# 👁️  EYE BLINK DETECTION
#     - Left Eye Blink  ➜ Left Click
#     - Right Eye Blink ➜ Right Click
#
# 🤏 HAND GESTURE CONTROL (Right Hand)
#     - Index + Thumb Pinch    ➜ Scroll Down
#     - Middle + Thumb Pinch   ➜ Scroll Up
#     - Ring + Thumb Pinch     ➜ Close Active Tab (Cmd + W)
#
# ✋ HAND GESTURE CONTROL (Left Hand)
#     - Thumbs Up    ➜ Increase Volume
#     - Thumbs Down  ➜ Decrease Volume
#     - Index + Thumb Pinch ➜ Play/Pause Music
#
# 🖱️ CURSOR CONTROL
#     - Right Hand Index Finger moves cursor across the screen
#
# -------------------
# 🛠️ DEPENDENCIES
# -------------------
# Install using pip:
#   pip install opencv-python mediapipe pyautogui numpy
#
# For macOS volume & music control:
#   Uses: osascript (pre-installed on macOS)
#
# -------------------
# 📦 HOW TO RUN
# -------------------
# python GestureControl.py
#
# -------------------
# 💡 NOTES
# -------------------
# - Works best in good lighting conditions.
# - macOS-specific; modify for Windows/Linux system commands.
# - Adjust 'frame_skip', 'blink_threshold', and other params for tuning.
#
# -------------------
# 📁 FILES
# -------------------
# - GestureControl.py      # Main script with gesture logic
#
# -------------------
# 📸 DEMO
# -------------------
# [Insert demo GIF or YouTube link here]
#
# -------------------
# 📄 LICENSE
# -------------------
# [Insert license if any, e.g., MIT]
