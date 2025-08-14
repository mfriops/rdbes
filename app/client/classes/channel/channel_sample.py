#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd

class ChannelSample:

    def __init__(self, sample: dict):
        self.sample_id = sample['sample_id']
        self.station_id = sample['station_id']
        self.sample_category_no = sample['sample_category_no']
        self.land_sample = sample['land_sample']
        self.tow_start = sample['tow_start']
        self.tow_end = sample['tow_end']
        self.time_measure = sample['time_measure']
        self.mesh_size = sample['mesh_size']
        self.isscfg_no = sample['isscfg_no']
        self.target_assemblage = 'SPF'

    def dict(self) -> dict:
        st = {}
        st['sample_id'] = self.sample_id
        st['station_id'] = self.station_id
        st['sample_category_no'] = self.sample_category_no
        st['land_sample'] = self.land_sample
        st['tow_start'] = self.tow_start
        st['tow_end'] = self.tow_end
        st['time_measure'] = self.time_measure
        st['mesh_size'] = self.mesh_size
        st['isscfg_no'] = self.isscfg_no
        st['target_assemblage'] = self.target_assemblage
        return st

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
