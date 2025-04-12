import cv2
import cv2 as cv
import mediapipe as mp
import numpy as np
import time

# mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# capture video
path = 'resources/hand.MP4'
url = 'http://192.168.100.62:4747/video'
cap = cv.VideoCapture(url)

cur_time = time.time()
prev_pos = (0, 0)
opt = 0
opts = [
    'YouTube',
    'Discord',
    'CLion'
]


def distance(start, end):
    return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5


def direction(start, end):
    return 1 if end[0] - start[0] > 0 else -1


def swipe(_dire=0):
    if _dire == 0:
        return

    global cur_time, opt
    now = time.time()
    if now - cur_time > 1:
        if _dire == 1:
            if opt < len(opts) - 1:
                opt += 1
            else:
                opt = 0
        else:
            if opt > 0:
                opt -= 1
            else:
                opt = len(opts) - 1
        cur_time = now


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

    cv.putText(frame, ''.join([str(opt + 1), ': ', opts[opt]]), (25, 100), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            hand_anchor = hand_landmarks.landmark[8]

            pos = (hand_anchor.x, hand_anchor.y)
            if distance(prev_pos, pos) > 0.1:
                dire = direction(prev_pos, pos)
                swipe(dire)
                cv.putText(frame, 'Swipe Trigger', (25, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            prev_pos = pos

    cv.imshow('frame', frame)

    # print("time", cur_time)
    # cur_time = time.time()

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
