"""главный файл программы
 нейросеть для поиска лучшего варианта болида на сайте https://www.codingame.com/ в игре 'Mad Pod Racing'
 """
import pygame
import math
from random import randint

SCALE = 100
POD_RADIUS = 400
CHECK_RADIUS = 600
FPS = 10
GAME_FRAME_SIZE = [16000, 9000]


class Pod:
    def __init__(self, track):
        self.pod_track = []
        self.x = 80000
        self.y = 45000
        self.v_x = 0
        self.v_y = 0
        self.angle_target = 0
        self.angle_next_target = 0
        self.speed = 0
        self.acc = 60
        self.angle_acc = 0
        self.angle_move = 0
        self.check_distance = 0
        self.next_checkpoint = 0

    def collisson(self) -> bool:
        pass


if __name__ == '__main__':
    pygame.init()
    sc = pygame.display.set_mode((list(map(lambda k: k / SCALE, GAME_FRAME_SIZE))))
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        sc.fill((0, 0, 0))

        pygame.display.flip()
        clock.tick(FPS)
