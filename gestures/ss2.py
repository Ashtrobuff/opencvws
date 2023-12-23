import cv2
import mediapipe as mp
import pyautogui

webcam = cv2.VideoCapture(0)
my_hands = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils

while True:
    _, image = webcam.read()
    frame_height = image.shape[0]
    frame_width = image.shape[1]
    rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_img)
    hands = output.multi_hand_landmarks

    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark

            # Draw wireframe connecting hand landmarks
            for i in range(0, 21):
                x_i = int(landmarks[i].x * frame_width)
                y_i = int(landmarks[i].y * frame_height)
                cv2.circle(image, (x_i, y_i), 5, (0, 255, 0), -1)

                if i > 0:
                    x_prev = int(landmarks[i - 1].x * frame_width)
                    y_prev = int(landmarks[i - 1].y * frame_height)
                    cv2.line(image, (x_prev, y_prev), (x_i, y_i), (0, 255, 0), 2)

            # Connect the last and first landmarks to complete the loop
            x_first = int(landmarks[0].x * frame_width)
            y_first = int(landmarks[0].y * frame_height)
            cv2.line(image, (x_i, y_i), (x_first, y_first), (0, 255, 0), 2)

        # Check for a fist gesture (all fingers closed)
        is_fist = all(landmarks[i].y > landmarks[i + 1].y for i in range(0, 20, 4))

        if is_fist:
            # Take a screenshot when a fist is detected
            screenshot = pyautogui.screenshot()
            screenshot.save("screenshot.png")

    cv2.imshow("Hand volume control", image)
    key = cv2.waitKey(10)
    if key == 27:
        break

webcam.release()
cv2.destroyAllWindows()
