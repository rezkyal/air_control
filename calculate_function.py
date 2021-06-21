import math

def _dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]

def find_angle(vA, vB):
    # Get nicer vector form
    # Get _dot prod
    dot_prod = _dot(vA, vB)
    # Get magnitudes
    magA = _dot(vA, vA)**0.5
    magB = _dot(vB, vB)**0.5

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

def find_centroid(finger_tip_x : list, finger_tip_y : list):
    x_sum = sum(finger_tip_x)
    x_total = len(finger_tip_x)

    y_sum = sum(finger_tip_y)
    y_total = len(finger_tip_y)

    x_centroid = x_sum/x_total
    y_centroid = y_sum/y_total

    return x_centroid, y_centroid