import time
import cv2
import mediapipe as mp
import win32api as wp
import win32con
WIN_NAME = 'Picture'


def track():
    hands = mp.solutions.hands.Hands()  # False, 2, 0.5, 0.5
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    prev_time = 0
    cur_time = 0

    cv2.namedWindow(WIN_NAME, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(WIN_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    _, overlay = cap.read()
    height, width, channel = overlay.shape

    record = True
    while record:
        exito, img = cap.read()
        img.flags.writeable = False
        img = cv2.flip(img, 1)
        if not exito:
            print("Error! Wrong input device!")
            break
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        sensed = results.multi_hand_landmarks
        if sensed:
            for mano in sensed:
                lm = mano.landmark[8]  # tip of index finger
                cursor_pos = mano.landmark[12]  # tip of middle finger
                lm_c_one = mano.landmark[1]  # base of thumb
                lm_c_two = mano.landmark[0]  # wrist
                cx, cy = int(lm.x * width), int(lm.y * height)
                mx, my = int(cursor_pos.x * width), int(cursor_pos.y * height)
                wp.SetCursorPos((mx, my))
                clicked_color = (255, 0, 0) if lm.z > lm_c_one.z and lm.z > lm_c_two.z else (255, 0, 255)
                cv2.circle(img, (cx, cy), 5, clicked_color, cv2.FILLED)
                # draw.draw_landmarks(img, mano)

        cur_time = time.time()
        fps = 1 / (cur_time - prev_time)
        prev_time = cur_time

        cv2.putText(img, str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)

        cv2.imshow(WIN_NAME, img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


def main():
    track()


if __name__ == "__main__":
    main()
