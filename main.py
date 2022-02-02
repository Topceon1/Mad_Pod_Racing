"""главный файл программы
 нейросеть для поиска лучшего варианта болида на сайте https://www.codingame.com/ в игре 'Mad Pod Racing'
 """
from random import randint


class Pod:
    def __init__(self):
        self.time_pod = self.track_time_pod()

    def track_time_pod(self):
        return randint(1000, 5000)


class GenerateBestGroup:
    """класс создаёт нужное количество боллидов и выбирает группу из заданного количества лучших"""

    def __init__(self, best_group: int, size_of_group: int):
        self.best_group = best_group
        self.size_of_group = size_of_group
        self.best_pods = self.find_first_pods()

    @staticmethod
    def sort_best_pods(a: list):
        a.sort(key=lambda x: x.time_pod)
        return a

    def find_first_pods(self):
        first_pods = [Pod() for i in range(self.best_group)]
        return self.sort_best_pods(first_pods)

    def find_best_pods(self):
        for i in range(self.best_group, self.size_of_group):
            pod = Pod()
            if pod.time_pod > self.best_pods[0].time_pod:
                self.best_pods[0] = pod
                self.sort_best_pods(self.best_pods)


if __name__ == '__main__':
    gen = GenerateBestGroup(10, 1000)
    gen.find_best_pods()
