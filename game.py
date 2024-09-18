import cv2
import mediapipe as mp
import math
import random
# Initialize MediaPipe Hands and Drawing Utils
def play_rock_paper_scissors():
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    randint = random.randint(0, 2)
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    num = 0
    counter = 0
    counter2 = 0
    beep = False
    palm_was_visible = False
    # Instantiate Hands object once
    hands = mp_hands.Hands()

    def get_landmark_coordinates(landmark_number, frame):

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if 0 <= landmark_number < len(hand_landmarks.landmark):
                    landmark = hand_landmarks.landmark[landmark_number]
                    height, width, _ = frame.shape
                    x = int(landmark.x * width)
                    y = int(landmark.y * height)
                    return (x, y)
        return None
    def get_angle(tx, ty, mx, my, bx, by):
        tm = math.sqrt((tx-mx)**2 + (ty-my)**2)
        mb = math.sqrt((bx-mx)**2 + (by-my)**2)
        bt = math.sqrt((bx-tx)**2 + (by-ty)**2)
        try:
            angle = math.acos(((tm**2) + (mb**2) - (bt**2))/(2*tm*mb))
        except:
            angle = math.pi
        angle *= 180/math.pi
        return angle
    def is_bent(t, m, b):
        tip = get_landmark_coordinates(t, frame)
        middle = get_landmark_coordinates(m, frame)
        bottom = get_landmark_coordinates(b, frame)
        if tip and middle and bottom:
            tx, ty = tip
            mx, my = middle
            bx, by = bottom
            angle = get_angle(tx, ty, mx, my, bx, by)//1
            if not angle >= 145:
                index = True
                return index
    figures = ["scissor", "paper", "rock"]
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        if counter2 <= 4:
            
            mno = get_landmark_coordinates(0, frame)
        if mno is None:
            if palm_was_visible:
                palm_was_visible = False
        else:
            if not palm_was_visible:
                palm_was_visible = True
                counter2 += 1
        if counter2 >= 4:    
            index = is_bent(8, 6, 5)
            pinky = is_bent(20, 18, 17)
            prevnum = num
            if not index and pinky:
                num = 0
            if not index and not pinky:
                num = 1
            if index and pinky:
                num = 2
            if prevnum == num:
                counter += 1
            else:
                counter = 0

            if counter == 3:

                break


            # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    outcomes = ["tie", "win", "lose"]
    ["scissor", "paper", "rock"]
    if num == randint:
        wl = 0
    if num == 0 and randint == 1:
        wl = 1
    if num == 0 and randint == 2:
        wl = 2
    if num == 1 and randint == 0:
        wl = 2
    if num == 1 and randint == 2:
        wl = 1
    if num == 2 and randint == 0:
        wl = 1
    if num == 2 and randint == 1:
        wl = 2
    return (figures[num], figures[randint] ,outcomes[wl])
print(play_rock_paper_scissors())
