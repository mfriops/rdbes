
import pandas as pd

class GearIsscfg:

    def __init__(self, gear: dict):
        self.isscfg_no = gear['isscfg_no']
        self.gear_category = gear['gear_category']
        self.stand_no = gear['stand_no']

    def dict(self) -> dict:
        iss = {}
        iss['isscfg_no'] = self.isscfg_no
        iss['gear_category'] = self.gear_category
        iss['stand_no'] = self.stand_no
        return iss

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
