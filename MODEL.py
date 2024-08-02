
import numpy as np
import matplotlib.pyplot as plt
import csv

def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []

    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []

        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)

        path_XYs.append(XYs)

    return path_XYs

# def plot_paths(paths_XYs):
#     fig, ax = plt.subplots(tight_layout=True, figsize=(8, 8))

#     for i, XYs in enumerate(paths_XYs):
#         for XY in XYs:
#             ax.plot(XY[:, 0], XY[:, 1], linewidth=2)

#     ax.set_aspect('equal')
#     plt.show()

def is_straight_line(XY, dynamic_tolerance_factor=100):
    if len(XY) < 2:
        return False  # A single point or empty path cannot form a straight line
    
    dx = XY[1:, 0] - XY[:-1, 0]
    dy = XY[1:, 1] - XY[:-1, 1]
    if np.any(dx == 0):  # Avoid division by zero for vertical lines
        return False
    
    slopes = dy / dx
    
    slope_std = np.std(slopes)
    tolerance = dynamic_tolerance_factor * slope_std
    
    is_straight = np.all(np.abs(slopes - slopes[0]) < tolerance)
    
    return is_straight

def is_circle(XY, tolerance=100):
    center = np.mean(XY, axis=0)
    radii = np.sqrt((XY[:, 0] - center[0])**2 + (XY[:, 1] - center[1])**2)
    return np.all(np.abs(radii - radii[0]) < tolerance)

def line_to_bezier(XY):
    p0 = XY[0]
    p3 = XY[-1]
    p1 = p0 + (p3 - p0) / 3
    p2 = p0 + 2 * (p3 - p0) / 3
    return np.array([p0, p1, p2, p3])

# def circle_to_bezier(radius, center):
#     # Calculate control points for each quadrant of the circle
#     k = 4 * (np.sqrt(2) - 1) / 3
#     control_points = []
    
#     for i in range(4):
#         angle = np.pi / 2 * i
#         p0 = np.array([np.cos(angle), np.sin(angle)]) * radius + center
#         p1 = np.array([np.cos(angle + np.pi / 4) * k, np.sin(angle + np.pi / 4) * k]) * radius + center
#         p2 = np.array([np.cos(angle + 3 * np.pi / 4) * k, np.sin(angle + 3 * np.pi / 4) * k]) * radius + center
#         p3 = np.array([np.cos(angle + np.pi / 2), np.sin(angle + np.pi / 2)]) * radius + center
#         control_points.append([p0, p1, p2, p3])
    
#     return control_points
def circle_to_bezier(radius, center):
    k = 4 * (np.sqrt(2) - 1) / 3
    control_points = []

    for i in range(4):
        angle = np.pi / 2 * i
        p0 = np.array([np.cos(angle), np.sin(angle)]) * radius + center
        p1 = np.array([np.cos(angle + np.pi / 4) * k, np.sin(angle + np.pi / 4) * k]) * radius + center
        p2 = np.array([np.cos(angle + 3 * np.pi / 4) * k, np.sin(angle + 3 * np.pi / 4) * k]) * radius + center
        p3 = np.array([np.cos(angle + np.pi / 2), np.sin(angle + np.pi / 2)]) * radius + center
        control_points.append([p0, p1, p2, p3])

    return control_points

