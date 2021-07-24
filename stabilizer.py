from settings.stabilizer_settings import MAXIMUM_CENTROID_DISTANCE, MINIMUM_ANGLE_DEGREE, MINIMUM_TIP_POINT_TO_CALCULATE_CENTROID, SMOOTHING_POINT
from calculate_function import find_angle, find_centroid
from constant.stabilize_type import CALCULATE_CENTROID_1, CALCULATE_CENTROID_2, NO_STABILIZER, SMOOTH_MOVE, SMOOTH_MOVE_WITH_MINIMUM_ANGLE
import math

def get_stabilize_function (stabilize_type):
    if stabilize_type == CALCULATE_CENTROID_1:
        return calculate_centroid_1
    elif stabilize_type == CALCULATE_CENTROID_2:
        return calculate_centroid_2
    elif stabilize_type == SMOOTH_MOVE:
        return smooth_move
    elif stabilize_type == SMOOTH_MOVE_WITH_MINIMUM_ANGLE:
        return smooth_move_with_minimum_angle
    elif stabilize_type == NO_STABILIZER:
        return no_stabilizer
    else:
        return no_stabilizer


def no_stabilizer (finger_tip_x : list, finger_tip_y : list, _ : list):
    x_point = finger_tip_x[len(finger_tip_x) - 1]
    y_point = finger_tip_y[len(finger_tip_y) - 1]

    return [x_point, y_point]

def calculate_centroid_1 (finger_tip_x : list, finger_tip_y : list, last_position : list):
    if len(finger_tip_x) > 0:
        x_point = finger_tip_x[len(finger_tip_x) - 1]
        y_point = finger_tip_y[len(finger_tip_y) - 1]

        if len(last_position) == 0:
            return [x_point, y_point]
        
        if len(finger_tip_x) >= MINIMUM_TIP_POINT_TO_CALCULATE_CENTROID:
            last_centroid_x = last_position[0]
            last_centroid_y = last_position[1]
            new_centroid_x, new_centroid_y = find_centroid(finger_tip_x, finger_tip_y)
            
            distance = math.sqrt( (last_centroid_x - new_centroid_x)**2 + (last_centroid_y - new_centroid_y)**2 )

            if distance > MAXIMUM_CENTROID_DISTANCE:
                return [new_centroid_x, new_centroid_y]
            else :
                return last_position
        else:
            return [x_point, y_point]
    else:
        return []

def calculate_centroid_2 (finger_tip_x : list, finger_tip_y : list, _):
    x_point = finger_tip_x[len(finger_tip_x) - 1]
    y_point = finger_tip_y[len(finger_tip_y) - 1]

    last_x = finger_tip_x[len(finger_tip_x) - 2]
    last_y = finger_tip_y[len(finger_tip_y) - 2]

    x_centroid, y_centroid = find_centroid(finger_tip_x, finger_tip_y)

    distance = math.sqrt( (x_point - x_centroid)**2 + (y_point - y_centroid)**2 )

    if distance > MAXIMUM_CENTROID_DISTANCE:
        is_not_moving = False
    else :
        is_not_moving = True

    if is_not_moving:
        finger_tip_x.clear()
        finger_tip_y.clear()

        for _ in range(0, MINIMUM_TIP_POINT_TO_CALCULATE_CENTROID):
            finger_tip_x.append(last_x)
            finger_tip_y.append(last_y)

        return [last_x, last_y]
    else:
        return [x_point, y_point]

def smooth_move(finger_tip_x : list, finger_tip_y : list, _):
    new_x_point = finger_tip_x[len(finger_tip_x) - 1]
    new_y_point = finger_tip_y[len(finger_tip_y) - 1]

    last_old_x = finger_tip_x[len(finger_tip_x) - 2]
    last_old_y = finger_tip_y[len(finger_tip_y) - 2]

    x_point = last_old_x + (new_x_point - last_old_x) / SMOOTHING_POINT
    y_point = last_old_y + (new_y_point - last_old_y) / SMOOTHING_POINT
        
    return [x_point, y_point]

def smooth_move_with_minimum_angle(finger_tip_x : list, finger_tip_y : list, _):
    MINIMUM_LAST_TIP_POINT_TO_CALCULATE_ANGLE = 2

    new_x_point = finger_tip_x[len(finger_tip_x) - 1]
    new_y_point = finger_tip_y[len(finger_tip_y) - 1]
        
    if(len(finger_tip_x) >= MINIMUM_LAST_TIP_POINT_TO_CALCULATE_ANGLE) :
        
        last_x = finger_tip_x[len(finger_tip_x) - 2]
        last_y = finger_tip_y[len(finger_tip_y) - 2]

        before_last_x = finger_tip_x[len(finger_tip_x) - 3]
        before_last_y = finger_tip_y[len(finger_tip_y) - 3]
        
        vA = [(last_x - new_x_point), (last_y - new_y_point)]
        vB = [(last_x - before_last_x), (last_y - before_last_y)]

        angle = find_angle(vA, vB)

        if angle < MINIMUM_ANGLE_DEGREE:
            return smooth_move(finger_tip_x, finger_tip_y, _)
    
    return [new_x_point, new_y_point]