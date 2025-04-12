import cv2
import cv2 as cv
import mediapipe as mp
import numpy as np

# mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# capture video
path = 'resources/hand.MP4'
url = 'http://192.168.100.62:4747/video'
cap = cv.VideoCapture(url)


def distance(start, end):
    return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5


def direction(start, end):
    return 1 if end[0] - start[0] > 0 else -1


prev_pos = (0, 0)
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

            index_finger_mcp = hand_landmarks.landmark[5]

            pos = (index_finger_mcp.x, index_finger_mcp.y)
            if distance(prev_pos, pos) > 0.05:
                if direction(prev_pos, pos) > 0:
                    cv.putText(frame, 'Swipe Left', (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv.putText(frame, 'Swipe Right', (50, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            prev_pos = pos

    cv.imshow('frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv.destroyAllWindows()
