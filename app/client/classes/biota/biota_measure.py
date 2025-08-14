#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd

class BiotaMeasure:

    def __init__(self, measure: dict):
        self.measure_id = measure['measure_id']
        self.sample_id = measure['sample_id']
        self.measure_type = measure['measure_type']
        self.length = measure['length']
        self.weight = measure['weight']
        self.sex_no = measure['sex_no']
        self.species_no = measure['species_no']
        self.sexual_maturity_id = measure['sexual_maturity_id']

    def dict(self) -> dict:
        me = {}
        me['measure_id'] = self.measure_id
        me['sample_id'] = self.sample_id
        me['measure_type'] = self.measure_type
        me['length'] = self.length
        me['weight'] = self.weight
        me['sex_no'] = self.sex_no
        me['species_no'] = self.species_no
        me['sexual_maturity_id'] = self.sexual_maturity_id
        return me

    def id(self):
        return self.measure_id

    def species(self):
        return self.species_no

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
