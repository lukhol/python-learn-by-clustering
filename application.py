import json
import random
import matplotlib.pyplot as plt
import math 

RED = "#F00"
MAX_ITERATIONS = 30
INITIAL_CLUSTERS_COUNT = 4

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(self.x) + hash(self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        # return f"Point({self.x}, {self.y})"
        return self.__dict__.__repr__().replace("'", '"')

POINTS = [
    Point(18.055318559084213, -73.77308436657906),
    Point(123.62080200094903, 53.22377315644087),
    Point(-79.47982281623484, -35.33090176429092),
    Point(-113.97433098789911, -66.25497734946914),
    Point(163.18090554252603, -13.922279490330979),
    Point(-117.03789817635507, -35.54403402377148),
    Point(62.73211375289384, 51.72336290816608),
    Point(26.771535650946078, 40.951181227305426),
    Point(123.28265796262997, -32.822525230004125),
    Point(114.79240166577688, 33.749897822358946),
    Point(-134.14299292817964, 8.955200380202825),
    Point(-100.72687903145496, 1.3171657543764184),
    Point(128.69707347683135, 13.00537101145538),
    Point(-96.98082233058295, -53.635088927202176),
    Point(71.85128835881287, 49.74309621235926),
    Point(178.68417409092473, -87.40273310112214),
    Point(27.76069120806335, 75.63869058831227),
    Point(44.99558260162934, 35.157335928200155),
    Point(145.61816762188494, 42.365434984213664),
    Point(-25.972046619649376, -71.56978205540364) 
]

class Application:
    def __init__(self, count):
        self.points = []
        if count > 0:
            for i in range(count):
                self.points.append(Point(random.uniform(-180, 180), random.uniform(-90, 90)))
            for point in self.points:
                print (point)
        else:
            self.points = list(POINTS)

    def run(self):
        iterations = 1

        medoids, rest_points = find_random_from_list(self.points, INITIAL_CLUSTERS_COUNT) 
        mapping = assign_to_centroids(rest_points, medoids)
        previousMapping = {}

        while(not has_same_keys(mapping, previousMapping) and iterations < MAX_ITERATIONS):
            print(f"medoids count: {len(medoids)}")
            plot_result(rest_points, medoids, mapping, iterations)     
            iterations += 1  

            previousMapping = mapping
            medoids = find_new_medoids(mapping)
            rest_points = list(filter(lambda p : p not in medoids, self.points))
            mapping = assign_to_centroids(rest_points, medoids)

        plot_result(rest_points, medoids, mapping, iterations)     

def has_same_keys(dict1, dict2):
    if(len(dict1) != len(dict2)):
        return False

    for key in dict1.keys():
        if key not in dict2.keys():
            return False

    return True

def find_new_medoids(mapping):
    medoids = []
    for key in mapping.keys():
        points = mapping[key]
        
        if len(points) == 0:
            continue

        x, y = find_center_point_coords(points)
        medoid = find_nearest_to(points, Point(x, y))
        medoids.append(medoid)
    
    return medoids

def print_centroid_and_medoid(mapping):
    for key in mapping.keys():
        points = mapping[key]
        
        if len(points) == 0:
            continue

        x, y = find_center_point_coords(points)
        plt.scatter([x], [y], color = "#ad9c00")

        medoid = find_nearest_to(points, Point(x, y))
        plt.scatter([medoid.x], [medoid.y], color = "#ff00a2")

def assign_to_centroids(points, centroids):
    mapping = {}
    for centroid in centroids:
        mapping[centroid] = []
    
    for point in points:
        smallest_distance_centroid = find_nearest_to(centroids, point)
        mapping[smallest_distance_centroid].append(point)

    return mapping

def find_nearest_to(points, point_to_check):
    smallest_distance = calculate_distance(points[0], point_to_check)
    smallest_distance_point = points[0]
    
    for point in points:
        distance = calculate_distance(point, point_to_check)
        if smallest_distance >= distance:
            smallest_distance = distance
            smallest_distance_point = point

    return smallest_distance_point

def find_random_from_list(points, count):
    copied_points = points.copy()
    count_safe = len(copied_points) if count > len(copied_points) - 1 else count
    rand_points = []

    for i in range(count_safe):
        index = random.randint(0, len(copied_points) - 1)
        point = copied_points[index]
        copied_points.pop(index)
        rand_points.append(point)

    return (
        rand_points,
        copied_points
    )

def find_center_point_coords(points):
    return (
        sum([p.x for p in points])/len(points),
        sum([p.y for p in points])/len(points)
    )

def points_arr_to_x_y_tuples(points):
    return (
        [p.x for p in points],
        [p.y for p in points],
    )

def calculate_distance(p1, p2):
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    return math.sqrt(dx ** 2 + dy ** 2)

# ======================================= PLOT =======================================
def plot_result(rest_points, medoids, mapping, counter):
    plot_points(rest_points)
    plot_points(medoids, color=RED)
    plot_mapping(mapping)
    plt.savefig(f"plot-{counter}")
    plt.clf()

def plot_mapping(mapping):
    for key in mapping.keys():
        centroid = key
        for point in mapping[key]:
            plt.plot([centroid.x, point.x], [centroid.y, point.y], color="#cecece")

def plot_points(points, color=""):
    points_to_plot_tuple = points_arr_to_x_y_tuples(points)
    plt.scatter(points_to_plot_tuple[0], points_to_plot_tuple[1], color = color if color != "" else None)
