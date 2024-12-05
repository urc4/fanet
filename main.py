import pygame
import time
from target import Target
from base import Base
from fanet import FANET
from utils import (
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    UAV_COUNT,
    BASE_POSITION,
    BASE_SIZE,
    ACTIVATION_DELAY,
    WHITE,
    FPS,
)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("FANET Simulation")
    clock = pygame.time.Clock()

    fanet = FANET(UAV_COUNT)
    base = Base(BASE_POSITION[0], BASE_POSITION[1], BASE_SIZE)
    target = Target()

    running = True
    last_activation_time = time.time()
    activation_delay = ACTIVATION_DELAY

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = time.time()
        if current_time - last_activation_time > activation_delay:
            fanet.activate_next_uav()
            last_activation_time = current_time

        fanet.update(target)

        screen.fill(WHITE)
        links = fanet.get_communication_links()

        fanet.draw(screen, links)
        target.draw(screen, fanet.found_count)
        base.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
