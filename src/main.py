import math
import time
import cv2
import mediapipe as mp
import win32api as wp
import win32con as wc
import pent_gui
from imutils.video import WebcamVideoStream


WIN_NAME = 'Picture'
MHEIGHT = wp.GetSystemMetrics(1)
MWIDTH = wp.GetSystemMetrics(0)


def get_distance(first, second):
    x1, y1 = first
    x2, y2 = second
    return math.sqrt((x1-x2)**2 + (y1-y2)**2)


def track():
    hands = mp.solutions.hands.Hands()  # False, 2, 0.5, 0.5
    draw = mp.solutions.drawing_utils
    cap = WebcamVideoStream(src=0).start()
    prev_time = 0
    cur_time = 0

    cv2.namedWindow(WIN_NAME, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(WIN_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    overlay = cap.read()
    height, width, channel = overlay.shape

    record = True
    while record:
        img = cap.read()
        img.flags.writeable = False
        img = cv2.flip(img, 1)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        sensed = results.multi_hand_landmarks
        if sensed:
            for mano in sensed:
                lm = mano.landmark[8]  # tip of index finger
                cur = mano.landmark[12]  # tip of middle finger
                compare = mano.landmark[3]  # thumb knuckle
                lm_c_one = mano.landmark[1]  # base of thumb
                lm_c_two = mano.landmark[0]  # wrist
                cx, cy = int(lm.x * width), int(lm.y * height)
                mx, my = int(compare.x * width), int(compare.y * height)
                distance = get_distance((cur.x * width, cur.y * height), (mx, my))

                # Translate to monitor specifications
                mtrans_w = lm.x * MWIDTH
                mtrans_h = lm.y * MHEIGHT
                wp.SetCursorPos((int(mtrans_w), int(mtrans_h)))

                if distance <= 50:
                    clicked_color = (255, 0, 0)
                    wp.mouse_event(wc.MOUSEEVENTF_LEFTDOWN, int(mtrans_w), int(mtrans_h), 0, 0)
                else:
                    clicked_color = (255, 0, 255)
                    wp.mouse_event(wc.MOUSEEVENTF_LEFTUP, int(mtrans_w), int(mtrans_h), 0, 0)

                cv2.circle(img, (cx, cy), 5, clicked_color, cv2.FILLED)

        cur_time = time.time()
        fps = 1 / (cur_time - prev_time)
        prev_time = cur_time

        cv2.putText(img, str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)

        cv2.imshow(WIN_NAME, img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def main():
    pent_gui.launch_gui()
    track()


if __name__ == "__main__":
    main()
