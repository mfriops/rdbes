import pandas as pd


class BiotaSexualMaturity:

    def __init__(self, sample: dict):
        self.sexual_maturity_id = sample['sexual_maturity_id']
        self.sexual_maturity_no = sample['sexual_maturity_no']

    def dict(self) -> dict:
        sm = {}
        sm['sexual_maturity_id'] = self.sexual_maturity_id
        sm['sexual_maturity_no'] = self.sexual_maturity_no
        return sm

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
