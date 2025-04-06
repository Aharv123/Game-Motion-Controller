import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_drawing = mp.solutions.drawing_utils

# Webcam input (use lower resolution for faster processing)
cap = cv2.VideoCapture(0)
cap.set(3, 640)  # width
cap.set(4, 480)  # height

# Timing control
last_action_time = time.monotonic()
cooldown = 0.8  # seconds
    
# Finger tip indices in MediaPipe
tip_ids = [4, 8, 12, 16, 20]

def count_fingers(hand_landmarks):
    fingers = []

    # Thumb (check direction based on hand orientation)
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

print("🟢 Control with 1–4 fingers: Jump ➡️ ➡️ ➡️")

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers_up = count_fingers(hand_landmarks)
            now = time.monotonic()

            if now - last_action_time > cooldown:
                if fingers_up == 1:
                    pyautogui.press('space')
                    print("⬆️ Jump (1 finger)")
                    last_action_time = now

                elif fingers_up == 2:
                    pyautogui.press('right')
                    print("➡️ Move Right (2 fingers)")
                    last_action_time = now

                elif fingers_up == 3:
                    pyautogui.press('left')
                    print("⬅️ Move Left (3 fingers)")
                    last_action_time = now

                elif fingers_up == 4:
                    pyautogui.press('down')
                    print("⬇️ Duck (4 fingers)")
                    last_action_time = now

    cv2.imshow("🖐️ Finger Motion Controller", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()
 