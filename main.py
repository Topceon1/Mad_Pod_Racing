"""главный файл программы
 нейросеть для поиска лучшего варианта болида на сайте https://www.codingame.com/ в игре 'Mad Pod Racing'
 """
from random import randint


class Pod:
    def __init__(self, track):
        self.x = 8000
        self.y = 4500
        self.x_speed = randint(1, 50)
        self.y_speed = randint(1, 50)
        self.speed = 0
        self.acc = 0
        self.angle_acc = 0
        self.angle_move = 0
        self.next_checkpoint = 0
        self.track = track
        self.weigths = self.generate_random_weigths()
        self.time_pod = self.race()

    def generate_random_weigths(self):  # Заглушка.. генерирует случайные веса для всех нейронов
        return [1, 1, 0, 1, 1]

    def learn(self):  # Заглушка.. аналог градиентного спуска
        self.x_speed += randint(-2, 2)
        self.y_speed += randint(-2, 2)

        #  проверка на улучшение результата
        new_track_time = self.race()
        if new_track_time < self.time_pod:
            self.time_pod = new_track_time

    def tick(self):  # Заглушка.. переделать на симуляцпю настоящей игры
        if self.x > self.track[self.next_checkpoint][0]:
            self.x -= self.x_speed
        else:
            self.x += self.x_speed
        if self.y > self.track[self.next_checkpoint][1]:
            self.y -= self.y_speed
        else:
            self.y += self.y_speed

    def collisson(self) -> bool:  # OK
        if (self.x - self.track[self.next_checkpoint][0]) * (self.x - self.track[self.next_checkpoint][0]) + (
                self.y - self.track[self.next_checkpoint][1]) * (self.y - self.track[self.next_checkpoint][1]) < 16000:
            return True

    def race(self):  # OK
        ticks = 0
        self.next_checkpoint = 0
        while self.next_checkpoint != len(self.track):
            ticks += 1
            self.tick()
            if self.collisson():
                # print(f'чекпоинт {self.next_checkpoint} пройден')
                self.next_checkpoint += 1
        return ticks


class GenerateBestGroup:
    """класс создаёт нужное количество боллидов и выбирает группу из заданного количества лучших"""

    def __init__(self, size_of_best_group: int, size_of_group: int, layers, neurons):
        self.size_of_best_group = size_of_best_group
        self.size_of_group = size_of_group
        self.checkpoints = 10
        self.track = self.create_track()
        self.best_pods = self.find_best_pods()
        self.layers = layers
        self.neurons = neurons
        self.neural_network = self.create_neural_networks()

    def create_neural_networks(self):  # OK
        nn = []
        for i in range(self.layers):
            nn.append([0 for j in range(self.neurons)])
        return nn

    def create_track(self):  # OK
        return [[randint(1000, 15000), randint(1000, 8000)] for i in range(self.checkpoints)]

    @staticmethod
    def sort_best_pods(a: list):  # OK
        a.sort(key=lambda x: x.time_pod, reverse=True)
        return a

    def find_first_pods(self):  # OK
        first_pods = [Pod(self.track) for i in range(self.size_of_best_group)]
        return self.sort_best_pods(first_pods)

    def find_best_pods(self):  # OK
        best_pods = self.find_first_pods()
        for i in range(self.size_of_best_group, self.size_of_group):
            pod = Pod(self.track)
            if pod.time_pod < best_pods[0].time_pod:
                best_pods[0] = pod
                self.sort_best_pods(best_pods)
        return best_pods


if __name__ == '__main__':
    gen = GenerateBestGroup(10, 100, layers=3, neurons=5)
    print([i.time_pod for i in gen.best_pods])
    for i in gen.best_pods:
        for j in range(10):
            i.learn()
    print([i.time_pod for i in gen.best_pods])
    print(gen.neural_network)
