# --- Imports ---
import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time
import math
import osascript
import threading

# --- MacOS Volume and Playback Controls ---
def increase_volume():
    osascript.osascript("set volume output volume ((output volume of (get volume settings)) + 10) --100%")

def decrease_volume():
    osascript.osascript("set volume output volume ((output volume of (get volume settings)) - 10) --100%")

def playPause():
    osascript.osascript('tell application "Music" to playpause')

def next_track():
    osascript.osascript('tell application \"Music\" to next track')

def previous_track():
    osascript.osascript('tell application \"Music\" to previous track')
    
# --- Helper Functions ---
def euclidean(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def get_ear(landmarks, top_idx, bottom_idx, left_idx, right_idx):
    top = landmarks[top_idx]
    bottom = landmarks[bottom_idx]
    left = landmarks[left_idx]
    right = landmarks[right_idx]
    vertical = euclidean(top, bottom)
    horizontal = euclidean(left, right)
    return vertical / horizontal

# --- Frame Skip Configuration ---
frame_count = 0
frame_skip = 2  # Try 1, 2 or 3 — higher = faster, less accurate

# --- Setup ---
screen_w, screen_h = pyautogui.size()

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=2,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.5)

# Open webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# --- Gesture Parameters ---
blink_threshold = 0.20
blink_cooldown = 1  # seconds
last_left_blink_time = 0
last_right_blink_time = 0
last_song_skip = 0
pinch_threshold = 0.05
last_pinch = 0
last_play_pause = 0
last_middle_pinch = 0
last_tab_close = 0
prev_screen_x, prev_screen_y = pyautogui.position()
smooth_factor = 0.5
disable_cursor_movement = False
last_volume_adjust = 0
neutral_nose_x = None

