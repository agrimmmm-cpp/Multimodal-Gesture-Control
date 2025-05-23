# 🎯 FaceUI++: Multimodal Gesture-Controlled UI System

**Author**: *Agrim Joshi*  
**Description**: A real-time computer vision-based interface using **facial and hand gestures** to control mouse actions, volume, media playback, and tab navigation.  
**Technologies**: `Python`, `OpenCV`, `MediaPipe`, `PyAutoGUI`, `osascript (macOS)`

---

## 🚀 Features

### 👁️ Eye Blink Detection
- **Left Eye Blink** ➜ Left Click  
- **Right Eye Blink** ➜ Right Click  

### 🤏 Hand Gesture Control (Right Hand)
- **Index + Thumb Pinch** ➜ Scroll Down  
- **Middle + Thumb Pinch** ➜ Scroll Up  
- **Ring + Thumb Pinch** ➜ Close Active Tab (`Cmd + W`)  

### ✋ Hand Gesture Control (Left Hand)
- **Thumbs Up** ➜ Increase Volume  
- **Thumbs Down** ➜ Decrease Volume  
- **Index + Thumb Pinch** ➜ Play/Pause Music  

### 🖱️ Cursor Control
- **Right Hand Index Finger** ➜ Move Cursor across the screen  

---

## 🛠️ Dependencies

Install using pip:

```bash
pip install opencv-python mediapipe pyautogui numpy
```

For macOS volume & music control:  
> Uses `osascript` (pre-installed on macOS)

---

## 📦 How to Run

```bash
python GestureControl.py
```

---

## 💡 Notes

- Works best in **good lighting conditions**.
- Currently designed for **macOS** — system command modules (like `osascript`) must be replaced for **Windows/Linux**.
- Tune parameters like `frame_skip`, `blink_threshold`, and `pinch_threshold` for best results.

---

## 📁 Files

- `GestureControl.py` — Main script with gesture logic

---

## 📸 Demo

> [Youtube Link](https://youtu.be/_HzGsyczCgc)
