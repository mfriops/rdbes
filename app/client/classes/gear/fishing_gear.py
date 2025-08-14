#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd

class GearFishingGear:

    def __init__(self, gear: dict):
        self.fishing_gear_no = gear['fishing_gear_no']
        self.isscfg_no = gear['isscfg_no']

    def dict(self) -> dict:
        fg = {}
        fg['fishing_gear_no'] = self.fishing_gear_no
        fg['isscfg_no'] = self.isscfg_no
        return fg

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
