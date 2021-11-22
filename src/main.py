import cv2
import mediapipe as mp
import time


def track():
    hands = mp.solutions.hands.Hands()  # False, 2, 0.5, 0.5
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    prev_time = 0
    cur_time = 0

    record = True
    while record:
        exito, img = cap.read()
        img.flags.writeable = False
        img = cv2.flip(img, 1)
        height, width, channel = img.shape
        if not exito:
            print("Error! Wrong input device!")
            break
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        sensed = results.multi_hand_landmarks
        if sensed:
            for mano in sensed:
                lm = mano.landmark[8]
                cx, cy = int(lm.x * width), int(lm.y * height)
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
                # draw.draw_landmarks(img, mano)

        cur_time = time.time()
        fps = 1 / (cur_time - prev_time)
        prev_time = cur_time

        cv2.putText(img, str(int(fps)), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 1)

        cv2.imshow("Picture", img)
        cv2.waitKey(1)


def main():
    track()


if __name__ == "__main__":
    main()
