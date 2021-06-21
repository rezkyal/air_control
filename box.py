import cv2

class Box:

    _box_start_point = (0, 0)
    _box_end_point = (0, 0)
    _box_color = (0, 0, 0)

    _camera_width = 0
    _camera_height = 0

    def __init__(self, camera_width, camera_height, box_color, box_left_percentage, box_bottom_percentage, box_size_to_screen) -> None:
        self._camera_width = camera_width
        self._camera_height = camera_height
        self._box_color = box_color
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

    def finger_in_box(self, centroid_x, centroid_y):
        centroid_x_in_camera = centroid_x * self._camera_width
        centroid_y_in_camera = centroid_y * self._camera_height

        is_x_in_box = self._box_start_point[0] <= centroid_x_in_camera <= self._box_end_point[0]
        is_y_in_box = self._box_start_point[1] <= centroid_y_in_camera <= self._box_end_point[1]

        if is_x_in_box and is_y_in_box:
            x_in_box_percentage = (centroid_x_in_camera - self._box_start_point[0]) / (self._box_end_point[0] - self._box_start_point[0])
            y_in_box_percentage = (centroid_y_in_camera - self._box_start_point[1]) / (self._box_end_point[1] - self._box_start_point[1])

            return True, x_in_box_percentage, y_in_box_percentage
        else:
            return False, 0, 0