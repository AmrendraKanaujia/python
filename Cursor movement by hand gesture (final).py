#Cursor movement by hand gesture by amrendra kumar kanaujia @amrendrakanaujia

#gesture info:
#always start with neutral pose ie all 4 fingures and thumb is up and open ie show full palm
#cursor: cursor will move according to thumb tip
#left click: when index finger is down than thumb
#right click: when mid finger is down than thumb
#scroll up: when thumb tip and ring fingure tip is touched
#scroll down: when thumb tip and pinky fingure tip is touched
#no two or more fingure should down at same time

#importing files
import cv2
import mediapipe as mp
import pyautogui as pag
import pygame

# Initialize pygame mixer
pygame.mixer.init()
#sound file
click_sound = pygame.mixer.Sound('Project Practice\mouse-click-117076.mp3')

mp_hands = mp.solutions.hands  # Hands detection module
mp_drawing = mp.solutions.drawing_utils  # Drawing utilities to overlay landmarks

#accesing screen cordinates
screen_w, screen_h = pag.size()
#printing coordinates
print('The Screen width:', screen_w)
print('The Screen height:', screen_h)

cap = cv2.VideoCapture(0)  # Start video capture from webcam

with mp_hands.Hands(
        static_image_mode=False,       # Set to False for video input
        max_num_hands=1,               # Maximum number of hands to detect
        min_detection_confidence=0.5,  # Detection confidence threshold
        min_tracking_confidence=0.5) as hands:

    while cap.isOpened():
        ret, flip_frame = cap.read()  # Capture a single frame
        frame = cv2.flip(flip_frame, 1)
        if not ret:
            print("Failed to grab frame")
            break

        # Convert the image to RGB as MediaPipe requires it
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame and detect hands
        results = hands.process(rgb_frame)

        # Check if hands are detected
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw landmarks on each detected hand
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=hand_landmarks,
                    connections=mp_hands.HAND_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), circle_radius=2 ),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=1 )
                     )
                
                #accesing thumb tip's coordinates: 4
                thumb_tip = hand_landmarks.landmark[4]

                #converting to screen coordinates
                # Set a margin for the camera frame
                margin_ratio = 0.1  # Maps 80% of camera view to full screen
                x_margin = screen_w * margin_ratio
                y_margin = screen_h * margin_ratio

                # Scale hand position within these margins
                thumb_tip_x = ((thumb_tip.x - margin_ratio) / (1 - 2 * margin_ratio)) * screen_w
                thumb_tip_y = ((thumb_tip.y - margin_ratio) / (1 - 2 * margin_ratio)) * screen_h

                
                #move cursor acc to 4
                pag.moveTo(thumb_tip_x, thumb_tip_y, duration=0.05)

                #accesing indexfin_tip's coordinate: 8
                indexfin_tip = hand_landmarks.landmark[8]
                #converting to screen coordinates
                indexfin_tip_y = (indexfin_tip.y * screen_h)
                #condition for left click
                left_click_diff = abs(thumb_tip_y - indexfin_tip_y)
                print("left diff:", left_click_diff)
                if left_click_diff < 60:
                    pag.click(x=thumb_tip_x, y=thumb_tip_y, clicks=1, interval=0.0, button='left', duration=0.0)
                    print('Diff:', left_click_diff, "Left Key Clicked")
                    click_sound.play()

                #accesing midfin_tip's coordinate: 12
                midfin_tip = hand_landmarks.landmark[12]
                #converting to screen coordinates
                midfin_tip_y = (midfin_tip.y * screen_h)
                #condition for left click
                right_click_diff = abs(thumb_tip_y - midfin_tip_y)
                print('Right Diff:', right_click_diff)
                if right_click_diff < 40:
                    pag.click(x=thumb_tip_x, y=thumb_tip_y, clicks=1, interval=0.0, button='right', duration=0.0)
                    print('Diff:', right_click_diff, "Right Key Clicked")
                    click_sound.play()

                #accesing ringfin_tip's coordinate: 16
                ringfin_tip = hand_landmarks.landmark[16]
                #converting to screen coordinates
                ringfin_tip_y = (ringfin_tip.y * screen_h)
                #condition for scroll up
                ringfin_diff = abs(thumb_tip_y - ringfin_tip_y)
                print('Ring fingure Diff:', ringfin_diff)
                if ringfin_diff < 40:
                    pag.scroll(100)
                    print('Diff:', ringfin_diff, "Scroll Up")
                    click_sound.play()

                #accesing pinkfin_tip's coordinate: 20
                pinkfin_tip = hand_landmarks.landmark[20]
                #converting to screen coordinates
                pinkfin_tip_y = (pinkfin_tip.y * screen_h)
                #condition for scroll down
                pinkfin_diff = abs(thumb_tip_y - pinkfin_tip_y)
                print('Pinky fingure Diff:', pinkfin_diff)
                if pinkfin_diff < 40:
                    pag.scroll(-100)
                    print('Diff:', pinkfin_diff, "Scroll down")
                    click_sound.play()
                
                if left_click_diff < 60 and right_click_diff < 40:
                    print("Use Error: Both Index finger and Mid finger can't be closed to thumb at same time. ")
                


        # Display the output frame with hand landmarks
        cv2.imshow('Hand Detection', frame)

        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Release resources
cap.release()
cv2.destroyAllWindows()
