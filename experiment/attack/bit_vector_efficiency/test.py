import matplotlib.pyplot as plt

from LDP.protocols.GRR import GRR
from LDP.protocols.OLH import OLH
from LDP.protocols.OUE import OUE
from LDP.protocols.RAPPOR import RAPPOR
from experiment.attack.transit.guess_trajectory import guess_plain_user_trajectory, guess_plain_user_trajectory_olh, \
    guess_fk_user_trajectory, guess_fk_user_trajectory_olh, guess_advance_user_trajectory, \
    guess_advance_user_trajectory_olh
from dataset.helper import read_dataset
from hidden_markov_model.HMM import HMM
import time
import tracemalloc

k = 20
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases

users_grid_value_list = list()
probability_of_guess_rappor_old = list()
probability_of_guess_rappor = list()
probability_of_guess_oue_old = list()
probability_of_guess_oue = list()

dataset_name = "brinkhoff"

user_trajectory_list = read_dataset('../../../dataset/' + dataset_name + '/' + dataset_name + '_grid.dat')

print(dataset_name + " Dataset is Ready")

start_time = time.time()
tracemalloc.start()

for epsilon in epsilon_list:
    print("Epsilon Value: " + str(epsilon))

    """"
    rappor_old = RAPPOR(k, epsilon)
    rappor_old.name = 'rapporOld'
    rappor_old_model = HMM(k, epsilon)
    probability_of_guess_rappor_old.append(
        guess_plain_user_trajectory(rappor_old, rappor_old_model, user_trajectory_list, 'PA', "taxi"))
    print("RAPPOR_old is Ready")
    
    oue_old = OUE(k, epsilon)
    oue_old.name = 'oueOld'
    oue_old_model = HMM(k, epsilon)
    probability_of_guess_oue_old.append(guess_plain_user_trajectory(oue_old, oue_old_model, user_trajectory_list, 'PA', "taxi"))
    print("OUE_old is Ready")
    
        rappor = RAPPOR(k, epsilon)
    rappor_model = HMM(k, epsilon)
    probability_of_guess_rappor.append(
        guess_plain_user_trajectory(rappor, rappor_model, user_trajectory_list, 'PA', "taxi"))
    print("RAPPOR is Ready")

    
    """


    oue= OUE(k, epsilon)
    oue_model = HMM(k, epsilon)
    probability_of_guess_oue.append(
        guess_plain_user_trajectory(oue, oue_model, user_trajectory_list, 'PA', "taxi"))
    print("OUE_old is Ready")

snapshot = tracemalloc.take_snapshot()
top_stats = snapshot.statistics('lineno')

total_size_bytes = sum(stat.size for stat in top_stats)
total_size_mb = total_size_bytes / (1024 * 1024)  # Convert bytes to MB
print("Total Size: " + str(total_size_mb) + " MB")

elapsed_time = time.time() - start_time
print("Elapsed Time: " + str(elapsed_time))
print("RAPPOR: " + str(probability_of_guess_rappor))
print("OUE: " + str(probability_of_guess_oue))

plt.rcParams.update({'font.size': 12})
plt.figure(figsize=(4 * 1.33, 4 * 1.33))
plt.plot(epsilon_list, probability_of_guess_rappor, linewidth=2, color='grey', marker='s', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="RAPPOR")
plt.plot(epsilon_list, probability_of_guess_oue, linewidth=2, color='yellow', marker='x', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="OUE")
plt.xticks(fontsize=15)
plt.title(dataset_name + " Dataset")
plt.ylabel("PA")
plt.xlabel('Epsilon Values')
plt.grid(linestyle=':')
plt.legend(prop={'size': 12}, ncol=2, columnspacing=0.75)
plt.show()
