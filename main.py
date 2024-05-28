# import pandas as pd
# from convex_hull_builder import ConvexHullBuilder
#
# # Поменяйте путь на свой
# PATH_TO_SAVE = "data.csv"
#
# points_df = pd.read_csv("points.csv")
#
# builder = ConvexHullBuilder(points_df)
#
# result_df = builder.get_convex_hull()
#
# result_df.to_csv(PATH_TO_SAVE, index=False)

import pandas as pd
from map_renderer import MapRenderer

points_df = pd.read_csv("points.csv")
districts_df = pd.read_csv("data.csv")

renderer = MapRenderer(districts_df, points_df)

renderer.get_map()