import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

# Webcam input
cap = cv2.VideoCapture(0)

# Timing control to prevent repeated triggers
last_action_time = 0
cooldown = 1.0  # seconds

# Finger tip indices in MediaPipe
tip_ids = [4, 8, 12, 16, 20]

def count_fingers(hand_landmarks):
    fingers = []

    # Thumb
    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    for i in range(1, 5):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

print("🟢 Show hand gestures: ✌️☝️🖐️✊")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers_up = count_fingers(hand_landmarks)
            current_time = time.time()

            # Map gestures to keys
            if fingers_up == 0 and current_time - last_action_time > cooldown:
                pyautogui.press('down')
                print("⬇️ Duck (Fist)")
                last_action_time = current_time

            elif fingers_up == 1 and current_time - last_action_time > cooldown:
                pyautogui.press('right')
                print("➡️ Move Right (1 finger)")
                last_action_time = current_time

            elif fingers_up == 2 and current_time - last_action_time > cooldown:
                pyautogui.press('left')
                print("⬅️ Move Left (2 fingers)")
                last_action_time = current_time

            elif fingers_up == 5 and current_time - last_action_time > cooldown:
                pyautogui.press('space')
                print("⬆️ Jump (Open Palm)")
                last_action_time = current_time

    cv2.imshow("Finger Motion Controller", frame)
    if cv2.waitKey(5) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
