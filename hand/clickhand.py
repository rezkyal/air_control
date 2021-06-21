from constant.click_state import CLICK_STATE, DISPLAY_FORMAT, DRAG_STATE, POINTER_STATE
from constant.release_state import RELEASE_STATE, PRESS_STATE
from box import Box
from .hand import Hand
import math
import mouse

class ClickHand(Hand):
    _max_click_distance = 0.17

    _is_pressed = True
    _current_release_state_count = 0
    _current_release_state = RELEASE_STATE

    _current_click_state = POINTER_STATE

    _selected_hand = None

    _left_click_box = None
    _right_click_box = None

    MINIMUM_POINTER_STATE_COUNT = 3

    _box_start_point = (0, 0)
    _box_end_point = (0, 0)
    _box_color = (0, 0, 0)

    def __init__(self, tip_color, box_color, camera_width, camera_height) -> None:
        super().__init__(tip_color, camera_width, camera_height)
        self._left_click_box = Box(camera_width, camera_height, box_color, box_left_percentage = 0.15, box_bottom_percentage = 0.2, box_size_to_screen = 0.15)
        self._right_click_box = Box(camera_width, camera_height, box_color, box_left_percentage = 0.15, box_bottom_percentage = 0.45, box_size_to_screen = 0.15)

    def draw_box(self, image):
        self._right_click_box.draw_box(image)
        self._left_click_box.draw_box(image)

    def update_finger_tip(self, hand_landmarks, mp_hands, image):
        super().update_finger_tip(hand_landmarks, mp_hands, image, is_smoothen = False)
        self.check_and_execute_click(mouse.LEFT)
        self.check_and_execute_click(mouse.RIGHT)

    def check_and_execute_click(self, button = mouse.LEFT):
        if button == mouse.LEFT:
            click_box = self._left_click_box
        elif button == mouse.RIGHT:
            click_box = self._right_click_box

        is_index_in_box, x_index_in_box, y_index_in_box = click_box.finger_in_box(self._index_finger_centroid[0], self._index_finger_centroid[1])
        is_thumb_in_box, x_thumb_in_box, y_thumb_in_box = click_box.finger_in_box(self._thumb_finger_centroid[0], self._thumb_finger_centroid[1])
        
        if is_index_in_box and is_thumb_in_box:
            self._selected_hand = button

            distance = math.sqrt( (x_index_in_box - x_thumb_in_box)**2 + (y_index_in_box - y_thumb_in_box)**2)
            
            if distance < self._max_click_distance:
                if not self._is_pressed:
                    if self._current_release_state == PRESS_STATE:
                        self._current_release_state_count = 0

                    self._current_release_state = PRESS_STATE
                    self._current_release_state_count = self._current_release_state_count + 1

                    self._is_pressed = True
                    self._current_click_state = DISPLAY_FORMAT.format(state = CLICK_STATE, button = button)
                    # mouse.press(button = button)
                else:
                    self._current_click_state = DISPLAY_FORMAT.format(state = DRAG_STATE, button = button)
            else:
                if self._current_release_state != RELEASE_STATE:
                    self._current_release_state_count = 0

                self._current_release_state = RELEASE_STATE
                self._current_release_state_count = self._current_release_state_count + 1
                if self._current_release_state == RELEASE_STATE and self._current_release_state_count >= self.MINIMUM_POINTER_STATE_COUNT and self._is_pressed:
                    # mouse.release(button = button)
                    self._is_pressed = False
                    self._current_click_state = POINTER_STATE
        else:
            if self._selected_hand == button:
                self._selected_hand = None
                self._is_pressed = False
                self._current_release_state_count = 0
                self._current_click_state = POINTER_STATE
                self._current_release_state = RELEASE_STATE

    def get_current_click_state(self):
        print(self._current_click_state)
        return self._current_click_state