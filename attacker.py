import random
import time
from utils import ATTACK_DURATION


class Attacker:
    def __init__(self):
        self.jammed_uav = None
        self.attack_end_time = 0

    def initiate_attack(self, uavs):
        """Selects a random UAV to jam."""
        self.jammed_uav = None
        while not self.jammed_uav:
            self.jammed_uav = random.choice(uavs)
            if not self.jammed_uav.active:
                self.jammed_uav = None
        self.attack_end_time = time.time() + ATTACK_DURATION

    def is_jamming_active(self):
        return time.time() < self.attack_end_time

    def apply_jamming(self, uavs):
        """Disable communication for the jammed UAV."""
        if self.is_jamming_active():
            return self.jammed_uav
        return None
