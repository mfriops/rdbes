#!/usr/local/bin/python3
# coding: utf-8

import pandas as pd

class AgfLandings:

    def __init__(self, landing: dict):
        self.usage = landing['afdrif']
        self.condition = landing['astand']
        self.closed = landing['er_lokud']
        self.species_no = landing['fisktegund']
        self.processing = landing['fullvinnsla']
        self.storage = landing['geymsluadferd']
        self.landing_port_no = landing['hafnarnumer']
        self.landing_start = landing['londun_hefst']
        self.landing_id = landing['londun_id']
        self.weight = landing['magn']
        self.weight_ungutted = landing['magn_oslaegt']
        self.weight_gutted = landing['magn_slaegt']
        self.registration_no = landing['skip_numer']
        self.status = landing['stada']
        self.fishing_gear_no = landing['veidarfaeri']
        self.fishing_stock_no = landing['veidistofn']
        self.fishing_area = landing['veidisvaedi']
        self.weight_type = landing['vigtunartegund']


    def dict(self) -> dict:
        la = {}
        la['usage'] = self.usage
        la['condition'] = self.condition
        la['closed'] = self.closed
        la['species_no'] = self.species_no
        la['processing'] = self.processing
        la['storage'] = self.storage
        la['landing_port_no'] = self. landing_port_no
        la['landing_start'] = self.landing_start
        la['landing_id'] = self.landing_id
        la['weight'] = self.weight
        la['weight_ungutted'] = self. weight_ungutted
        la['weight_gutted'] = self.weight_gutted
        la['registration_no'] = self.registration_no
        la['status'] = self.status
        la['fishing_gear_no'] = self.fishing_gear_no
        la['fishing_stock_no'] = self.fishing_stock_no
        la['fishing_area'] = self.fishing_area
        la['weight_type'] = self.weight_type
        return la

    def pand(self) -> pd.DataFrame:
        return pd.DataFrame([self.dict()])
