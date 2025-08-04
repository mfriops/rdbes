
import pandas as pd

class AdbTrawlAndSeineNet:

    def __init__(self, fg: dict):
        self.fishing_station_id = fg['fishing_station_id']
        self.headline = fg['headline']
        self.bridle = fg['bridle']
        self.mesh_size = fg['mesh_size']
        self.mesh_type = fg['mesh_type']
        self.grid_no = fg['grid_no']
        self.square_window = fg['square_window']
        self.otterboard_weight = fg['otterboard_weight']
        self.circumference_mesh_number = fg['circumference_mesh_number']
        self.rope = fg['rope']
        self.two_fg = fg['two_fg']

    def dict(self) -> dict:
        fg = {}
        fg['fishing_station_id'] = self.fishing_station_id
        fg['headline'] = self.headline
        fg['bridle'] = self.bridle
        fg['mesh_size'] = self.mesh_size
        fg['mesh_type'] = self.mesh_type
        fg['grid_no'] = self.grid_no
        fg['square_window'] = self.square_window
        fg['otterboard_weight'] = self.otterboard_weight
        fg['circumference_mesh_number'] = self.circumference_mesh_number
        fg['rope'] = self.rope
        fg['two_fg'] = self.two_fg
        return fg

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
