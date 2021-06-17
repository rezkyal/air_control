from box import Box
from constant import PRESS_STATE, RELEASE_STATE
from .hand import Hand
import math
import mouse

class ClickHand(Hand):

    _max_click_distance = 0.2

    _is_left_pressed = False
    _current_left_click_state_count = 0
    _current_left_click_state = ''

    _is_right_pressed = False
    _current_right_click_state_count = 0
    _current_right_click_state = ''


    _left_click_box = None
    _right_click_box = None

    MINIMUM_RELEASE_STATE_COUNT = 3

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
        self.check_and_execute_left_click()
        self.check_and_execute_right_click()

    def check_and_execute_left_click(self):
        is_index_in_box, x_index_in_box, y_index_in_box = self._left_click_box.finger_in_box(self._index_finger_tip_x, self._index_finger_tip_y)
        is_thumb_in_box, x_thumb_in_box, y_thumb_in_box = self._left_click_box.finger_in_box(self._thumb_finger_tip_x, self._thumb_finger_tip_y)
        
        if is_index_in_box and is_thumb_in_box:
            distance = math.sqrt( (x_index_in_box - x_thumb_in_box)**2 + (y_index_in_box - y_thumb_in_box)**2)

            if distance < self._max_click_distance:
                if not self._is_left_pressed:
                    if self._current_left_click_state == PRESS_STATE:
                        self._current_left_click_state_count = 0

                    self._current_left_click_state = PRESS_STATE
                    self._current_left_click_state_count = self._current_left_click_state_count + 1

                    self._is_left_pressed = True
                    print("clicked - left")
                    # mouse.press(button=mouse.LEFT)
                else:
                    print("dragged - left")
            else:
                if self._current_left_click_state != RELEASE_STATE:
                    self._current_left_click_state_count = 0

                self._current_left_click_state = RELEASE_STATE
                self._current_left_click_state_count = self._current_left_click_state_count + 1
                print("lose - left")
                if self._current_left_click_state == RELEASE_STATE and self._current_left_click_state_count >= self.MINIMUM_RELEASE_STATE_COUNT and self._is_left_pressed:
                    # mouse.release(button=mouse.LEFT)
                    self._is_left_pressed = False
                    print("released - left")
        else:
            self._is_left_pressed = False
            self._current_left_click_state_count = 0
            self._current_left_click_state = ''
        

    def check_and_execute_right_click(self):
        is_index_in_box, x_index_in_box, y_index_in_box = self._right_click_box.finger_in_box(self._index_finger_tip_x, self._index_finger_tip_y)
        is_thumb_in_box, x_thumb_in_box, y_thumb_in_box = self._right_click_box.finger_in_box(self._thumb_finger_tip_x, self._thumb_finger_tip_y)
        
        if is_index_in_box and is_thumb_in_box:
            distance = math.sqrt( (x_index_in_box - x_thumb_in_box)**2 + (y_index_in_box - y_thumb_in_box)**2)

            if distance < self._max_click_distance:
                if not self._is_right_pressed:
                    if self._current_right_click_state == PRESS_STATE:
                        self._current_right_click_state_count = 0

                    self._current_right_click_state = PRESS_STATE
                    self._current_right_click_state_count = self._current_right_click_state_count + 1

                    self._is_right_pressed = True
                    print("clicked - right")
                    # mouse.press(button=mouse.RIGHT)
                else:
                    print("dragged - right")
            else:
                if self._current_right_click_state != RELEASE_STATE:
                    self._current_right_click_state_count = 0

                self._current_right_click_state = RELEASE_STATE
                self._current_right_click_state_count = self._current_right_click_state_count + 1
                print("lose - right")
                if self._current_right_click_state == RELEASE_STATE and self._current_right_click_state_count >= self.MINIMUM_RELEASE_STATE_COUNT and self._is_right_pressed:
                    # mouse.release(button=mouse.RIGHT)
                    self._is_right_pressed = False
                    print("released - right")
        else:
            self._is_right_pressed = False
            self._current_right_click_state_count = 0
            self._current_right_click_state = ''