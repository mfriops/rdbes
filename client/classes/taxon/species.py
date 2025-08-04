
import pandas as pd

class TaxonSpecies:

    def __init__(self, species: dict):
        self.species_no = species['species_no']
        self.worms_id = species['worms_id']
        self.code_3a = species['code_3a']
        self.name = species['name']
        self.eng_name = species['eng_name']

    def dict(self) -> dict:
        sp = {}
        sp['species_no'] = self.species_no
        sp['worms_id'] = self.worms_id
        sp['code_3a'] = self.code_3a
        sp['name'] = self.name
        sp['eng_name'] = self.eng_name
        return sp

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
