
import pandas as pd

class BiotaOtolith:

    def __init__(self, sample: dict):
        self.measure_id = sample['measure_id']
        self.sample_id = sample['sample_id']
        self.age = sample['age']
        self.otolith_type = sample['otolith_type']

    def dict(self) -> dict:
        ot = {}
        ot['measure_id'] = self.measure_id
        ot['sample_id'] = self.sample_id
        ot['age'] = self.age
        ot['otolith_type'] = self.otolith_type
        return ot

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
