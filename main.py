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
        self.acc = 60
        self.angle_acc = 0
        self.angle_move = 0
        self.check_distance = 0
        self.next_checkpoint = 0
        self.track = track
        self.input = [self.angle_target,  # посчитан
                      # self.angle_next_target,
                      self.check_distance,  # посчитан
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

    def neuron_calc(self):  # OK меняет скорость и угол на новые
        nn = sm.sum_matrix(self.neural_network, self.weigths)
        self.acc = nn[-1][0]

    def learn(self):  # Заглушка.. аналог градиентного спуска
        self.v_x += randint(-2, 2)
        self.v_y += randint(-2, 2)

        #  проверка на улучшение результата
        new_track_time = self.race()
        if new_track_time < self.time_pod:
            self.time_pod = new_track_time

    def tick(self):
        #  определяем расстояние до следующей цели и скорость
        self.check_distance = int(gs.dist([self.x, self.y], self.track[self.next_checkpoint]))
        self.speed = int(gs.pod_speed(self.v_x, self.v_y))
        #  определяем угол до цели
        self.angle_target = gs.target_angle(self.x, self.y, self.track[self.next_checkpoint][0],
                                            self.track[self.next_checkpoint][1])
        #  расчитывается угол следующего положения. На входе направление указанное нейронкой(доделать)
        self.angle_move = gs.max_angle(self.angle_move,
                                       gs.target_angle(self.x, self.y, self.track[self.next_checkpoint][0],
                                                       self.track[self.next_checkpoint][1]))
        #  симуляция получает входные данные и выдает выходные
        self.x, self.y, self.v_x, self.v_y = gs.simulate(self.x, self.y, self.v_x, self.v_y, self.acc, self.angle_move)

    def collisson(self) -> bool:  # OK
        if (self.x - self.track[self.next_checkpoint][0]) * (self.x - self.track[self.next_checkpoint][0]) + (
                self.y - self.track[self.next_checkpoint][1]) * (self.y - self.track[self.next_checkpoint][1]) < 360000:
            return True

    def race(self):  # OK
        ticks = 0
        turns = 0
        self.next_checkpoint = 0
        while self.next_checkpoint != len(self.track):
            self.neuron_calc()
            turns += 1
            if turns > 100:
                return 9999999999
            ticks += 1
            self.tick()
            if self.collisson():
                turns = 0
                self.next_checkpoint += 1
            x = self.x
            y = self.y
            vn = [x, y]
            self.pod_track.append(vn)  # формируем список для визуализации
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
    SCALE = 30
    POD_RADIUS = 400
    CHECK_RADIUS = 600
    FPS = 30
    GAME_FRAME_SIZE = [16000, 9000]
    #  созаем "FROM_PODS" болидов и выбираем "BEST_PODS" лучших из них
    BEST_PODS = 50
    FROM_PODS = 100
    gen = GenerateBestGroup(BEST_PODS, FROM_PODS, layers=4, neurons=4)
    print([i.time_pod for i in gen.best_pods])
    # """
    import pygame

    pygame.init()
    sc = pygame.display.set_mode((list(map(lambda k: k / SCALE, GAME_FRAME_SIZE))))
    clock = pygame.time.Clock()
    gen.best_pods[0].next_checkpoint = 0
    pod_max_step = min(gen.best_pods, key=lambda i: i.time_pod)  # находим самый долгий болид чтобы увидеть весь путь
    step_max = pod_max_step.time_pod - 1
    step = 0


    def pod_ticks_xy(f_step: int, b: list):
        if f_step > len(b) - 1:
            return b[-1]
        return b[f_step]


    while True:
        step += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        sc.fill((0, 0, 0))

        for i in gen.track:
            pygame.draw.circle(sc, (111, 111, 111), (list(map(lambda k: k / SCALE, i))), CHECK_RADIUS / SCALE)

        for i in gen.best_pods:
            pygame.draw.circle(sc, (255, 255, 255), (list(map(lambda k: k / SCALE, pod_ticks_xy(step, i.pod_track)))),
                               POD_RADIUS / SCALE)
        pygame.display.flip()
        clock.tick(FPS)
        # """
