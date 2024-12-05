import random
import pygame
from utils import SCREEN_HEIGHT, SCREEN_WIDTH, TARGET_DETECTION_RADIUS, UAV_COUNT, RED


class Target:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.found = False

    def is_detected_by(self, uav):
        """Check if the target is detected by a UAV."""
        return uav.distance_to(self) <= TARGET_DETECTION_RADIUS

    def draw(self, screen, found_count):
        if found_count:
            pygame.draw.circle(
                screen,
                (
                    255 * (UAV_COUNT - found_count) / UAV_COUNT,
                    255 * found_count / UAV_COUNT,
                    0,
                ),
                (int(self.x), int(self.y)),
                TARGET_DETECTION_RADIUS,
            )
        else:
            pygame.draw.circle(
                screen,
                RED,
                (int(self.x), int(self.y)),
                TARGET_DETECTION_RADIUS,
            )
