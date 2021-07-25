from settings.hand_settings import CLICK_HAND_BOX_COLOR, CLICK_HAND_LEFT_CLICK_BOTTOM_BOX_POSITION_PERCENTAGE, CLICK_HAND_LEFT_CLICK_BOX_SIZE_TO_SCREEN, CLICK_HAND_LEFT_CLICK_LEFT_BOX_POSITION_PERCENTAGE, CLICK_HAND_RIGHT_CLICK_BOTTOM_BOX_POSITION_PERCENTAGE, CLICK_HAND_RIGHT_CLICK_BOX_SIZE_TO_SCREEN, CLICK_HAND_RIGHT_CLICK_LEFT_BOX_POSITION_PERCENTAGE, CLICK_HAND_TIP_POINT_COLORS, IS_CLICK_HAND_ON, MAX_CLICK_DISTANCE, MAX_TIP_POINTS
from constant.click_state import CLICK_STATE, DISPLAY_FORMAT, DRAG_STATE, POINTER_STATE
from constant.release_state import RELEASE_STATE, PRESS_STATE
from box import Box
from .hand import Hand
import math
import mouse
from settings.stabilizer_settings import STABILIZER_FUNCTION_CLICK

class ClickHand(Hand):
    _is_pressed = True
    _current_release_state_count = 0
    _current_release_state = RELEASE_STATE

    _current_click_state = POINTER_STATE

    _selected_hand = None

    _left_click_box = None
    _right_click_box = None

    MINIMUM_POINTER_STATE_COUNT = 3

    LEFT_CLICK_BOX_NAME = "left click"
    RIGHT_CLICK_BOX_NAME = "right click"

    _box_start_point = (0, 0)
    _box_end_point = (0, 0)
    _box_color = (0, 0, 0)

    def __init__(self, camera_width, camera_height) -> None:
        super().__init__(CLICK_HAND_TIP_POINT_COLORS, camera_width, camera_height, MAX_TIP_POINTS, STABILIZER_FUNCTION_CLICK)
        self._left_click_box = Box(camera_width, camera_height, CLICK_HAND_BOX_COLOR, CLICK_HAND_LEFT_CLICK_LEFT_BOX_POSITION_PERCENTAGE, CLICK_HAND_LEFT_CLICK_BOTTOM_BOX_POSITION_PERCENTAGE, CLICK_HAND_LEFT_CLICK_BOX_SIZE_TO_SCREEN, self.LEFT_CLICK_BOX_NAME)
        self._right_click_box = Box(camera_width, camera_height, CLICK_HAND_BOX_COLOR, CLICK_HAND_RIGHT_CLICK_LEFT_BOX_POSITION_PERCENTAGE, CLICK_HAND_RIGHT_CLICK_BOTTOM_BOX_POSITION_PERCENTAGE, CLICK_HAND_RIGHT_CLICK_BOX_SIZE_TO_SCREEN, self.RIGHT_CLICK_BOX_NAME)

    def draw_box(self, image):
        self._right_click_box.draw_box(image)
        self._left_click_box.draw_box(image)

    def update_finger_tip(self, hand_landmarks, mp_hands, image):
        super().update_finger_tip(hand_landmarks, mp_hands, image)
        self.check_and_execute_click(mouse.LEFT)
        self.check_and_execute_click(mouse.RIGHT)

    def check_and_execute_click(self, button = mouse.LEFT):
        if button == mouse.LEFT:
            click_box = self._left_click_box
        elif button == mouse.RIGHT:
            click_box = self._right_click_box

        is_index_in_box, x_index_in_box, y_index_in_box = click_box.finger_in_box(self._index_finger_position[0], self._index_finger_position[1])
        is_thumb_in_box, x_thumb_in_box, y_thumb_in_box = click_box.finger_in_box(self._thumb_finger_position[0], self._thumb_finger_position[1])
        
        if is_index_in_box and is_thumb_in_box:
            self._selected_hand = button

            distance = math.sqrt( (x_index_in_box - x_thumb_in_box)**2 + (y_index_in_box - y_thumb_in_box)**2)
            
            if distance < MAX_CLICK_DISTANCE:
                if not self._is_pressed:
                    if self._current_release_state == PRESS_STATE:
                        self._current_release_state_count = 0

                    self._current_release_state = PRESS_STATE
                    self._current_release_state_count = self._current_release_state_count + 1

                    self._is_pressed = True
                    self._current_click_state = DISPLAY_FORMAT.format(state = CLICK_STATE, button = button)
                    if IS_CLICK_HAND_ON:
                        mouse.press(button = button)
                else:
                    self._current_click_state = DISPLAY_FORMAT.format(state = DRAG_STATE, button = button)
            else:
                if self._current_release_state != RELEASE_STATE:
                    self._current_release_state_count = 0

                self._current_release_state = RELEASE_STATE
                self._current_release_state_count = self._current_release_state_count + 1
                if self._current_release_state == RELEASE_STATE and self._current_release_state_count >= self.MINIMUM_POINTER_STATE_COUNT and self._is_pressed:
                    if IS_CLICK_HAND_ON:
                        mouse.release(button = button)
                    self._is_pressed = False
                    self._current_click_state = POINTER_STATE
        else:
            if self._selected_hand == button:
                self._selected_hand = None
                self._is_pressed = False
                self._current_release_state_count = 0
                self._current_click_state = POINTER_STATE
                self._current_release_state = RELEASE_STATE
                mouse.release(button = button)

    def get_current_click_state(self):
        return self._current_click_state