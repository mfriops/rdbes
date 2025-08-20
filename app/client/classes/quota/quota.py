#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd

class QuotaQuota:

    def __init__(self, quota: dict):
        self.registration_no = quota['skip_nr']
        self.species_no = quota['ftegund']
        self.quota_type = quota['heimild']
        self.quota = quota['magn']
        self.valid_from = quota['i_gildi']
        self.valid_to = quota['ur_gildi']


    def dict(self) -> dict:
        qu = {}
        qu['registration_no'] = self.registration_no
        qu['species_no'] = self.species_no
        qu['quota_type'] = self.quota_type
        qu['quota'] = self.quota
        qu['valid_from'] = self.valid_from
        qu['valid_to'] = self.valid_to
        return qu

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
