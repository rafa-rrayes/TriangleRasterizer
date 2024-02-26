import numpy as np
def find_intersection(camera_position, camera_direction, distance_to_plane, point):
    """
    Calculate the intersection of a line and a plane in 3D using NumPy.
    
    Parameters:
    - plane: A tuple (A, B, C, D) representing the plane equation Ax + By + Cz + D = 0.
    - line: A tuple ((x0, y0, z0), (dx, dy, dz)) representing the line.
    
    Returns:
    - The intersection point as a NumPy array [x, y, z], or None if there is no intersection.
    """
    D = distance_to_plane
    A, B, C = camera_direction
    x0, y0, z0 = camera_position
    dx, dy, dz = point
    
    # Create a vector for the coefficients of t in the linear equation
    direction_vector = np.array([dx, dy, dz])
    normal_vector = np.array([A, B, C])
    
    # Check if the line is parallel to the plane
    if np.dot(direction_vector, normal_vector) == 0:
        return None  # No intersection, the line is parallel to the plane
    
    # Solve for t
    t = -(A * x0 + B * y0 + C * z0 + D) / np.dot(direction_vector, normal_vector)
    if t < 0:
        return None
    # Calculate the intersection point
    intersection_point = np.array([x0, y0, z0]) + t * direction_vector
    
    return intersection_point

# Example usage
distance_to_plane = 3
point = (1, 2, 3)  # Point on the line
camera_position = (0, 0, 0)  # Camera position
camera_direction = (1, 1, 1)  # Camera direction
intersection_point = find_intersection(camera_position, camera_direction, distance_to_plane, point)
# find intersection for 1000 points
import random
import time
tempo = time.time()
for i in range(3000):
    point = (random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10))
    intersection_point = find_intersection(camera_position, camera_direction, distance_to_plane, point)
print(time.time()-tempo)
print(1/30)