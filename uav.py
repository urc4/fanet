import random
import pygame
import math

from utils import (
    BASE_POSITION,
    MOVE_STEP,
    BATTERY_DRAIN_RATE,
    BATTERY_LIFE,
    BATTERY_MINIMUM_THRESHOLD,
    YELLOW,
    UAV_RADIUS,
    RED,
    GREEN,
    COMMUNICATION_RANGE,
    BLACK,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SEPARATION_DISTANCE,
    ALIGNMENT_WEIGHT,
    SEPARATION_WEIGHT,
)


class UAV:
    def __init__(self):
        self.x = BASE_POSITION[0]
        self.y = BASE_POSITION[1]
        self.vx = random.uniform(-MOVE_STEP, MOVE_STEP)
        self.vy = random.uniform(-MOVE_STEP, MOVE_STEP)
        self.target_found = False
        self.active = False
        self.battery_life = BATTERY_LIFE
        self.battery_drain_rate = BATTERY_DRAIN_RATE
        self.min_battery_threshold = BATTERY_MINIMUM_THRESHOLD
        self.jammed = False

    def distance_to(self, other):
        """Calculate distance to another UAV or target."""
        return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def signal_quality(self, other):
        """Calculate signal quality between this UAV and another UAV."""
        distance = self.distance_to(other)
        if distance > COMMUNICATION_RANGE:
            return 0
        return max(0, 1 - (distance / COMMUNICATION_RANGE) ** 2)

    def can_communicate_with(self, other):
        """Check if this UAV can communicate with another UAV."""
        if self.jammed or other.jammed:
            return False
        return self.distance_to(other) <= COMMUNICATION_RANGE

    def move(self):
        """Update UAV position based on velocity."""
        if not self.active:
            return

        self.battery_life -= self.battery_drain_rate
        if self.battery_life < 0:
            self.battery_life = 0
            self.active = False

        current_move_step = MOVE_STEP
        if self.battery_life < self.min_battery_threshold:
            current_move_step = MOVE_STEP * (
                self.battery_life / self.min_battery_threshold
            )

        self.x += self.vx * current_move_step / MOVE_STEP
        self.y += self.vy * current_move_step / MOVE_STEP
        self.x = max(0, min(self.x, SCREEN_WIDTH))
        self.y = max(0, min(self.y, SCREEN_HEIGHT))

    def apply_behaviors(self, neighbors):
        """Calculate new velocity based on autonomous behaviors."""
        if not self.active:
            return

        if self.target_found:
            self.seek(BASE_POSITION[0], BASE_POSITION[1])
            return

        separation = [0, 0]
        alignment = [0, 0]
        wall_avoidance = [0, 0]
        neighbor_count = 0

        for other in neighbors:
            distance = self.distance_to(other)
            if distance > 0:  # ignore self
                neighbor_count += 1

                if distance < SEPARATION_DISTANCE:
                    separation[0] += self.x - other.x
                    separation[1] += self.y - other.y

                alignment[0] += other.vx
                alignment[1] += other.vy

        if self.x < SEPARATION_DISTANCE:
            wall_avoidance[0] += MOVE_STEP
        if self.x > SCREEN_WIDTH - SEPARATION_DISTANCE:
            wall_avoidance[0] -= MOVE_STEP
        if self.y < SEPARATION_DISTANCE:
            wall_avoidance[1] += MOVE_STEP
        if self.y > SCREEN_HEIGHT - SEPARATION_DISTANCE:
            wall_avoidance[1] -= MOVE_STEP

        if neighbor_count > 0:
            alignment[0] /= neighbor_count
            alignment[1] /= neighbor_count
            alignment[0] *= ALIGNMENT_WEIGHT
            alignment[1] *= ALIGNMENT_WEIGHT

        separation[0] *= SEPARATION_WEIGHT
        separation[1] *= SEPARATION_WEIGHT

        self.vx += separation[0] + alignment[0] + wall_avoidance[0]
        self.vy += separation[1] + alignment[1] + wall_avoidance[1]

        speed = math.sqrt(self.vx**2 + self.vy**2)
        if speed > MOVE_STEP:
            self.vx = (self.vx / speed) * MOVE_STEP
            self.vy = (self.vy / speed) * MOVE_STEP

    def seek(self, target_x, target_y):
        """Move towards a specific target position (base) with arrival behavior."""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        ARRIVAL_THRESHOLD = 2

        if distance < ARRIVAL_THRESHOLD:
            self.x = target_x
            self.y = target_y
            self.vx = 0
            self.vy = 0
        else:
            slowing_factor = distance / COMMUNICATION_RANGE
            speed = MOVE_STEP * min(slowing_factor, 1)

            self.vx = (dx / distance) * speed
            self.vy = (dy / distance) * speed

    def draw(self, screen):

        battery_color = (
            255 * (1 - self.battery_life / 100),
            0,
            255 * (self.battery_life / 100),
        )

        if self.jammed:
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), UAV_RADIUS)
            pygame.draw.circle(
                screen, RED, (int(self.x), int(self.y)), COMMUNICATION_RANGE, 1
            )
            return

        if not self.active:
            pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), UAV_RADIUS)
            return

        if self.target_found:
            pygame.draw.circle(
                screen, battery_color, (int(self.x), int(self.y)), UAV_RADIUS
            )
            pygame.draw.circle(
                screen, GREEN, (int(self.x), int(self.y)), COMMUNICATION_RANGE, 1
            )
        else:
            pygame.draw.circle(
                screen, battery_color, (int(self.x), int(self.y)), UAV_RADIUS
            )
            pygame.draw.circle(
                screen, BLACK, (int(self.x), int(self.y)), COMMUNICATION_RANGE, 1
            )
