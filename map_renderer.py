import pandas as pd
import numpy as np
from ipyleaflet import Map, Marker, Polygon, FullScreenControl, LegendControl
from ipywidgets import Layout
import ast


class MapRenderer:
    def __init__(self, district_data: pd.DataFrame, points_data: pd.DataFrame):
        self.__points_data = points_data
        self.__district_data = district_data

    def get_map(self) -> Map:
        # Вычисление центра карты (медианные значения lat и lon)
        center_lat = self.__points_data['lat'].median()
        center_lon = self.__points_data['lon'].median()

        # Создание карты
        m = Map(center=(center_lat, center_lon), zoom=12, layout=Layout(width='100%', height='800px'))

        # Список элементов для легенды
        legend_items = []

        for _, row in self.__district_data.iterrows():
            district_name = row['district']
            points = row['points']
            center = row['center']
            color = row['color']

            # Убедимся, что points является списком кортежей
            if isinstance(points, str):
                points = ast.literal_eval(points)

            print(f"District: {district_name}, Points: {points}, Center: {center}, Color: {color}")  # Отладочный вывод

            # Проверка наличия координат
            if not points:
                print(f"No points for district: {district_name}")
                continue

            # Добавление полигона для района
            polygon = Polygon(
                locations=[(point[0], point[1]) for point in points],
                color=color,
                fill_color=color,
                fill_opacity=0.5,
                weight=2
            )
            m.add_layer(polygon)

            # Добавление маркера в центр района
            marker = Marker(
                location=center,
                draggable=False,
                title=district_name
            )
            m.add_layer(marker)

            # Добавление элемента в легенду
            legend_items.append((district_name, color))

        # Создание легенды
        legend = LegendControl(
            {district_name: color for district_name, color in legend_items},
            name="Legend",
            position="bottomright"
        )
        m.add_control(legend)

        # Добавление элемента управления FullScreen
        m.add_control(FullScreenControl())

        return m