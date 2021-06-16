from hand import Hand
import math
import mouse

class ClickHand(Hand):

    _max_click_distance = 0.2
    _is_clicked = False

    def __init__(self, tip_color, box_color, camera_width, camera_height) -> None:
        super().__init__(tip_color, box_color, camera_width, camera_height, box_left_percentage = 0.15, box_bottom_percentage = 0.2, box_size_to_screen = 0.15)

    def update_finger_tip(self, hand_landmarks, mp_hands, image):
        super().update_finger_tip(hand_landmarks, mp_hands, image, is_smoothen = False)
        self.check_and_execute_click()

    def check_and_execute_click(self):
        is_index_in_box, x_index_in_box, y_index_in_box = self.index_finger_in_box()
        is_thumb_in_box, x_thumb_in_box, y_thumb_in_box = self.thumb_finger_in_box()
        
        if is_index_in_box and is_thumb_in_box:
            distance = math.sqrt( (x_index_in_box - x_thumb_in_box)**2 + (y_index_in_box - y_thumb_in_box)**2)

            # print(distance)
            # print(self._max_click_distance)
            # print(distance < self._max_click_distance)
            # print(self._is_clicked)

            if distance < self._max_click_distance:
                if not self._is_clicked:
                    self._is_clicked = True
                    print("clicked")
                    # mouse.click()
                else:
                    print("dragged")
            else:
                self._is_clicked = False
                print("lose")