# def plot_bezier_curve(bezier_points, num_points=100):
#     t = np.linspace(0, 1, num_points)
#     p0, p1, p2, p3 = bezier_points
#     curve = np.outer((1-t)**3, p0) + \
#             np.outer(3*(1-t)**2 * t, p1) + \
#             np.outer(3*(1-t) * t**2, p2) + \
#             np.outer(t**3, p3)
#     plt.plot(curve[:, 0], curve[:, 1])
def is_rectangle(coords, tolerance=1000):
    if len(coords) != 4:
        return False

    def distance(p1, p2):
        return np.linalg.norm(p1 - p2)

    def angle_between(v1, v2):
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        return np.degrees(angle)

    # Calculate the distances between consecutive points
    side_lengths = [distance(coords[i], coords[(i + 1) % 4]) for i in range(4)]
    # Calculate the lengths of the diagonals
    diagonal_lengths = [distance(coords[i], coords[(i + 2) % 4]) for i in range(2)]

    # Check if opposite sides are equal within a tolerance
    if not (np.abs(side_lengths[0] - side_lengths[2]) < tolerance and 
            np.abs(side_lengths[1] - side_lengths[3]) < tolerance):
        return False

    # Check if the diagonals are equal within a tolerance
    if not np.abs(diagonal_lengths[0] - diagonal_lengths[1]) < tolerance:
        return False

    # Calculate the angles between consecutive sides
    angles = [] 
    for i in range(4):
        v1 = coords[(i + 1) % 4] - coords[i]
        v2 = coords[(i + 2) % 4] - coords[(i + 1) % 4]
        angles.append(angle_between(v1, v2))
    # Check if all angles are approximately 90 degrees (allowing a small tolerance)
    if all(80 < angle < 100 for angle in angles):
        return True

    return False

def is_square(coords, tolerance=100000):
    if len(coords) != 4:
        return False
    
    def distance(p1, p2):
        return np.linalg.norm(p1 - p2)

    # Calculate the distances between consecutive points
    side_lengths = [distance(coords[i], coords[(i + 1) % 4]) for i in range(4)]
    # Calculate the lengths of the diagonals
    diagonal_lengths = [distance(coords[i], coords[(i + 2) % 4]) for i in range(2)]

    # Check if all sides are equal within a tolerance
    if not all(np.abs(side_lengths[i] - side_lengths[0]) < tolerance for i in range(1, 4)):
        return False

    # Check if the diagonals are equal within a tolerance
    if not np.abs(diagonal_lengths[0] - diagonal_lengths[1]) < tolerance:
        return False
    return True

def check_for_rectangle(XY, tolerance=1000000):
    num_points = len(XY)
    for start in range(0, num_points - 3):
        for i in range(start + 1, num_points - 2):
            for j in range(i + 1, num_points - 1):
                for k in range(j + 1, num_points):
                    coords = np.array([XY[start], XY[i], XY[j], XY[k]])
                    if is_rectangle(coords, tolerance):
                        return coords
                    # if is_square(coords,tolerance):
                    #     return coords
                    
    return None

def check_for_square(XY, tolerance=1000000):
    num_points = len(XY)    
    for start in range(0, num_points - 3):
        for i in range(start + 1, num_points - 2):
            for j in range(i + 1, num_points - 1):
                for k in range(j + 1, num_points):
                    coords = np.array([XY[start], XY[i], XY[j], XY[k]])
                    print(coords)
                    if is_square(coords, tolerance):
                        return coords
    return None


# Example usage
# XY = np.array([
#     [7.98000002, 0.83999997],
#     [8.98950958, 0.84788334],
#     [9.99900818, 0.85685998],
#     [11.00849438, 0.86692989],
#     [12.01796722, 0.878093]
# ])
# rectangle = check_for_rectangles(XY)
# if rectangle is not None:
#     print("Rectangle found:", rectangle)
# else:
#     print("No rectangle found")



def rectangle_to_bezier(XY):
    bezier_curves = []
    for i in range(4):
        p0 = XY[i]
        p3 = XY[(i+1)%4]
        p1 = p0 + (p3 - p0) / 3
        p2 = p0 + 2 * (p3 - p0) / 3
        bezier_curves.append(np.array([p0, p1, p2, p3]))
    return bezier_curves

def square_to_bezier(XY):
    bezier_curves = []
    for i in range(4):
        p0 = XY[i]
        p3 = XY[(i+1)%4]
        p1 = p0 + (p3 - p0) / 3
        p2 = p0 + 2 * (p3 - p0) / 3
        bezier_curves.append(np.array([p0, p1, p2, p3]))
    return bezier_curves


def plot_bezier_curve(bezier_points, num_points=100):
    t = np.linspace(0, 1, num_points)
    t = t[:, None]  #broadcasting karne keliye 

    p0, p1, p2, p3 = bezier_points
    curve = (1 - t)**3 * p0 + \
            3 * (1 - t)**2 * t * p1 + \
            3 * (1 - t) * t**2 * p2 + \
            t**3 * p3

    plt.plot(curve[:, 0], curve[:, 1])


