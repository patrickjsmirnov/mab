#!/usr/bin/python3

# mab bernoulli
from scipy.stats import bernoulli
import random
import math
import matplotlib.pyplot as plt


class Mab:
    def __init__(self, probability_vector, horizon):
        self.probability_vector = probability_vector
        self.horizon = horizon
        self.n = len(self.probability_vector)
        self.win_value = [0 for i in range(self.n)]
        self.mean_win_value = [0 for i in range(self.n)]
        self.number_of_games = [1 for i in range(self.n)]
        self.average_number_of_games = [0 for i in range(self.n)]
        self.current_index = 0
        self.total_number_of_games = self.n
        self.current_index_vector = []

    def get_max_of_probability_vector(self):
        return max(self.probability_vector)

    def get_index_of_max_of_probably_vector(self):
        return self.probability_vector.index(max(self.probability_vector))

    def play(self):
        self.win_value[self.current_index] += bernoulli.rvs(self.probability_vector[self.current_index])
        self.number_of_games[self.current_index] += 1
        self.mean_win_value[self.current_index] = self.win_value[self.current_index] / self.number_of_games[self.current_index]
        self.total_number_of_games += 1
        self.current_index_vector.append(self.current_index)

    # стратегии
    def epsilon_greedy(self, epsilon):
        x = random.random()
        if x < 1 - epsilon:
            self.current_index = self.mean_win_value.index(max(self.mean_win_value))
        else:
            self.current_index = random.randint(0, self.n - 1)

    def delta_for_epsilon_n_greedy(self):
        index_of_max_probability_vector = self.get_index_of_max_of_probably_vector()
        delta_array = [self.probability_vector[index_of_max_probability_vector] - self.probability_vector[i] for i in range(self.n)]
        min_delta = min(i for i in delta_array if i > 0)
        return min_delta

    def epsilon_n_greedy(self, t, c):
        x = random.random()
        delta = self.delta_for_epsilon_n_greedy()
        temp = c * self.n / (delta * delta * t)
        epsilon = temp if temp < 1 else 1
        if x < 1 - epsilon:
            self.current_index = self.mean_win_value.index(max(self.mean_win_value))
        else:
            self.current_index = random.randint(0, self.n - 1)

    def get_regret(self):
        regret_vector = []
        for i in range(self.horizon):
            j = 0
            k = 0
            while j < i:
                k += self.probability_vector[self.current_index_vector[j]]
                j += 1
            regret_vector.append(i * self.probability_vector[self.get_index_of_max_of_probably_vector()] - k)
        return regret_vector

    def get_time(self):
        return [i for i in range(self.horizon)]

    def print_data(self):
        print('\n---------------------------------')
        print('Vector of probability = ', self.probability_vector)
        print('Horizon = ', self.horizon)
        print('Sum win value = ', self.win_value)
        print('Average win value = ', self.mean_win_value)
        print('Number of games = ', self.number_of_games)
        print('Total number of games = ', self.total_number_of_games)
        print('---------------------------------\n')


horizon = 10000
mab = Mab([0.5, 0.2, 0.7], horizon)

i = 0
while i < horizon:
    mab.epsilon_n_greedy(i + 1, 0.3)
    mab.play()
    i += 1

time = mab.get_time()

mab.delta_for_epsilon_n_greedy()


mab.epsilon_n_greedy(1000, 0.3)

plt.figure(1)
plt.plot(time, mab.get_regret(), linestyle='-', label='mean = xxx')
plt.title('Regret', fontsize=18)
plt.xlabel('time', fontsize=16)
plt.ylabel('regret', fontsize=16)
plt.legend(loc='upper left', prop={'size': 11})
plt.show()