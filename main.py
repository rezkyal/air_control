from hand.pointerhand import PointerHand
from hand.clickhand import ClickHand
import cv2
import mediapipe as mp
import time
import screeninfo
from settings import camera_settings

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

monitor = screeninfo.get_monitors()[0]
monitor_width = monitor.width
monitor_height = monitor.height

webcam_width = camera_settings.CAMERA_WIDTH
webcam_height = camera_settings.CAMERA_HEIGHT

# For webcam input:
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, webcam_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, webcam_height)

hand_index = []

click_hand = ClickHand(webcam_width, webcam_height)
pointer_hand = PointerHand(webcam_width, webcam_height, monitor_width, monitor_height)

pTime = 0
with mp_hands.Hands(
    min_detection_confidence=0.70,
    min_tracking_confidence=0.70) as hands:
    while cap.isOpened():
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

        is_click_hand_tracking = click_hand.get_is_tracking()
        is_pointer_hand_tracking = pointer_hand.get_is_tracking()

        success, image = cap.read()
        
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        used_image = cv2.resize
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:

            hand_index = []
            for each_hand in results.multi_handedness:
                hand_index.append(each_hand.classification[0].label)

            for iteration in range(0, len(hand_index)):
                if hand_index[iteration] == "Right" :
                    if not is_pointer_hand_tracking:
                        pointer_hand.begin_tracking()
                    hand_landmarks = results.multi_hand_landmarks[iteration]
                    pointer_hand.update_finger_tip(hand_landmarks, mp_hands, image)

                elif hand_index[iteration]  == "Left" :
                    if not is_click_hand_tracking:
                        click_hand.begin_tracking()
                    hand_landmarks = results.multi_hand_landmarks[iteration]
                    click_hand.update_finger_tip(hand_landmarks, mp_hands, image)
        
        else:
            click_hand.stop_tracking()
            pointer_hand.stop_tracking()
        
        click_hand.draw_box(image)
        pointer_hand.draw_box(image)

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(image, str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

        click_state = click_hand.get_current_click_state()
        org_x = monitor_width - 100
        cv2.putText(image, click_state, (1000,50), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 3)

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()