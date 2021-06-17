import math

SMOOTHENING_POINT = 30
MINIMUM_POINT_TO_CALCULATE_ANGLE = 2
MINIMUM_POINT_TO_CALCULATE_CENTROID = 5
MINIMUM_ANGLE_DEGREE = 178
MAXIMUM_CENTROID_DISTANCE = (1E-2)

def stabilize(x_point, y_point, index_finger_tip_x : list, index_finger_tip_y : list, is_calculate_centroid = True, is_smoothen = True):
    
    if(is_calculate_centroid):
        if(len(index_finger_tip_x) >= MINIMUM_POINT_TO_CALCULATE_CENTROID):
            last_x = index_finger_tip_x[len(index_finger_tip_x) - 1]
            last_y = index_finger_tip_y[len(index_finger_tip_y) - 1]

            is_not_moving = find_if_moving(x_point, y_point, index_finger_tip_x, index_finger_tip_y)
            if is_not_moving:
                index_finger_tip_x.clear()
                index_finger_tip_y.clear()

                for _ in range(0, MINIMUM_POINT_TO_CALCULATE_CENTROID):
                    index_finger_tip_x.append(last_x)
                    index_finger_tip_y.append(last_y)

                return last_x, last_y

    if is_smoothen :    
        if(len(index_finger_tip_x) >= MINIMUM_POINT_TO_CALCULATE_ANGLE) :
            last_x = index_finger_tip_x[len(index_finger_tip_x) - 1]
            last_y = index_finger_tip_y[len(index_finger_tip_y) - 1]

            before_last_x = index_finger_tip_x[len(index_finger_tip_x) - 2]
            before_last_y = index_finger_tip_y[len(index_finger_tip_y) - 2]
            
            vA = [(last_x - x_point), (last_y - y_point)]
            vB = [(last_x - before_last_x), (last_y - before_last_y)]

            angle = ang(vA, vB)

            if angle < MINIMUM_ANGLE_DEGREE:
                return smoothen_point(x_point, y_point, last_x, last_y)

    return x_point, y_point

def find_if_moving(x_point, y_point, index_finger_tip_x, index_finger_tip_y):
    x_sum = sum(index_finger_tip_x)
    x_total = len(index_finger_tip_x)

    y_sum = sum(index_finger_tip_y)
    y_total = len(index_finger_tip_y)

    x_centroid = x_sum/x_total
    y_centroid = y_sum/y_total

    distance = math.sqrt( (x_point - x_centroid)**2 + (y_point - y_centroid)**2 )

    if distance > MAXIMUM_CENTROID_DISTANCE:
        # print(distance)
        return False
    else :
        return True

def smoothen_point(x_point, y_point, last_x, last_y):
    x_point = last_x + (x_point - last_x) / SMOOTHENING_POINT
    y_point = last_y + (y_point - last_y) / SMOOTHENING_POINT
        
    return x_point, y_point

def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]

def ang(vA, vB):
    # Get nicer vector form
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5

    # If same point, then 0 degree
    if magA == 0 or magB == 0:
        return 0

    # Get cosine value
    cos_ = dot_prod/magA/magB
    # Get angle in radians and then convert to degrees
    angle = math.acos(cos_)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle)%360

    if ang_deg-180>=0:
        # As in if statement
        return 360 - ang_deg
    else: 
        return ang_deg
