from constant import stabilize_type

STABILIZER_FUNCTION_POINTER = stabilize_type.SMOOTH_MOVE_WITH_MINIMUM_ANGLE
STABILIZER_FUNCTION_CLICK = stabilize_type.SMOOTH_MOVE_WITH_MINIMUM_ANGLE

# Stabilizer setting
# used in SMOOTH_MOVE and SMOOTH_MOVE_WITH_MINIMUM_ANGLE, the higher the point the slower and smoother the movement
SMOOTHING_POINT = 30

# used in SMOOTH_MOVE_WITH_MINIMUM_ANGLE, minimum tip point tracked before calculate angle
MINIMUM_TIP_POINT_TO_CALCULATE_ANGLE = 2

# used in SMOOTH_MOVE_WITH_MINIMUM_ANGLE, how much minimum the angle between current and latest tip point to use slow function
MINIMUM_ANGLE_DEGREE = 178

# used in CENTROID_1 and CENTROID_2, minimum tip point tracked before calculate centroid
MINIMUM_TIP_POINT_TO_CALCULATE_CENTROID = 5

# used in CENTROID_1 and CENTROID_2, distance between tip point and centroid to know if the tip is really moving or not
MAXIMUM_CENTROID_DISTANCE = (1E-3*3)