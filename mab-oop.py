#!/usr/bin/python3

# mab bernoulli
from scipy.stats import bernoulli


class Mab:
    def __init__(self, probability_vector, horizon):
        self.probability_vector = probability_vector
        self.horizon = horizon
        self.win_value = [0 for i in range(len(self.probability_vector))]
        self.mean_win_value = [0 for i in range(len(self.probability_vector))]
        self.number_of_games = [1 for i in range(len(self.probability_vector))]
        self.average_number_of_games = [1 for i in range(len(self.probability_vector))]
        self.current_index = 0
        self.total_number_of_games = len(self.probability_vector)

    def get_max_of_probability_vector(self):
        return max(self.probability_vector)

    def get_index_of_max_of_probably_vector(self):
        return self.probability_vector.index(max(self.probability_vector))

    def play(self):
        self.win_value[self.current_index] += bernoulli.rvs(self.probability_vector[self.current_index])
        self.number_of_games[self.current_index] += 1
        self.total_number_of_games += 1

    def print_data(self):
        print('\n---------------------------------')
        print('Vector of probability = ', self.probability_vector)
        print('Horizon = ', self.horizon)
        print('Sum win value = ', self.win_value)
        print('Number of games = ', self.number_of_games)
        print('Total number of games = ', self.total_number_of_games)
        print('---------------------------------\n')




mab = Mab([0.5, 0.2, 0.7], 100)

mab.print_data()

mab.play()
mab.play()
mab.play()
mab.play()
mab.play()

mab.print_data()