def save_shapes_to_csv(shapes, csv_path):
    try:
        with open(csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for shape in shapes:
                writer.writerows(shape)  # Write the points directly
        print(f"CSV file created successfully at {csv_path}")
    except Exception as e:
        print(f"Error writing CSV file: {e}")

# Example usage
paths_XYs = read_csv('C:/Users/OM/Downloads/problems/problems/isolated.csv')

shapes = []
for XYs in paths_XYs:
    # print(f'no1:{XYs}')
    
    for XY in XYs:
        # if is_straight_line(XY):
        #     # print(f"Straight line: {XY.tolist()}")
        #     shapes.append(XY.tolist())
        #     bezier_curve = line_to_bezier(XY)
        #     plot_bezier_curve(bezier_curve)
        #     shapes.append(bezier_curve.tolist())
        # print(f'no2:{XY}')
        # if is_circle(XY):
        #     # print(f"Circle: {XY.tolist()}")
        #     center = np.mean(XY, axis=0)
        #     radius = np.mean(np.sqrt((XY[:, 0] - center[0])**2 + (XY[:, 1] - center[1])**2))
        #     bezier_control_points = circle_to_bezier(radius, center)
        #     for bezier_points in bezier_control_points:
        #         plot_bezier_curve(np.array(bezier_points))  # Ensure bezier_points is a NumPy array
        #         shapes.append(np.array(bezier_points).tolist())  # Convert to NumPy array then to list
        # rectangle_coords=check_for_rectangle(XY)
        # print(rectangle_coords)
        #if rectangle_coords is not None:
         #   bezier_curves=rectangle_to_bezier(XY)
          #  print(bezier_curves)    
            #for bezier_curve in bezier_curves:
            #    plot_bezier_curve(bezier_curve)
             #   shapes.append(bezier_curve.tolist())
        square_coords=check_for_square(XY)
        if square_coords is not None:
            bezier_curves=square_to_bezier(XY)
            for bezier_curve in bezier_curves:
                plot_bezier_curve(bezier_curve)
                shapes.append(bezier_curve.tolist())
#       else:
#             print("no shapes detected ")

plt.show()

# # shapes = []
# # for XYs in paths_XYs:
# #     for XY in XYs:
# #         rectangle_coords=check_for_rectangles(XY)
# #         if rectangle_coords is not None:
# #             bezier_curves = rectangle_to_bezier(XY)
# #             for bezier_curve in bezier_curves:
# #                 plot_bezier_curve(bezier_curve)
# #                 shapes.append(bezier_curve.tolist())
# #         else:
# #             print("No rectangle found")
            

# # plt.show()

# # shapes = []
# # for XYs in paths_XYs:
# #     for XY in XYs:
# #         square_coords=check_for_square(XY)
# #         if square_coords is not None:
# #             bezier_curves=square_to_bezier(XY)
# #             for bezier_curve in bezier_curves:
# #                 plot_bezier_curve(bezier_curve)
# #                 shapes.append(bezier_curve.tolist())
# #         else:
# #             print("No rectangle found")
            

# # plt.show()


# # shapes = []
# # for XYs in paths_XYs:
# #     for XY in XYs:
# #         if is_circle(XY):
# #             print(f"Circle: {XY.tolist()}")
# #             center = np.mean(XY, axis=0)
# #             radius = np.mean(np.sqrt((XY[:, 0] - center[0])**2 + (XY[:, 1] - center[1])**2))
# #             bezier_control_points = circle_to_bezier(radius, center)
# #             for bezier_points in bezier_control_points:
# #                 plot_bezier_curve(np.array(bezier_points))  # Ensure bezier_points is a NumPy array
# #                 shapes.append(np.array(bezier_points).tolist())  # Convert to NumPy array then to list
# #         else:
# #             print("no")

# # plt.show()
# # print("Shapes detected:")
# # for shape in shapes:
# #     print(shape)

# csv_path = 'C:/Users/OM/Downloads/problems/identified1_shapes.csv'
# save_shapes_to_csv(shapes, csv_path)
