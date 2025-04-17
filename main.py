import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import pyautogui

# mediapipe hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_drawing = mp.solutions.drawing_utils

# capture video
url = 'http://192.168.100.62:4747/video'
cap = cv.VideoCapture(url)

swipe_time = select_time = time.time()
already_selected = False
prev_pos = (0, 0)
opt = 0
opts = [
    'Resume/Pause',
    'Next Song',
    'Prev Song',
    'Mute/Unmute',
    'Volume Up',
    'Volume Down',
    'Quit App'
]


def distance(start, end):
    return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5


def direction(start, end):
    return 1 if end[0] - start[0] > 0 else -1


def swipe(_dire=0):
    if _dire == 0:
        return

    global swipe_time, opt
    now = time.time()
    if now - swipe_time > 0.25:
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
        swipe_time = now


def select():
    global select_time, opt, already_selected
    now = time.time()
    if now - select_time > 1 and not already_selected:
        # 0 - 'Resume/Pause',
        # 1 - 'Next Song',
        # 2 - 'Prev Song',
        # 3 - 'Mute/Unmute'
        # 4 - 'Volume Up'
        # 5 - 'Volume Down'
        # Last - 'Quit App'
        if opt == 0:
            pyautogui.press('playpause')
        elif opt == 1:
            pyautogui.press('nexttrack')
        elif opt == 2:
            pyautogui.press('prevtrack')
        elif opt == 3:
            pyautogui.press('volumemute')
        elif opt == 4:
            for i in range(5):
                pyautogui.press('volumeup')
        elif opt == 5:
            for i in range(5):
                pyautogui.press('volumedown')
        elif opt == len(opts) - 1:
            raise SystemExit
        else:
            print("Unknown command")
        select_time = now
        already_selected = True


while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # rotate and crop frame
    frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    frame = cv.resize(frame, (480, 640))
    frame = frame[100:560, 30:440]

    cv.putText(frame, 'Music Controller', (25, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv.putText(frame, ''.join([str(opt + 1), ': ', opts[opt]]), (25, 100), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    result = hands.process(rgb)


    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # detecting swipes
            hand_anchor = hand_landmarks.landmark[8]

            pos = (hand_anchor.x, hand_anchor.y)
            if distance(prev_pos, pos) > 0.1:
                dire = direction(prev_pos, pos)
                swipe(dire)

            prev_pos = pos

            # selecting an option
            index_tip, index_mcp = hand_landmarks.landmark[8], hand_landmarks.landmark[5]
            middle_tip, middle_mcp = hand_landmarks.landmark[12], hand_landmarks.landmark[9]
            ring_tip, ring_mcp = hand_landmarks.landmark[16], hand_landmarks.landmark[13]
            pinky_tip, pinky_mcp = hand_landmarks.landmark[20], hand_landmarks.landmark[17]

            index_dist = distance((index_tip.x, index_tip.y), (index_mcp.x, index_mcp.y))
            middle_dist = distance((middle_tip.x, middle_tip.y), (middle_mcp.x, middle_mcp.y))
            ring_dist = distance((ring_tip.x, ring_tip.y), (ring_mcp.x, ring_mcp.y))
            pinky_dist = distance((pinky_tip.x, pinky_tip.y), (pinky_mcp.x, pinky_mcp.y))

            # print(index_dist, middle_dist, ring_dist, pinky_dist)
            min_select_dist = 0.05
            if (index_dist < min_select_dist and middle_dist < min_select_dist
                    and ring_dist < min_select_dist and pinky_dist < min_select_dist):
                select()
            else:
                already_selected = False

    cv.imshow('Frame', frame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
