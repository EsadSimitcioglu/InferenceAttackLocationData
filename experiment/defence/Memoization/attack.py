from matplotlib import pyplot as plt

from LDP.protocols.GRR import GRR
from LDP.protocols.RAPPOR import RAPPOR
from dataset.helper import read_dataset
from experiment.attack.transit.guess_trajectory import guess_plain_user_trajectory, ratio_of_guess
from hidden_markov_model.HMM import HMM


def experiment(protocol, hmm_model, user_trajectory_list):
    perturbed_reports = protocol.memoized(user_trajectory_list)
    hmm_model.create_plain_protocol_model(protocol)
    guess_list = [hmm_model.guess_user_values(report) for report in perturbed_reports]
    ratio = sum([ratio_of_guess(user_trajectory, guess) for user_trajectory, guess in
                 zip(user_trajectory_list, guess_list)]) / len(user_trajectory_list)
    return ratio

# Parameters for simulation
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases
users_grid_value_list = list()
probability_of_guess_grr = list()
probability_of_guess_grr_memoized = list()
probability_of_guess_rappor = list()
probability_of_guess_rappor_memoized = list()

user_trajectory_list = read_dataset('../../../dataset/taxi/taxi_grid_2.dat')

for epsilon in epsilon_list:
    print("Epsilon Value: " + str(epsilon))

    grr_model = HMM(k, epsilon)
    rappor_model = HMM(k, epsilon)


    grr = GRR(k, epsilon)
    probability_of_guess_grr.append(guess_plain_user_trajectory(grr, grr_model, user_trajectory_list))

    grr_m = GRR(k, epsilon)
    probability_of_guess_grr_memoized.append(experiment(grr_m, grr_model, user_trajectory_list))

    rappor = RAPPOR(k, epsilon)
    probability_of_guess_rappor.append(guess_plain_user_trajectory(rappor, rappor_model, user_trajectory_list))
    print("RAPPOR is Ready")

    rappor_m = RAPPOR(k, epsilon)
    probability_of_guess_rappor_memoized.append(experiment(rappor_m, rappor_model, user_trajectory_list))
    print("RAPPOR_M is Ready")

print("GRR: " + str(probability_of_guess_grr))
print("GRR_M: " + str(probability_of_guess_grr_memoized))
print("RAPPOR: " + str(probability_of_guess_rappor))
print("RAPPOR_M: " + str(probability_of_guess_rappor_memoized))
plt.rcParams.update({'font.size': 12})
plt.figure(figsize=(4 * 1.33, 4 * 1.33))
plt.plot(epsilon_list, probability_of_guess_grr, linewidth=2, color='red', marker='o', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="GRR")
plt.plot(epsilon_list, probability_of_guess_grr_memoized, linewidth=2, color='purple', marker='o', markersize=10,
         mew=1.5,
         fillstyle='none', clip_on=False, label="GRR-Memoized")
plt.plot(epsilon_list, probability_of_guess_rappor, linewidth=2, color='blue', marker='o', markersize=10, mew=1.5,
            fillstyle='none', clip_on=False, label="RAPPOR")
plt.plot(epsilon_list, probability_of_guess_rappor_memoized, linewidth=2, color='green', marker='o', markersize=10,
            mew=1.5, fillstyle='none', clip_on=False, label="RAPPOR-Memoized")

plt.xticks(fontsize=15)
plt.ylim(0, 1)
plt.ylabel("Ratio Of Guess")
plt.xlabel('Epsilon Values')
plt.grid(linestyle=':')
plt.legend(prop={'size': 12}, ncol=2, columnspacing=0.75)
plt.show()
