"""главный файл программы
 нейросеть для поиска лучшего варианта болида на сайте https://www.codingame.com/ в игре 'Mad Pod Racing'
 """
from random import randint
import copy

import geerate_weigths as gw
import sum_matrix as sm
import game_simulation as gs


class Pod:
    def __init__(self, track, neural_network):
        self.pod_track = []
        self.x = 8000
        self.y = 4500
        self.v_x = 0
        self.v_y = 0
        self.angle_target = 0
        self.angle_next_target = 0
        self.speed = 0
        self.acc = 30
        self.angle_acc = 0
        self.angle_move = 0
        self.next_checkpoint = 0
        self.track = track
        self.input = [self.angle_target,
                      self.angle_next_target,
                      self.speed,
                      self.angle_move,
                      100  # нейрон смещения
                      ]
        self.output = [self.acc,
                       self.angle_acc]
        self.neural_network = copy.deepcopy(neural_network)
        self.neural_network_assebly()
        self.weigths = self.generate_random_weigths()
        self.neuron_calc()
        self.time_pod = self.race()

    def generate_random_weigths(self):  # OK
        return gw.generate_weigths(self.neural_network, randint, 100000)

    def neural_network_assebly(self):  # OK
        self.neural_network.append(self.output)
        self.neural_network.insert(0, self.input)

    def neuron_calc(self):  # OK
        self.neural_network = sm.sum_matrix(self.neural_network, self.weigths)

    def learn(self):  # Заглушка.. аналог градиентного спуска
        self.v_x += randint(-2, 2)
        self.v_y += randint(-2, 2)

        #  проверка на улучшение результата
        new_track_time = self.race()
        if new_track_time < self.time_pod:
            self.time_pod = new_track_time

    def tick2(self):  # Заглушка.. переделать на симуляцпю настоящей игры
        if self.x > self.track[self.next_checkpoint][0]:
            self.x -= self.v_x
        else:
            self.x += self.v_x
        if self.y > self.track[self.next_checkpoint][1]:
            self.y -= self.v_y
        else:
            self.y += self.v_y

    def tick(self):
        self.angle_move = gs.max_angle(self.angle_move,
                                       gs.target_angle(self.x, self.y, self.track[self.next_checkpoint][0],
                                                       self.track[self.next_checkpoint][1]))
        self.x, self.y, self.v_x, self.v_y = gs.simulate(self.x, self.y, self.v_x, self.v_y, self.acc, self.angle_move)

    def collisson(self) -> bool:  # OK
        if (self.x - self.track[self.next_checkpoint][0]) * (self.x - self.track[self.next_checkpoint][0]) + (
                self.y - self.track[self.next_checkpoint][1]) * (self.y - self.track[self.next_checkpoint][1]) < 16000:
            return True

    def race(self):  # OK
        ticks = 0
        turns = 0
        self.next_checkpoint = 0
        while self.next_checkpoint != len(self.track):
            self.neuron_calc()
            turns += 1
            if turns > 300:
                return 9999999999
            ticks += 1
            self.tick()
            if self.collisson():
                turns = 0
                self.next_checkpoint += 1
            x = self.x
            y = self.y
            vn = [x, y]
            self.pod_track.append(vn)
        return ticks


class GenerateBestGroup:
    """класс создаёт нужное количество боллидов и выбирает группу из заданного количества лучших"""

    def __init__(self, size_of_best_group: int, size_of_group: int, layers: int, neurons: int):
        self.size_of_best_group = size_of_best_group
        self.size_of_group = size_of_group
        self.checkpoints = 10
        self.track = self.create_track()
        self.layers = layers
        self.neurons = neurons
        self.neural_network = self.create_neural_networks()
        self.best_pods = self.find_best_pods()

    def create_neural_networks(self):  # OK
        nn = []
        for i in range(self.layers):
            nn.append([100 for j in range(self.neurons)])
        return nn

    def create_track(self):  # OK
        return [[randint(1000, 15000), randint(1000, 8000)] for i in range(self.checkpoints)]

    @staticmethod
    def sort_best_pods(a: list):  # OK
        a.sort(key=lambda x: x.time_pod, reverse=True)
        return a

    def find_first_pods(self):  # OK
        first_pods = [Pod(self.track, self.neural_network) for i in range(self.size_of_best_group)]
        return self.sort_best_pods(first_pods)

    def find_best_pods(self):  # OK
        best_pods = self.find_first_pods()
        for i in range(self.size_of_best_group, self.size_of_group):
            pod = Pod(self.track, self.neural_network)
            if pod.time_pod < best_pods[0].time_pod:
                best_pods[0] = pod
                self.sort_best_pods(best_pods)
        return best_pods


if __name__ == '__main__':
    gen = GenerateBestGroup(2, 10, layers=8, neurons=8)
    # print([i.time_pod for i in gen.best_pods])
    # print(gen.best_pods[0].pod_track)
    # for i in gen.best_pods:
    #     for j in range(10):
    #         i.learn()
    # print([i.time_pod for i in gen.best_pods])
    # """
    import pygame

    SCALE = 10
    POD_RADIUS = 400
    CHECK_RADIUS = 600
    FPS = 30
    GAME_FRAME_SIZE = [16000, 9000]

    pygame.init()
    sc = pygame.display.set_mode((list(map(lambda k: k / SCALE, GAME_FRAME_SIZE))))
    clock = pygame.time.Clock()
    gen.best_pods[0].next_checkpoint = 0
    pod_max_step = max(gen.best_pods, key=lambda i: i.time_pod)  # находим самый долгий болид чтобы увидеть весь путь
    step_max = pod_max_step.time_pod - 1
    step = 0
    while step < step_max:
        step += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        sc.fill((0, 0, 0))

        for i in gen.track:
            pygame.draw.circle(sc, (2, 255, 255), (list(map(lambda k: k / SCALE, i))), CHECK_RADIUS / SCALE)

        for i in gen.best_pods:
            pygame.draw.circle(sc, (255, 255, 255), (list(map(lambda k: k / SCALE, i.pod_track[step]))), POD_RADIUS / SCALE)
        pygame.display.flip()
        clock.tick(FPS)
        # """
