import math
import time
import cv2
import mediapipe as mp
import win32api as wp
import win32con as wc
import pent_gui as pg
import multiprocessing
import os
import threading
from win32gui import GetForegroundWindow, ShowWindow, EnumWindows
from imutils.video import WebcamVideoStream


WIN_NAME = 'Picture'
MHEIGHT = wp.GetSystemMetrics(1)
MWIDTH = wp.GetSystemMetrics(0)
STOP_THREAD = False


def get_distance(first, second):
    x1, y1 = first
    x2, y2 = second
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


def summon_the_storm():
    tr = threading.Thread(target=pg.main, args=())
    tr.daemon = True
    tr.start()


def track(show_debug: bool):

    hands = mp.solutions.hands.Hands(max_num_hands=1)  # False, 2, 0.5, 0.5
    cap = cv2.VideoCapture(0)
    prev_time = 0
    cur_time = 0
    tr_dc = False
    gui_on = False
    niterate = 0
    prevx, prevy = 0, 0

    if show_debug:
        cv2.namedWindow(WIN_NAME, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(WIN_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    _, overlay = cap.read()
    height, width, channel = overlay.shape
    record = True
    while record:
        niterate += 1
        _, img = cap.read()
        img.flags.writeable = False
        img = cv2.flip(img, 1)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        sensed = results.multi_hand_landmarks
        if sensed:
            if not gui_on:
                gui_on = True
                summon_the_storm()
                pg.STOP = False
                # start gui
            for mano in sensed:
                lm = mano.landmark[8]  # tip of index finger
                cur = mano.landmark[12]  # tip of middle finger
                compare = mano.landmark[3]  # thumb knuckle
                th_tip = mano.landmark[4]  # thumb tip
                ring_tip = mano.landmark[16]  # ring tip
                cx, cy = int(lm.x * width), int(lm.y * height)
                mx, my = int(compare.x * width), int(compare.y * height)
                distance = get_distance((cur.x * width, cur.y * height), (mx, my))

                # Translate to monitor specifications
                mtrans_w = lm.x * MWIDTH
                mtrans_h = lm.y * MHEIGHT

                # Jitter protection, still should be optimized
                curx, cury = wp.GetCursorPos()
                if niterate % 2 == 0 and abs(curx - prevx) > 10 and abs(cury - prevy) > 10:
                    wp.SetCursorPos((int(curx), int(cury)))
                elif niterate % 2 != 0:
                    wp.SetCursorPos((int(mtrans_w), int(mtrans_h)))

                prevx, prevy = curx, cury

                if distance <= 50:
                    clicked_color = (255, 0, 0)
                    wp.mouse_event(wc.MOUSEEVENTF_LEFTDOWN, int(mtrans_w), int(mtrans_h), 0, 0)
                else:
                    clicked_color = (255, 0, 255)
                    wp.mouse_event(wc.MOUSEEVENTF_LEFTUP, int(mtrans_w), int(mtrans_h), 0, 0)

                thumb_ring = get_distance((th_tip.x * width, th_tip.y * height),
                                          (ring_tip.x * width, ring_tip.y * height))
                if thumb_ring <= 15:
                    if tr_dc:
                        tr_dc = False
                        wtm = GetForegroundWindow()
                        ShowWindow(wtm, wc.SW_MINIMIZE)
                else:
                    tr_dc = True

                sd = get_distance((cx, cy), (ring_tip.x * width, ring_tip.y * height))
                if sd <= 15 and niterate % 3 == 0:
                    return

                if niterate == 3:
                    niterate = 1

                cv2.circle(img, (cx, cy), 5, clicked_color, cv2.FILLED)
        else:
            if gui_on:
                gui_on = False
                pg.STOP = True
                # stop gui
        cur_time = time.time()
        fps = 1 / (cur_time - prev_time)
        prev_time = cur_time

        cv2.putText(img, str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)

        if show_debug:
            cv2.imshow(WIN_NAME, img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


def main():
    track(show_debug=False)


if __name__ == "__main__":
    main()
