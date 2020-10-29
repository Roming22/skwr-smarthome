#!/usr/bin/env python3
import os
import socket
from time import sleep, strftime
from api.tuya import Tuya


class Room:
    def __init__(self, name):
        self.name = name
        self.lights = self._status(["192.168.72.31", "192.168.72.32"])
        self.scenes = {
            (0, 700): "Night",
            (700, 800): "Soft",
            (800, 1700): "Daylight",
            (1700, 2130): "Soft",
            (2130, 2400): "Night",
        }
        self.scenes = {
            (int(k[0]), int(k[1])): Tuya.get_objects(type="scene", name=f"{name}: {v}")[
                0
            ]
            for k, v in self.scenes.items()
        }

    @staticmethod
    def _status(ips):
        def is_up(ip):
            status = None
            try:
                with socket.create_connection((ip, 6668), 1):
                    status = True
            except:
                status = False
            return status

        return {ip: is_up(ip) for ip in ips}

    def refresh(self):
        new_status = self._status(self.lights.keys())
        diff = {
            ip: status for ip, status in new_status.items() if status != self.lights[ip]
        }
        if True in diff.values():
            print(f"{strftime('%H:%M:%S')}: Some {self.name} lights turned on  {diff}")
            self.reset_scene()
        if False in diff.values():
            print(f"{strftime('%H:%M:%S')}: Some {self.name} lights turned off  {diff}")
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
    basement = Room("Basement")
    while True:
        basement.refresh()
        sleep(0.5)


if __name__ == "__main__":
    main()