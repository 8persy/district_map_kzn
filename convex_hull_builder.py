import random
import numpy as np
import pandas as pd


class ConvexHullBuilder:
    def __init__(self, points: pd.DataFrame):
        self.__points = points

    def get_convex_hull(self) -> pd.DataFrame:
        def generate_random_color():
            return "#{:06x}".format(random.randint(0, 0xFFFFFF))

        def leftmost_point(points):
            return min(points, key=lambda p: (p[0], p[1]))

        def orientation(p, q, r):
            val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
            if val == 0:
                return 0  # collinear
            elif val > 0:
                return 1  # clockwise
            else:
                return 2  # counterclockwise

        def algorithm(points):
            n = len(points)
            if n < 3:
                return points

            hull = []

            l = leftmost_point(points)
            p = l
            while True:
                hull.append(p)
                q = points[0]
                for r in points:
                    if (q == p) or (orientation(p, q, r) == 2):
                        q = r

                p = q
                if p == l:
                    break

            return hull

        result = []

        for district, group in self.__points.groupby('district'):
            points = group[['lat', 'lon']].values.tolist()

            if len(points) < 3:
                hull_points = points
            else:
                hull_points = algorithm(points)

            center = tuple(np.mean(hull_points, axis=0))
            color = generate_random_color()

            result.append({
                'district': district,
                'points': hull_points,
                'center': center,
                'color': color
            })

        return pd.DataFrame(result)