from hand import Hand
import mouse

class PointerHand(Hand):

    _monitor_width = 0
    _monitor_height = 0

    def __init__(self, tip_color, box_color, camera_width, camera_height) -> None:
        super().__init__(tip_color, box_color, camera_width, camera_height, box_left_percentage = 0.4, box_bottom_percentage = 0.3, box_size_to_screen = 0.45)

    def update_finger_tip(self, hand_landmarks, mp_hands, image):
        super().update_finger_tip(hand_landmarks, mp_hands, image)
        self.move_cursor()

    def move_cursor(self):
        if len(self._index_finger_tip_x) > 1:
            is_finger_in_box, x_in_box_percentage, y_in_box_percentage = self.index_finger_in_box()

            if is_finger_in_box:
                x_mouse_monitor = x_in_box_percentage * self._monitor_width
                y_mouse_monitor = y_in_box_percentage * self._monitor_height

                mouse.move(x_mouse_monitor, y_mouse_monitor)    

    def update_monitor_size(self, monitor_width, monitor_height):
        self._monitor_width = monitor_width
        self._monitor_height = monitor_height