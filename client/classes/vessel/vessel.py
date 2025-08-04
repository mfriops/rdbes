
import pandas as pd

class VesselVessel:

    def __init__(self, vessel: dict):
        self.vessel_id = vessel['vessel_id']
        self.registration_no = vessel['registration_no']
        self.usage_category_no = vessel['usage_category_no']
        self.length = vessel['length']
        self.power_kw = vessel['power_kw']
        self.brutto_weight_tons = vessel['brutto_weight_tons']
        self.home_port_no = vessel['home_port_no']

    def dict(self) -> dict:
        ve = {}
        ve['vessel_id'] = self.vessel_id
        ve['registration_no'] = self.registration_no
        ve['usage_category_no'] = self.usage_category_no
        ve['length'] = self.length
        ve['power_kw'] = self.power_kw
        ve['brutto_weight_tons'] = self.brutto_weight_tons
        ve['home_port_no'] = self.home_port_no
        return ve

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
