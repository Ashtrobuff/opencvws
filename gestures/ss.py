import cv2
import mediapipe as mp
import pyautogui

webcam = cv2.VideoCapture(0)
x1 = y1 = x2 = y2 = x3 = y3 = x4 = y4 = x5 = y5 = 0
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
            drawing_utils.draw_landmarks(image, hand,)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x1, y1 = x, y
                if id == 4:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(0, 255, 255), thickness=3)
                    x2, y2 = x, y

        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 // 4
        cv2.line(image, (x1, y1), (x2, y2), (9, 255, 0), 5)

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
