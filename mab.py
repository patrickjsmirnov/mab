# import random
import math
# import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import bernoulli

p1 = [0.3, 0.45, 0.5, 0.47, 0.1]
p2 = [0.1, 0.1, 0.6, 0.1, 0.1]
n = len(p1)


# определение лучшей руки
def search_best_arm():
    index_maximum, maximum = 0, p1[0]
    for i in range(n):
        if p1[i] > maximum:
            maximum = p1[i]
            index_maximum = i
    return index_maximum


#  параметры запуска
launch_number = 60
time_finish = 5000
index_best_arm = search_best_arm()


def func_win():
    mean_win[current_number] += bernoulli.rvs(p1[current_number])
    num_of_games[current_number] += 1
    return 0


def func_first_win():
    for i in range(n):
        mean_win[i] = bernoulli.rvs(p1[i])
	return 0


def number_of_arms(t):
	global current_number
	max_temp = mean_win[0] / num_of_games[0] + math.sqrt(2 * math.log(t) / num_of_games[0])
	max_temp_index = 0
	for i in range(n):
		temp[i] = mean_win[i] / num_of_games[i] + math.sqrt(2 * math.log(t) / num_of_games[i])
		if temp[i] > max_temp:
			max_temp = temp[i]
			max_temp_index = i
	current_number = max_temp_index
	number_of_games[current_number] += 1
	return 0


def func_regret_calculation():
	for i in range(time_finish):
		j, temp_var = 0, 0
		while j < i:
			temp_var += p1[current_number_vector[j]]
			j += 1
		regret_vec[i] = i * p1[index_best_arm] - temp_var
	return 0


# вычисляем доля оптимальных
def func_per_of_optimal():
	temp_vec = [0 for k in range(time_finish)]
	i = 1
	while i < time_finish:
		if current_number_vector[i] == index_best_arm:
			temp_vec[i] = 1
		j = 0
		s = 0
		while j <= i:
			s += temp_vec[j]
			j += 1
		per_of_optimal[i] = s / i
		i += 1

	return 0

#  без эксперта
sum_of_reward = [0 for i in range(n)]
sum_per_of_optimal = [0 for i in range(time_finish)]
per_of_optimal = [0 for i in range(time_finish)]
mean_regret_vec = [0 for i in range(time_finish)]
number_of_games = [0 for i in range(n)]
upper_bound_vector = [0 for i in range(time_finish)]
launch_count = 0
regret_vec = [0 for i in range(time_finish)]
mean_win = [0 for i in range(n)]
num_of_games = [1 for i in range(n)]
current_number_vector = [0 for i in range(time_finish)]
temp = [0 for i in range(n)]

while launch_count < launch_number:
	count = 1
	current_number = 0
	for i in range(n):
		mean_win[i] = 0
		num_of_games[i] = 1
		temp[i] = 0
	for i in range(time_finish):
		regret_vec[i] = 0
		current_number_vector[i] = 0
		per_of_optimal[i] = 0

	func_first_win()

	while count < time_finish:
		number_of_arms(count)
		current_number_vector[count] = current_number
		func_win()
		count += 1

	func_per_of_optimal()
	func_regret_calculation()

	for i in range(time_finish):
		mean_regret_vec[i] += regret_vec[i]
		sum_per_of_optimal[i] += per_of_optimal[i]

	for i in range(n):
		sum_of_reward[i] += mean_win[i]

	launch_count += 1

# суммарный выигрыш
sum_reward = 0
for i in range(n):
	sum_reward += sum_of_reward[i] / launch_number
	number_of_games[i] /= launch_number
	sum_per_of_optimal[i] /= launch_number


print('sum_reward = ', sum_reward)
print('curr_vec = ', number_of_games)

for i in range(time_finish):
	# sum_per_of_optimal[i] /= launch_number
	mean_regret_vec[i] /= launch_number
	# print('mean = ', mean_regret_vec_f[i])

# считаем долю оптимальных
# sum_optimal = 0
# for i in range(time_finish):
# 	sum_optimal += sum_per_of_optimal[i]
# 	# print('sum_optimal = ', sum_optimal)




def upper_bound():
	delta = [0 for i in range(n)]
	temp2 = 0
	for i in range(n):
		if p1[i] < p1[index_best_arm]:
			delta[i] = p1[index_best_arm] - p1[i]
		temp2 += delta[i]

	i = 1
	while i < time_finish:
		temp1 = 0
		for k in range(n):
			if delta[k] != 0:
				temp1 += 8 * math.log(i) / delta[k]
		upper_bound_vector[i] = temp1 + (1 + math.pi * math.pi / 3) * temp2
		i += 1

	return 0


time = [i for i in range(time_finish)]
upper_bound()

#  для вывода
p1_string = [str(x) for x in p1]
p1_string = ', '.join(p1_string)

p2_string = [str(x) for x in p2]
p2_string = ', '.join(p2_string)

p3_string = [str(x) for x in p3]
p3_string = ', '.join(p3_string)

p4_string = [str(x) for x in p4]
p4_string = ', '.join(p4_string)

p5_string = [str(x) for x in p5]
p5_string = ', '.join(p5_string)

p6_string = [str(x) for x in p6]
p6_string = ', '.join(p6_string)




plt.figure(1)
plt.plot(time, mean_regret_vec_classic, linestyle='--', label='mean = [' + p1_string + ']')
plt.plot(time, mean_regret_vec, 'green', label='predictions = [' + p2_string + ']')
plt.plot(time, mean_regret_vec_f1, 'red', label='predictions = [' + p3_string + ']')
plt.plot(time, mean_regret_vec_f2, 'black', label='predictions = [' + p4_string + ']')
plt.plot(time, mean_regret_vec_f3, 'magenta', label='predictions = [' + p5_string + ']')
plt.plot(time, mean_regret_vec_f4, 'cyan', label='predictions = [' + p6_string + ']')
# plt.plot(time, upper_bound_vector, 'r', label='upper bound')
# plt.plot(time, mean_regret_1, 'b', label='[0, 3.3, 0, 0, 0]')
plt.title('The total expected regret (UCB1 Bernoulli)', fontsize=18)
plt.xlabel('time', fontsize=16)
plt.ylabel('regret', fontsize=16)
plt.legend(loc='upper left', prop={'size': 11})
plt.show()

plt.figure(2)
plt.plot(time, sum_per_of_optimal, linestyle='--', label='mean = [' + p1_string + ']')
plt.plot(time, sum_per_of_optimal_f, 'green', label='predictions = [' + p2_string + ']')
plt.title('Per of optimal', fontsize=18)
plt.xlabel('time', fontsize=16)
plt.ylabel('per of optimal', fontsize=16)
plt.legend(loc='lower right')
plt.show()