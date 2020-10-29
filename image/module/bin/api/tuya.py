import os
from time import sleep
from tuyapy import TuyaApi


class Tuya:
    def __init__(self):
        raise Exception("Do not instanciate class")

    @staticmethod
    def __api__():
        api = TuyaApi()
        api.init(
            os.environ["API_USERNAME"],
            os.environ["API_PASSWORD"],
            os.environ["API_COUNTRY_CODE"],
        )
        return api

    @classmethod
    def get_objects(cls, type=None, name=None):
        objs = cls.__api__().get_all_devices()
        if type:
            objs = [obj for obj in objs if obj.obj_type == type]
        if name:
            objs = [obj for obj in objs if obj.name().startswith(name)]
        return objs
