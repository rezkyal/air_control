import cv2
import mediapipe as mp
import mouse
import time
import screeninfo

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

FULL_INDEX_SIZE = 5
index_finger_tip_x = []
index_finger_tip_y = []

thumb_finger_tip_x = []
thumb_finger_tip_y = []

# For webcam input:
cap = cv2.VideoCapture(0)

monitor = screeninfo.get_monitors()[0]
monitor_width = monitor.width
monitor_height = monitor.height

pTime = 0
with mp_hands.Hands(
    min_detection_confidence=0.50,
    min_tracking_confidence=0.50) as hands:
    while cap.isOpened():
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

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
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        print('Handedness:', results.multi_handedness)
        if results.multi_hand_landmarks:
            print(len(results.multi_hand_landmarks))
            
            for hand_landmarks in results.multi_hand_landmarks:
                # print(
                #     f'Index finger tip coordinates: (',
                #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x}, '
                #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y}, '
                #     f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].z})'
                # )

                # x_point_thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                # y_point_thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                # x_point_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                # y_point_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                # x_point_index, y_point_index = smoothening.smoothening(x_point_index, y_point_index, index_finger_tip_x, index_finger_tip_y)
                # x_point_thumb, y_point_thumb = smoothening.smoothening(x_point_thumb, y_point_thumb, thumb_finger_tip_x, thumb_finger_tip_y)

                # index_finger_tip_x.append(x_point_index)
                # index_finger_tip_y.append(y_point_index)

                # thumb_finger_tip_x.append(x_point_thumb)
                # thumb_finger_tip_y.append(y_point_thumb)

                mp_drawing.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # else:
        #     index_finger_tip_x = []
        #     index_finger_tip_y = []

        #     thumb_finger_tip_x = []
        #     thumb_finger_tip_y = []

        # if len(index_finger_tip_x) > 1:

        #     for iteration in range (0, len(thumb_finger_tip_x)-1):
        #         x1 = int(thumb_finger_tip_x[iteration] * width)
        #         y1 = int(thumb_finger_tip_y[iteration] * height)
        #         x2 = int(thumb_finger_tip_x[iteration + 1] * width)
        #         y2 = int(thumb_finger_tip_y[iteration + 1] * height)
        #         cv2.line(image, (x1, y1), (x2, y2), (0,255,0), 2)

        #     for iteration in range (0, len(index_finger_tip_x)-1):
        #         x1 = int(index_finger_tip_x[iteration] * width)
        #         y1 = int(index_finger_tip_y[iteration] * height)
        #         x2 = int(index_finger_tip_x[iteration + 1] * width)
        #         y2 = int(index_finger_tip_y[iteration + 1] * height)
        #         cv2.line(image, (x1, y1), (x2, y2), (0,0,255), 2)


        #     x_mouse_monitor = index_finger_tip_x[len(index_finger_tip_x) - 1] * monitor_width
        #     y_mouse_monitor = index_finger_tip_y[len(index_finger_tip_y) - 1] * monitor_height

        #     # mouse.move(x_mouse_monitor, y_mouse_monitor)

        
        # while len(index_finger_tip_x) > FULL_INDEX_SIZE:
        #     index_finger_tip_x.pop(0)
        #     index_finger_tip_y.pop(0)
        #     thumb_finger_tip_x.pop(0)
        #     thumb_finger_tip_y.pop(0)

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.putText(image, str(int(fps)), (20,50), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,0), 3)

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()