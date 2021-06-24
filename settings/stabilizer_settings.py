from constant import stabilize_type

STABILIZER_FUNCTION = stabilize_type.CALCULATE_CENTROID_1

# Stabilizer setting
# used in SLOW_MOVE and SLOW_MOVE_WITH_MINIMUM_ANGLE, the higher the point the slower the movement
SLOWING_POINT = 30

# used in SLOW_MOVE_WITH_MINIMUM_ANGLE, minimum tip point tracked before calculate angle
MINIMUM_TIP_POINT_TO_CALCULATE_ANGLE = 2

# used in SLOW_MOVE_WITH_MINIMUM_ANGLE, how much minimum the angle between current and latest tip point to use slow function
MINIMUM_ANGLE_DEGREE = 178

# used in CENTROID_1 and CENTROID_2, minimum tip point tracked before calculate centroid
MINIMUM_TIP_POINT_TO_CALCULATE_CENTROID = 5

# used in CENTROID_1 and CENTROID_2, distance between tip point and centroid to know if the tip is really moving or not
MAXIMUM_CENTROID_DISTANCE = (1E-3*3)