import cv2
import cv2 as cv
import mediapipe as mp
import numpy as np

# mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

# capture video
path = 'resources/hand.MP4'
url = 'http://192.168.100.62:4747/video'
cap = cv.VideoCapture(url)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        # cap = cv.VideoCapture(url)
        # continue
        break

    # rotate and crop frame
    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    frame = cv.resize(frame, (480, 640))
    frame = frame[100:560, 30:440]

    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv.imshow('frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv.destroyAllWindows()
