import matplotlib.pyplot as plt

from LDP.protocols.GRR import GRR
from LDP.protocols.OLH import OLH
from LDP.protocols.OUE import OUE
from LDP.protocols.RAPPOR import RAPPOR
from experiment.attack.transit.guess_trajectory import guess_fk_user_trajectory, guess_fk_user_trajectory_olh
from dataset.helper import read_dataset

from test.script.hidden_markov_model.HMM import HMM

k = 20
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]
iter_list = [1, 2, 3, 4, 5]
users_grid_value_list = list()
probability_of_guess_grr = list()
probability_of_guess_rappor = list()
probability_of_guess_oue = list()
probability_of_guess_olh = list()

user_trajectory_list = read_dataset('../../dataset/taxi/taxi_stationary_grid.dat')

for epsilon in epsilon_list:
    print("Epsilon Value: " + str(epsilon))

    grr = GRR(k, epsilon)
    grr_model = HMM(k, epsilon)
    probability_of_guess_grr.append(guess_fk_user_trajectory(grr, grr_model, user_trajectory_list))
    print("GRR is Ready")

    rappor = RAPPOR(k, epsilon)
    rappor_model = HMM(k, epsilon)
    probability_of_guess_rappor.append(guess_fk_user_trajectory(rappor, rappor_model, user_trajectory_list))
    print("RAPPOR is Ready")

    oue = OUE(k, epsilon)
    oue_model = HMM(k, epsilon)
    probability_of_guess_oue.append(guess_fk_user_trajectory(oue, oue_model, user_trajectory_list))
    print("OUE is Ready")

    olh = OLH(k, epsilon)
    olh_model = HMM(k, epsilon)
    probability_of_guess_olh.append(guess_fk_user_trajectory_olh(olh, olh_model, user_trajectory_list))


print("GRR: " + str(probability_of_guess_grr))
print("RAPPOR: " + str(probability_of_guess_rappor))
print("OUE: " + str(probability_of_guess_oue))
print("OLH: " + str(probability_of_guess_olh))

plt.rcParams.update({'font.size': 12})
plt.figure(figsize=(4 * 1.33, 4 * 1.33))
plt.plot(epsilon_list, probability_of_guess_grr, linewidth=2, color='purple', marker='o', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="GRR")
plt.plot(epsilon_list, probability_of_guess_rappor, linewidth=2, color='grey', marker='s', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="RAPPOR")
plt.plot(epsilon_list, probability_of_guess_oue, linewidth=2, color='blue', marker='x', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="OUE")
plt.plot(epsilon_list, probability_of_guess_olh, linewidth=2, color='yellow', marker='x', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="OLH")
plt.xticks(fontsize=15)
plt.ylim(0, 1)
plt.ylabel("Ratio Of Guess")
plt.xlabel('Epsilon Values')
plt.grid(linestyle=':')
plt.legend(prop={'size': 12}, ncol=2, columnspacing=0.75)
plt.savefig('expected-sr-vs-U.png', format='png', dpi=300, bbox_inches='tight')
plt.show()