# --- Main Loop ---
while True:
    frame_count += 1
    if frame_count % frame_skip != 0:
        continue

    # Read and preprocess frame
    ret, img = cap.read()
    img = cv2.flip(img, 1)
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_results = face_mesh.process(rgb)
    hand_results = hands.process(rgb)

    # --- Face Landmarks & Blink Detection ---
    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                img, face_landmarks, mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )
            mp_drawing.draw_landmarks(
                img, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
            )

            # LEFT EYE BLINK = LEFT CLICK
            left_ear = get_ear(face_landmarks.landmark, 159, 145, 33, 133)
            if left_ear < blink_threshold and (time.time() - last_left_blink_time) > blink_cooldown:
                pyautogui.click(button='left')
                last_left_blink_time = time.time()
                disable_cursor_movement = True
                time.sleep(0.2)
                disable_cursor_movement = False

            # RIGHT EYE BLINK = RIGHT CLICK
            right_ear = get_ear(face_landmarks.landmark, 386, 374, 362, 263)
            if right_ear < blink_threshold and (time.time() - last_right_blink_time) > blink_cooldown:
                pyautogui.click(button='right')
                last_right_blink_time = time.time()
                disable_cursor_movement = True
                time.sleep(0.2)
                disable_cursor_movement = False
            
            # HEAD TILT TO NEXT SONG
            nose_tip = face_landmarks.landmark[1]
            if neutral_nose_x is None:
                neutral_nose_x = nose_tip.x

            head_tilt = nose_tip.x - neutral_nose_x
            if time.time() - last_song_skip > 2 and head_tilt > 0.05:
                    print("Tilt → Next Song")  # THIS should now show up
                    threading.Thread(target=next_track).start()
                    last_song_skip = time.time()

            # HEAD TILT TO PREVIOUS SONG
            elif time.time() - last_song_skip > 2 and head_tilt < -0.05:
                    print("Tilt → Previous Song")  # THIS should now show up
                    threading.Thread(target=previous_track).start()
                    last_song_skip = time.time()

            

    # --- Hand Landmarks & Gestures ---
    if hand_results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
            hand_label = hand_results.multi_handedness[idx].classification[0].label
            mp_drawing.draw_landmarks(
                img, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2)
            )

            # Right Hand = Cursor + Scroll + Tab Close
            img_h, img_w, _ = img.shape
            index_tip = hand_landmarks.landmark[8]
            if hand_label == "Right":
                x = int(index_tip.x * img_w)
                y = int(index_tip.y * img_h)
                cv2.circle(img, (x, y), 10, (255, 0, 0), -1)

                # Map to screen
                screen_x = int(index_tip.x * screen_w)
                screen_y = int(index_tip.y * screen_h)

                # Smooth cursor movement
                if not disable_cursor_movement:
                    if abs(screen_x - prev_screen_x) > 5 or abs(screen_y - prev_screen_y) > 5:
                        smooth_x = prev_screen_x + (screen_x - prev_screen_x) * smooth_factor
                        smooth_y = prev_screen_y + (screen_y - prev_screen_y) * smooth_factor
                        pyautogui.moveTo(smooth_x, smooth_y)
                        prev_screen_x, prev_screen_y = smooth_x, smooth_y

                # Pinch to Scroll Down
                thumb_tip = hand_landmarks.landmark[4]
                middle_tip = hand_landmarks.landmark[12]
                ring_tip = hand_landmarks.landmark[16]
                pinky_tip = hand_landmarks.landmark[20]
                pinch_dist = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)
                cx = int((index_tip.x + thumb_tip.x) / 2 * img_w)
                cy = int((index_tip.y + thumb_tip.y) / 2 * img_h)

                if pinch_dist < pinch_threshold:
                    cv2.circle(img, (cx, cy), 20, (0, 255, 0), -1)
                    if time.time() - last_pinch > 1:
                        pyautogui.scroll(-30)
                        last_pinch = time.time()
                else:
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), 2)

                # Pinch with Middle Finger to Scroll Up
                middle_pinch_distance = math.hypot(middle_tip.x - thumb_tip.x, middle_tip.y - middle_tip.y)
                mx = int((middle_tip.x + thumb_tip.x) / 2 * img_w)
                my = int((middle_tip.y + thumb_tip.y) / 2 * img_h)

                if middle_pinch_distance < pinch_threshold:
                    cv2.circle(img, (mx, my), 20, (0, 255, 0), -1)
                    if time.time() - last_pinch > 1:
                        pyautogui.scroll(30)
                        last_pinch = time.time()
                else:
                    cv2.circle(img, (mx, my), 10, (0, 0, 255), 2)

                # Pinch with Ring Finger to Close Tab
                ring_pinch_distance = math.hypot(ring_tip.x - thumb_tip.x, ring_tip.y - thumb_tip.y)
                rx = int((ring_tip.x + thumb_tip.x) / 2 * img_w)
                ry = int((ring_tip.y + thumb_tip.y) / 2 * img_h)

                if ring_pinch_distance < pinch_threshold:
                    cv2.circle(img, (rx, ry), 20, (0, 255, 0), -1)
                    if time.time() - last_tab_close > 2:
                        pyautogui.hotkey('command', 'w')
                        last_tab_close = time.time()
                else:
                    cv2.circle(img, (rx, ry), 10, (0, 0, 255), 2)

            # Left Hand = Volume & Play/Pause
            elif hand_label == "Left":
                thumb_tip = hand_landmarks.landmark[4]
                index_mcp = hand_landmarks.landmark[5]
                middle_mcp = hand_landmarks.landmark[9]
                index_tip = hand_landmarks.landmark[8]

                # THUMBS UP = Volume Up
                if thumb_tip.y < index_mcp.y and thumb_tip.y < middle_mcp.y:
                    cv2.putText(img, "Volume Up", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    if time.time() - last_volume_adjust > 1:
                        increase_volume()
                        last_volume_adjust = time.time()

                # THUMBS DOWN = Volume Down
                elif thumb_tip.y > index_mcp.y and thumb_tip.y > middle_mcp.y:
                    cv2.putText(img, "Volume Down", (30, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    if time.time() - last_volume_adjust > 1:
                        decrease_volume()
                        last_volume_adjust = time.time()

                # Index Thumb Pinch = Play/Pause
                pinch_dist = math.hypot(index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y)
                cx = int((index_tip.x + thumb_tip.x) / 2 * img_w)
                cy = int((index_tip.y + thumb_tip.y) / 2 * img_h)

                if pinch_dist < pinch_threshold:
                    cv2.circle(img, (cx, cy), 20, (0, 255, 0), -1)
                    if time.time() - last_pinch > 1:
                        playPause()
                        last_pinch = time.time()
                else:
                    cv2.circle(img, (cx, cy), 10, (0, 0, 255), 2)

    # --- Display the Result ---
    cv2.imshow('img', img)
    if cv2.waitKey(30) & 0xFF == 27:
        break

# --- Release Resources ---
cap.release()
cv2.destroyAllWindows()
