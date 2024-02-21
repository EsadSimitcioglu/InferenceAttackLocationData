from matplotlib import pyplot as plt

from LDP.protocols.GRR import GRR
from LDP.protocols.OLH import OLH
from LDP.protocols.OUE import OUE
from LDP.protocols.RAPPOR import RAPPOR
from dataset.helper import read_dataset
from experiment.attack.metrics import experiment_metrics
from experiment.attack.transit.guess_trajectory import guess_plain_user_trajectory, ratio_of_guess
from hidden_markov_model.HMM import HMM


def experiment(protocol, hmm_model, user_trajectory_list, test_type='PA', dataset_name=None):
    perturbed_reports = protocol.memoized(user_trajectory_list)
    hmm_model.create_plain_protocol_model(protocol)
    guess_list = [hmm_model.guess_user_values(protocol, report) for report in perturbed_reports]
    return experiment_metrics(test_type, user_trajectory_list, guess_list, dataset_name)


def experiment_olh(protocol, hmm_model, user_trajectory_list, test_type='PA', dataset_name=None):
    guess_list = list()
    for user_index, user_trajectory in enumerate(user_trajectory_list):
        report = protocol.memoized(user_trajectory, user_index + 1)
        hmm_model.create_plain_protocol_model(protocol, user_index + 1)
        guess_list.append(hmm_model.guess_user_values(protocol, report))
    return experiment_metrics(test_type, user_trajectory_list, guess_list, dataset_name)


# Parameters for simulation
k = 20  # attribute's domain size (grid size)
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases
users_grid_value_list = list()
probability_of_guess_grr = list()
probability_of_guess_rappor = list()
probability_of_guess_oue = list()
probability_of_guess_olh = list()

user_trajectory_list = read_dataset('../../../dataset/geolife/geolife_grid.dat')

for epsilon in epsilon_list:
    print("Epsilon Value: " + str(epsilon))


    grr_model = HMM(k, epsilon)
    grr_m = GRR(k, epsilon)
    probability_of_guess_grr.append(experiment(grr_m, grr_model, user_trajectory_list, 'NDE', 'geolife'))
    print("GRR_M is Ready")

    rappor_model = HMM(k, epsilon)
    rappor_m = RAPPOR(k, epsilon)
    probability_of_guess_rappor.append(experiment(rappor_m, rappor_model, user_trajectory_list, 'NDE', 'geolife'))
    print("RAPPOR_M is Ready")

    oue_m = OUE(k, epsilon)
    oue_model = HMM(k, epsilon)
    probability_of_guess_oue.append(experiment(oue_m, oue_model, user_trajectory_list, 'NDE', 'geolife'))
    print("OUE is Ready")

    olh_m = OLH(k, 5)
    olh_model = HMM(k, 5)
    probability_of_guess_olh.append(experiment_olh(olh_m, olh_model, user_trajectory_list, 'NDE', 'geolife'))
    print("OLH is Ready")

print("GRR: " + str(probability_of_guess_grr))
print("RAPPOR: " + str(probability_of_guess_rappor))
print("OUE: " + str(probability_of_guess_oue))
print("OLH: " + str(probability_of_guess_olh))

plt.rcParams.update({'font.size': 12})
plt.figure(figsize=(4 * 1.33, 4 * 1.33))
plt.plot(epsilon_list, probability_of_guess_grr, linewidth=2, color='purple', marker='o', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="GRR_M")
plt.plot(epsilon_list, probability_of_guess_rappor, linewidth=2, color='grey', marker='s', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="RAPPOR_M")
plt.plot(epsilon_list, probability_of_guess_oue, linewidth=2, color='blue', marker='x', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="OUE_M")
plt.plot(epsilon_list, probability_of_guess_olh, linewidth=2, color='yellow', marker='x', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="OLH_M")
#plt.ylim(0, 1)
plt.title("GEOLIFE Dataset")
plt.ylabel("NDE")
plt.xlabel('Epsilon Values')
plt.grid(linestyle=':')
plt.legend(prop={'size': 12}, ncol=2, columnspacing=0.75)
plt.savefig('geolife_memoized_NDA.png', format='png', dpi=300, bbox_inches='tight')
plt.show()
