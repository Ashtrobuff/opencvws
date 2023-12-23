import cv2 as cv
import numpy as np
import mediapipe as mp

# ------- Resizing and Rescaling Images --------- #
def rescale(frame, scale=1.5):
    # Images, Videos and Live Video
    height = int(frame.shape[0]*scale)
    width = int(frame.shape[1]*scale) 
    dimensions = (width, height)

    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA) # (src , dimensions, interpolation) 
    # interpolation is the method of how the image is resized
    # INTER_AREA is used for shrinking the image and INTER_LINEAR is used for enlarging the image

mp_drawing = mp.solutions.drawing_utils # Drawing helpers 
mp_drawing_styles = mp.solutions.drawing_styles # Drawing styles (for drawing landmarks)
mp_hands = mp.solutions.hands # Hands model (for detecting hands)


def getHandMove(hands_landmarks):
    landmark = hands_landmarks.landmark
    # print(landmark)
    # landmark for fingers
    l5 = landmark[5].y
    l8 = landmark[8].y
    l9 = landmark[9].y
    l12 = landmark[12].y
    l13 = landmark[13].y
    l16 = landmark[16].y
    l17 = landmark[17].y
    l20 = landmark[20].y

    if(l5<l8 and l9<l12 and l13<l16 and l17<l20):
        return "Rock"
    elif(l13<l16 and l17<l20):
        return "Scissors"
    else:
        return "Paper"



video = cv.VideoCapture(0) # Video capture object from webcam

clock = 0
p1_move = p2_move = None
gameText  = ""
resultText = ""
succes  = True;

with mp_hands.Hands(model_complexity=0 , min_detection_confidence=0.5 , min_tracking_confidence=0.5) as hands: # Hands object
    while True:
        ret , frame = video.read()
        if ret == False:
            break

        frame  = cv.cvtColor(frame , cv.COLOR_BGR2RGB) # Converting the frame to RGB
        results = hands.process(frame)
        frame = cv.cvtColor(frame , cv.COLOR_RGB2BGR) # Converting the frame back to BGR
        if results.multi_hand_landmarks:
            for hands_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame , hands_landmarks , mp_hands.HAND_CONNECTIONS , mp_drawing_styles.get_default_hand_landmarks_style() , mp_drawing_styles.get_default_hand_connections_style())
        frame = cv.flip(frame , 1)
        if 0<= clock <= 20:
            succes = True
            gameText = "Ready"
        elif clock <30: gameText = "3.."
        elif clock <40: gameText = "2.."
        elif clock <50: gameText = "1.."
        elif clock <60: gameText = "Shoot!"
        elif clock ==60:
            hls = results.multi_hand_landmarks
            if hls and len(hls)==2:
                p1_move = getHandMove(hls[0])
                p2_move = getHandMove(hls[1])
            else:
                succes = False
                gameText = "Error"
        elif clock <100:
            if succes:
                gameText = f"Player 1:{p1_move} Player 2:{p2_move}"
                if p1_move == p2_move:
                    resultText = "Draw"
                elif (p1_move == "Rock" and p2_move == "Scissors") or (p1_move == "Scissors" and p2_move == "Paper") or (p1_move == "Paper" and p2_move == "Rock"):
                    resultText = "Player 1 Wins"
                else:
                    resultText = "Player 2 Wins"
            else:
                resultText = "No Result"
                gameText = "Didn't detect both hands"
        cv.putText(frame , str(clock) , (10,100) , cv.FONT_HERSHEY_SIMPLEX , 0.5 , (0,0,255) , 1)
        cv.putText(frame , resultText , (10,150) , cv.FONT_HERSHEY_SIMPLEX , 0.5 , (0,255,0) , 2)
        cv.putText(frame , gameText , (10,50) , cv.FONT_HERSHEY_SIMPLEX , 0.5 , (0,0,255) , 2)
        clock = (clock + 1)%101
        cv.imshow("Video" , rescale(frame))
        if cv.waitKey(5) & 0xFF==ord('d'):
        # 20 is the delay means that the video will be played at 50 fps , to increase the fps decrease the delay
        # 0xFF==ord('d') is the key to stop the video i.e pressing 'd' will stop the video
            break

video.release() # releases the capture
cv.destroyAllWindows() # destroys all the windows 