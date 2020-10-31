#!/usr/bin/env python3
import multiprocessing as mp
import os
import socket
import yaml
from time import sleep, strftime
from api.tuya import Tuya


def _is_up(ip):
    status = False
    for i in range(0, 5):
        sleep(i * 1)
        try:
            with socket.create_connection((ip, 6668), 0.1):
                status = True
                break
        except:
            pass
    return (ip, status)


class Room:
    def __init__(self, name, cfg):
        self.name = name
        self.lights = self._get_status(cfg["lights"])
        self.scenes = {}
        for scene in cfg["scenes"]:
            start = int(scene["time"].split("-")[0].replace(":", ""))
            stop = int(scene["time"].split("-")[1].replace(":", ""))
            scene_name = scene["name"]
            self.scenes[(start, stop)] = Tuya.get_objects(
                type="scene", name=f"{name}: {scene_name}"
            )[0]
        print(f"{strftime('%H:%M:%S')}: Status:{self.lights}")

    @staticmethod
    def _get_status(ips):
        with mp.Pool(processes=4) as pool:
            status = {it[0]: it[1] for it in pool.map(_is_up, [ip for ip in ips])}
        return status

    def refresh(self):
        new_status = self._get_status(self.lights.keys())
        diff = {
            ip: status for ip, status in new_status.items() if status != self.lights[ip]
        }
        if True in diff.values():
            print(f"{strftime('%H:%M:%S')}: Some {self.name} lights turned on  {diff}")
            self.reset_scene()
        if False in diff.values():
            print(f"{strftime('%H:%M:%S')}: Some {self.name} lights turned off  {diff}")
        if diff:
            print(f"{strftime('%H:%M:%S')}: Status:{new_status}")
        self.lights = new_status

    def reset_scene(self):
        time = int(strftime("%H%M"))
        for schedule, scene in self.scenes.items():
            start, stop = schedule
            if start <= time < stop:
                print(f"{strftime('%H:%M:%S')}: Activating {scene.name()}")
                for _ in range(5):
                    scene.activate()
                    sleep(1)
                return


def main():
    with open("/opt/module/etc/config.yaml", "r") as file:
        config = yaml.full_load(file)
    rooms = []
    for name, cfg in config["rooms"].items():
        rooms.append(Room(name, cfg))
    while True:
        for room in rooms:
            room.refresh()
        sleep(0.5)


if __name__ == "__main__":
    main()