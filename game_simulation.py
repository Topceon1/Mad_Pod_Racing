""" файл получает выходные данные,
расчитывает следующее положение боллида и возвращает входные данные для следующего расчета """
import math


def target_angle(pod_x, pod_y, ch_x, ch_y):
    return math.atan2(ch_y - pod_y, ch_x - pod_x)


def dist(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def pod_speed(a, b):
    return math.sqrt(a ** 2 + b ** 2)


def max_angle(a, b):
    n = a + (b - a)
    if b - a > math.pi * 0.1:
        n = a + math.pi * 0.1
        if b - a > math.pi:
            n = a - math.pi * 0.1
    if b - a < -math.pi * 0.1:
        n = a - math.pi * 0.1
        if b - a < -math.pi:
            n = a + math.pi * 0.1
    if n > math.pi:
        n -= 2 * math.pi
    if n < -math.pi:
        n += 2 * math.pi
    return n


def simulate(x, y, v_x, v_y, acc, angle):
    # принимает х, у, v_x, v_y из ответа этой же функции. Ускорение и угол из нейронки

    new_v_x = int((v_x + math.cos(angle) * acc) * 0.85)
    new_v_y = int((v_y + math.sin(angle) * acc) * 0.85)

    new_x = x + new_v_x
    new_y = y + new_v_y
    return new_x, new_y, new_v_x, new_v_y


if __name__ == '__main__':
    assert max_angle(1, 2) == 1 + math.pi * 0.1
    assert max_angle(2, 1) == 2 - math.pi * 0.1
    assert max_angle(-2, 2) == - 2 - math.pi * 0.1
    assert max_angle(2, -2) == 2 + math.pi * 0.1
    assert max_angle(1, 1.1) == 1.1
    assert max_angle(1.1, 1) == 1
    assert dist([6, 8], [3, 4]) == 5

    import pygame

    pygame.init()
    sc = pygame.display.set_mode((600, 400))
    clock = pygame.time.Clock()
    FPS = 10
    pod_x, pod_y, pod_v_x, pod_v_y, pod_acc, pod_angle = 200, 200, 0, 0, 3, 0
    check_x, check_y = 300, 300
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pod_angle = max_angle(pod_angle, target_angle(pod_x, pod_y, check_x, check_y))
        check_x, check_y = pygame.mouse.get_pos()
        pod_x, pod_y, pod_v_x, pod_v_y = simulate(pod_x, pod_y, pod_v_x, pod_v_y, pod_acc, pod_angle)
        sc.fill((0, 0, 0))
        pygame.draw.circle(sc, (255, 255, 255), (pod_x, pod_y), 10)
        pygame.draw.circle(sc, (2, 255, 255), (check_x, check_y), 10)
        pygame.display.flip()
        clock.tick(FPS)
