"""главный файл программы
 нейросеть для поиска лучшего варианта болида на сайте https://www.codingame.com/ в игре 'Mad Pod Racing'
 """
from random import randint


class Sim:
    pod_radius = 400
    checkpoint_radius = 600

    @staticmethod
    def race(weigths):
        return randint(1000, 5000)


class Pod:
    def __init__(self, track):
        self.track = track
        self.weigths = self.generate_random_weigths()
        self.time_pod = self.track_time_pod()

    def generate_random_weigths(self):
        return [1, 1, 0, 1, 1]

    def track_time_pod(self):
        return Sim.race([1, 2])

    def learn(self):
        self.time_pod = self.time_pod - 1
        return self.time_pod


class GenerateBestGroup:
    """класс создаёт нужное количество боллидов и выбирает группу из заданного количества лучших"""

    def __init__(self, size_of_best_group: int, size_of_group: int):
        self.size_of_best_group = size_of_best_group
        self.size_of_group = size_of_group
        self.checkpoints = 10
        self.track = self.create_track()
        self.best_pods = self.find_best_pods()

    def create_track(self):
        return [[randint(1000, 15000), randint(1000, 8000)] for i in range(self.checkpoints)]

    @staticmethod
    def sort_best_pods(a: list):
        a.sort(key=lambda x: x.time_pod, reverse=True)
        return a

    def find_first_pods(self):
        first_pods = [Pod(self.track) for i in range(self.size_of_best_group)]
        return self.sort_best_pods(first_pods)

    def find_best_pods(self):
        best_pods = self.find_first_pods()
        for i in range(self.size_of_best_group, self.size_of_group):
            pod = Pod(self.track)
            if pod.time_pod < best_pods[0].time_pod:
                best_pods[0] = pod
                self.sort_best_pods(best_pods)
        return best_pods


if __name__ == '__main__':
    gen = GenerateBestGroup(10, 1000)
    print([i.time_pod for i in gen.best_pods])
    print([i.learn() for i in gen.best_pods])



