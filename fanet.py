import random
import time
import pygame
from uav import UAV
from attacker import Attacker
from utils import (
    MOVE_STEP,
    ATTACK_DURATION,
    ATTACK_INTERVAL,
    SIGNAL_QUALITY_THRESHOLD,
    UAV_RADIUS,
)


class FANET:
    def __init__(self, num_uavs):
        self.uavs = [UAV() for _ in range(num_uavs)]
        self.current_uav_index = 0
        self.found_count = 0
        self.attacker = Attacker()
        self.last_attack_time = time.time()

    def activate_next_uav(self):
        """Activate the next UAV to start its mission."""
        if self.current_uav_index < len(self.uavs):
            self.uavs[self.current_uav_index].active = True
            self.uavs[self.current_uav_index].vx = random.uniform(-MOVE_STEP, MOVE_STEP)
            self.uavs[self.current_uav_index].vy = random.uniform(-MOVE_STEP, MOVE_STEP)
            self.current_uav_index += 1

    def propagate_detection(self, uav, visited):
        """Recursively propagate target detection to all connected UAVs."""
        if uav in visited:
            return
        visited.add(uav)

        if not uav.target_found:
            self.found_count += 1
            uav.target_found = True

        for neighbor in self.uavs:
            probability = neighbor.signal_quality(uav)
            probability_message_is_sent = random.random() < probability
            if (
                neighbor != uav
                and neighbor.can_communicate_with(uav)
                and not neighbor.target_found
                and neighbor.signal_quality(uav) > 0.9
            ):
                self.propagate_detection(neighbor, visited)

    def get_communication_links(self):
        """Find all UAV pairs that can communicate and their signal quality."""
        links = []
        for i, uav1 in enumerate(self.uavs):
            for j, uav2 in enumerate(self.uavs):
                if i < j:
                    quality = uav1.signal_quality(uav2)
                    if quality > SIGNAL_QUALITY_THRESHOLD:
                        links.append((uav1, uav2, quality))
        return links

    def update(self, target):
        """Update UAV positions and behaviors."""
        if time.time() - self.last_attack_time > ATTACK_INTERVAL:
            self.attacker.initiate_attack(self.uavs)
            self.last_attack_time = time.time()
        if time.time() - self.last_attack_time > ATTACK_DURATION:
            for uav in self.uavs:
                uav.jammed = False

        jammed_uav = self.attacker.apply_jamming(self.uavs)
        if jammed_uav:
            jammed_uav.jammed = True

        for uav in self.uavs:
            neighbors = [
                other for other in self.uavs if uav.can_communicate_with(other)
            ]
            uav.apply_behaviors(neighbors)  # ta usando mesmo range q o de comunicacao
            uav.move()

            if uav.target_found:
                self.propagate_detection(uav, set())

            if target.is_detected_by(uav):
                if not uav.target_found:
                    self.found_count += 1
                    uav.target_found = True
                self.propagate_detection(uav, set())

    def draw(self, screen, links):
        for uav1, uav2, quality in links:
            if not uav1.active or not uav2.active:
                continue
            if uav1.jammed or uav2.jammed:
                continue
            color = (
                int(255 * ((1 + SIGNAL_QUALITY_THRESHOLD) - quality)),
                int(255 * quality),
                0,
            )
            pygame.draw.line(screen, color, (uav1.x, uav1.y), (uav2.x, uav2.y), 2)

        for uav in self.uavs:
            uav.draw(screen)
