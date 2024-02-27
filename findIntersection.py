import numpy as np
def project(camera_position, camera_direction, distance_to_plane, point):
    """
    Calculate the intersection of a line and a plane in 3D using NumPy.
    
    Parameters:
    - plane: A tuple (A, B, C, D) representing the plane equation Ax + By + Cz + D = 0.
    - line: A tuple ((x0, y0, z0), (dx, dy, dz)) representing the line.
    
    Returns:
    - The intersection point as a NumPy array [x, y, z], or None if there is no intersection.
    """
    if distance_to_plane <= 0:
        raise ValueError("The distance to the plane must be positive")
    D = distance_to_plane
    A, B, C = camera_direction
    x0, y0, z0 = camera_position
    dx, dy, dz = point
    #subtract the camera position from the point
    dx -= x0
    dy -= y0
    dz -= z0
    
    # Create a vector for the coefficients of t in the linear equation
    direction_vector = np.array([dx, dy, dz])
    normal_vector = np.array([A, B, C])
    
    # Solve for t
    t2 = (A * x0 + B * y0 + C * z0 + D) / np.dot(normal_vector, normal_vector)
    
    t = (A * x0 + B * y0 + C * z0 + D) / np.dot(direction_vector, normal_vector)

    if t < 0 or t > 1:
        return None
    # Calculate the intersection point
    intersection_point = np.array([x0, y0, z0]) + t * direction_vector
    vector = intersection_point - np.array([A, B, C])*t2
    return (-vector[1], -vector[2])

# # Example usage
# distance_to_plane = 5

# point = (-8, 7,8)  # Point on the line
# camera_position = (0, 0, 0)  # Camera position
# camera_direction = (1, 2, 3)  # Camera direction

# intersection_point = project(camera_position, camera_direction, distance_to_plane, point)
# print(intersection_point)  # Output: [1. 1. 1.]