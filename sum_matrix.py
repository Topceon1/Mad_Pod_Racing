def sigmoid(a):
    if (a / 1 + abs(a)) > 30:
        return 1
    return 0


def sum_matrix(neural_network: list, weigths: list) -> list:
    d = neural_network
    for i in range(1, len(d)):
        for j in range(len(d[i]) - 1):
            d[i][j] = sigmoid(sum([d[i][j] * k for k in weigths[i - 1][j]]))
    return d


if __name__ == '__main__':
    print(sum_matrix(
        [[0, 0, 0, 0, 100],
         [100, 100, 100, 100, 100],
         [100, 100, 100, 100, 100],
         [100, 100, 100, 100, 100],
         [100, 100, 100, 100, 100],
         [100, 100, 100, 100, 100],
         [0, 0, 'dont del']],
        [[[0.49394, 0.46222, 0.6808, 0.15759, 0.48074], [0.1732, 0.19304, 0.26187, 0.11346, 0.91319],
          [0.63146, 0.20547, 0.53129, 0.43683, 0.12818], [0.68555, 0.44097, 0.34098, 0.7575, 0.65793]],
         [[0.50457, 0.83389, 0.04612, 0.59598, 0.57527], [0.25242, 0.2186, 0.05127, 0.54942, 0.09896],
          [0.29268, 0.60883, 0.17512, 0.35934, 0.95167], [0.92125, 0.14136, 0.10276, 0.76423, 0.92322]],
         [[0.27664, 0.82202, 0.32329, 0.26075, 0.4145], [0.55232, 0.93539, 0.27618, 0.02091, 0.55073],
          [0.94446, 0.47295, 0.35465, 0.59736, 0.15198], [0.04112, 0.56928, 0.08546, 0.48796, 0.66781]],
         [[0.29116, 0.50858, 0.81443, 0.69165, 0.8216], [0.18506, 0.96361, 0.57955, 0.33208, 0.81835],
          [0.38113, 0.31696, 0.50515, 0.93354, 0.45518], [0.82438, 0.54626, 0.67094, 0.65991, 0.07508]],
         [[0.96091, 0.37381, 0.85104, 0.70854, 0.64123], [0.76556, 0.03497, 0.72376, 0.24644, 0.50165],
          [0.07408, 0.54822, 0.90231, 0.55513, 0.84794], [0.73708, 0.21562, 0.31195, 0.14201, 0.27404]],
         [[0.33473, 0.87869, 0.57765, 0.93789, 0.79685], [0.27108, 0.22101, 0.87837, 0.00994, 0.79191]]]

    ))
    assert sum_matrix([[1, 2, 3],
                       [1, 2, 3],
                       [1, 2, 3]]
                      ,
                      [[[1, 2, 3], [1, 2, 3], [1, 2, 3]],
                       [[1, 2, 3], [1, 2, 3], [1, 2, 3]]]) == [[1, 2, 3],
                                                               [0, 0, 3],
                                                               [0, 0, 3]]
    assert sum_matrix([[1, 2, 3, 4],
                       [1, 2, 3, 4],
                       [1, 2, 3, 4],
                       [1, 2, 3, 4]]
                      ,
                      [[[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]],
                       [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]],
                       [[1, 2, 3, 4], [1, 2, 3, 4], [1, 2, 3, 4]]]) == [[1, 2, 3, 4],
                                                                        [0, 1, 1, 4],
                                                                        [0, 1, 1, 4],
                                                                        [0, 1, 1, 4]]
