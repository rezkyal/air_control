import stabilizer
import cv2

class Hand:

    _max_tip_point = 5

    _is_tracking = False
    _index_finger_tip_x = []
    _index_finger_tip_y = []

    _thumb_finger_tip_x = []
    _thumb_finger_tip_y = []

    _camera_width = 0
    _camera_height = 0

    _box_start_point = (0, 0)
    _box_end_point = (0, 0)

    _tip_color = (0, 0, 0)
    _box_color = (0, 0, 0)

    def __init__(self, tip_color, box_color, camera_width, camera_height, box_left_percentage = 0.1, box_bottom_percentage = 0.1, box_size_to_screen = 0.1) -> None:
        self._tip_color = tip_color
        self._box_color = box_color
        self._camera_width = camera_width
        self._camera_height = camera_height
        self.calculate_box_point(box_left_percentage, box_bottom_percentage, box_size_to_screen)

    def calculate_box_point(self, box_left_percentage, box_bottom_percentage, box_size_to_screen):
        box_start_point_x = box_left_percentage * self._camera_width
        box_start_point_y = self._camera_height - ((box_bottom_percentage + box_size_to_screen) * self._camera_height)
        box_end_point_x = (box_left_percentage + box_size_to_screen) * self._camera_width
        box_end_point_y = self._camera_height - (box_bottom_percentage * self._camera_height)

        self._box_start_point = (int(box_start_point_x), int(box_start_point_y))
        self._box_end_point = (int(box_end_point_x), int(box_end_point_y))

    def draw_box(self, image):
        cv2.rectangle(image, self._box_start_point, self._box_end_point, self._box_color, 3)

    def index_finger_in_box(self):
        return self.finger_in_box(self._index_finger_tip_x, self._index_finger_tip_y)

    def thumb_finger_in_box(self):
        return self.finger_in_box(self._thumb_finger_tip_x, self._thumb_finger_tip_y)

    def finger_in_box(self, finger_tip_x, finger_tip_y):
        x_last_in_camera = finger_tip_x[len(finger_tip_x) - 1] * self._camera_width
        y_last_in_camera = finger_tip_y[len(finger_tip_y) - 1] * self._camera_height

        is_x_in_box = self._box_start_point[0] <= x_last_in_camera <= self._box_end_point[0]
        is_y_in_box = self._box_start_point[1] <= y_last_in_camera <= self._box_end_point[1]

        if is_x_in_box and is_y_in_box:
            x_in_box_percentage = (x_last_in_camera - self._box_start_point[0]) / (self._box_end_point[0] - self._box_start_point[0])
            y_in_box_percentage = (y_last_in_camera - self._box_start_point[1]) / (self._box_end_point[1] - self._box_start_point[1])

            return True, x_in_box_percentage, y_in_box_percentage

        else:
            
            return False, 0, 0

    def update_camera_size(self, camera_width, camera_height):
        self._camera_width = camera_width
        self._camera_height = camera_height

    def get_is_tracking(self):
        return self._is_tracking

    def begin_tracking(self):
        self._is_tracking = True

    def stop_tracking(self):
        self._is_tracking = False
        self._index_finger_tip_x = []
        self._index_finger_tip_y = []
        self._thumb_finger_tip_x = []
        self._thumb_finger_tip_y = []

    def update_finger_tip(self, hand_landmarks, mp_hands, image, is_calculate_centroid = True, is_smoothen = True):
        x_point_thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
        y_point_thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

        x_point_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
        y_point_index = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y


        x_point_index, y_point_index = stabilizer.stabilize(x_point_index, y_point_index, self._index_finger_tip_x, self._index_finger_tip_y, is_calculate_centroid, is_smoothen)
        x_point_thumb, y_point_thumb = stabilizer.stabilize(x_point_thumb, y_point_thumb, self._thumb_finger_tip_x, self._thumb_finger_tip_y, is_calculate_centroid, is_smoothen)

        self._index_finger_tip_x.append(x_point_index)
        self._index_finger_tip_y.append(y_point_index)

        self._thumb_finger_tip_x.append(x_point_thumb)
        self._thumb_finger_tip_y.append(y_point_thumb)

        if len(self._index_finger_tip_x) > 1:

            for iteration in range (0, len(self._index_finger_tip_x)-1):
                x1 = int(self._index_finger_tip_x[iteration] * self._camera_width)
                y1 = int(self._index_finger_tip_y[iteration] * self._camera_height)
                x2 = int(self._index_finger_tip_x[iteration + 1] * self._camera_width)
                y2 = int(self._index_finger_tip_y[iteration + 1] * self._camera_height)
                cv2.line(image, (x1, y1), (x2, y2), self._tip_color, 3)

            cv2.circle(image, (x1, y1), 3, self._tip_color, 3)

            for iteration in range (0, len(self._thumb_finger_tip_x)-1):
                x1 = int(self._thumb_finger_tip_x[iteration] * self._camera_width)
                y1 = int(self._thumb_finger_tip_y[iteration] * self._camera_height)
                x2 = int(self._thumb_finger_tip_x[iteration + 1] * self._camera_width)
                y2 = int(self._thumb_finger_tip_y[iteration + 1] * self._camera_height)
                cv2.line(image, (x1, y1), (x2, y2), self._tip_color, 3)

            cv2.circle(image, (x1, y1), 3, self._tip_color, 3)

        while len(self._index_finger_tip_x) > self._max_tip_point:
            self._index_finger_tip_x.pop(0)
            self._index_finger_tip_y.pop(0)
            self._thumb_finger_tip_x.pop(0)
            self._thumb_finger_tip_y.pop(0)