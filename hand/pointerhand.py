from settings.hand_settings import IS_POINTER_HAND_ON, MAX_TIP_POINTS, POINTER_HAND_BOTTOM_BOX_PERCENTAGE, POINTER_HAND_BOX_COLOR, POINTER_HAND_BOX_SIZE_TO_SCREEN, POINTER_HAND_LEFT_BOX_PERCENTAGE, POINTER_HAND_TIP_POINT_COLORS
from box import Box
from .hand import Hand
import mouse
from settings.stabilizer_settings import STABILIZER_FUNCTION_POINTER

class PointerHand(Hand):

    _monitor_width = 0
    _monitor_height = 0

    POINTER_HAND_BOX_NAME = "pointer"

    _pointer_box = None

    def __init__(self, camera_width, camera_height, monitor_width, monitor_height) -> None:
        super().__init__(POINTER_HAND_TIP_POINT_COLORS, camera_width, camera_height, MAX_TIP_POINTS, STABILIZER_FUNCTION_POINTER)
        self._pointer_box = Box(camera_width, camera_height, POINTER_HAND_BOX_COLOR, POINTER_HAND_LEFT_BOX_PERCENTAGE, POINTER_HAND_BOTTOM_BOX_PERCENTAGE, POINTER_HAND_BOX_SIZE_TO_SCREEN, self.POINTER_HAND_BOX_NAME)
        self._monitor_width = monitor_width
        self._monitor_height = monitor_height

    def draw_box(self, image):
        self._pointer_box.draw_box(image)

    def update_finger_tip(self, hand_landmarks, mp_hands, image):
        super().update_finger_tip(hand_landmarks, mp_hands, image)
        self.move_cursor()

    def move_cursor(self):
        if len(self._index_finger_tip_x) > 1:
            is_finger_in_box, x_in_box_percentage, y_in_box_percentage = self._pointer_box.finger_in_box(self._index_finger_centroid[0], self._index_finger_centroid[1])

            if is_finger_in_box:
                x_mouse_monitor = x_in_box_percentage * self._monitor_width
                y_mouse_monitor = y_in_box_percentage * self._monitor_height

                if IS_POINTER_HAND_ON:
                    print(x_mouse_monitor, y_mouse_monitor)
                    mouse.move(x_mouse_monitor, y_mouse_monitor)
