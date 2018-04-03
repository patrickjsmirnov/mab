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
        self.win_value_in_time = []
        self.mean_win_value = [0 for i in range(self.n)]
        self.number_of_games = [1 for i in range(self.n)]
        self.average_number_of_games = [0 for i in range(self.n)]
        self.current_index = 0
        self.total_number_of_games = self.n
        self.current_index_vector = []
        self.pursuit_probability_array = []
        self.conversion_array = []

    def clear(self):
        self.win_value = [0 for i in range(self.n)]
        self.win_value_in_time = []
        self.mean_win_value = [0 for i in range(self.n)]
        self.number_of_games = [1 for i in range(self.n)]
        self.average_number_of_games = [0 for i in range(self.n)]
        self.current_index = 0
        self.total_number_of_games = self.n
        self.current_index_vector = []
        self.pursuit_probability_array = []
        self.conversion_array = []

    def get_max_of_probability_vector(self):
        return max(self.probability_vector)

    def get_index_of_max_of_probably_vector(self):
        return self.probability_vector.index(max(self.probability_vector))

    def get_index_of_max_of_mean_win_value(self):
        return self.mean_win_value.index(max(self.mean_win_value))

    def play(self):
        win_value = bernoulli.rvs(self.probability_vector[self.current_index])
        self.win_value[self.current_index] += win_value
        self.win_value_in_time.append(win_value)
        self.number_of_games[self.current_index] += 1
        self.mean_win_value[self.current_index] = self.win_value[self.current_index] / self.number_of_games[self.current_index]
        self.total_number_of_games += 1
        self.current_index_vector.append(self.current_index)

    # стратегии
    # изменяют current_index
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

    def UCB1(self, t):
        ucb1_array = [self.mean_win_value[i] + math.sqrt(2 * math.log(t) / self.number_of_games[i]) for i in range(self.n)]
        self.current_index = ucb1_array.index(max(ucb1_array))

    def softmax(self, tau):
        sum_denominator = sum([math.exp(self.mean_win_value[i] / tau) for i in range(self.n)])
        softmax_probability_array = [math.exp(self.mean_win_value[i] / tau) / sum_denominator for i in range(self.n)]
        x = random.random()
        probability_sum = softmax_probability_array[0]
        index = 0

        while index < self.n:
            if x < probability_sum:
                self.current_index = index
                break

            index += 1
            probability_sum += softmax_probability_array[index]

    def pursuit(self, beta, t):
        if t == 0:
            self.pursuit_probability_array = [1/self.n for i in range(self.n)]
            return

        index_max_mean_win_value = self.get_index_of_max_of_mean_win_value()

        for i in range(self.n):
            if i == index_max_mean_win_value:
                self.pursuit_probability_array[i] += beta * (1 - self.pursuit_probability_array[i])
                continue

            self.pursuit_probability_array[i] -= beta * self.pursuit_probability_array[i]

        x = random.random()
        probability_sum = self.pursuit_probability_array[0]
        index = 0

        while index < self.n:
            if x < probability_sum:
                self.current_index = index
                break

            index += 1
            probability_sum += self.pursuit_probability_array[index]

    def thompson_sampling(self):
        sampling_array = [random.betavariate(self.win_value[i] + 1, self.number_of_games[i] - self.win_value[i] + 1) for i in range(self.n)]
        self.current_index = sampling_array.index(max(sampling_array))

    def play_the_winner(self, t):
        if t == 1:
            self.current_index = random.randint(0, self.n - 1)
            return
        
        if self.win_value_in_time[t - 1] == 1:
            self.current_index = self.current_index_vector[t - 1]
            return

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

    def conversion(self, t):
        if t == 0:
            self.conversion_array = [0 for i in range(self.horizon)]
            return
        self.conversion_array[t] = self.conversion_array[t - 1] * t / (t + 1) + 1 / t * self.win_value_in_time[t]

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
mab = Mab([0.1, 0.3, 0.9, 0.4, 0.45, 0.39, 0.6], horizon)
starts = 30
count_starts = 0
global_regret_vector = [0 for i in range(horizon)]

while count_starts < starts:
    mab.clear()
    i = 1

    while i < horizon:
        mab.epsilon_n_greedy(i, 0.05)
        mab.play()
        i += 1

    local_regret_vector = mab.get_regret()

    for i in range(horizon):
        global_regret_vector[i] += local_regret_vector[i]

    count_starts += 1

for i in range(horizon):
    global_regret_vector[i] /= starts

# global_regret_vector = [x / starts for x in global_regret_vector]

time = mab.get_time()


plt.figure(1)
plt.plot(time, global_regret_vector, linestyle='-', label='mean = xxx')
plt.title('Regret', fontsize=18)
plt.xlabel('time', fontsize=16)
plt.ylabel('regret', fontsize=16)
plt.legend(loc='upper left', prop={'size': 11})
plt.show()

