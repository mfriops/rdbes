
import pandas as pd

class Harbour:

    def __init__(self, port: dict):
        self.port_no = port['port_no']
        self.harbour = port['locode']

    def dict(self) -> dict:
        ha = {}
        ha['port_no'] = self.port_no
        ha['harbour'] = self.harbour
        return ha

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
