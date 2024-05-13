import numpy as np
from matplotlib import pyplot as plt

epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases




################## Brinkhoff Plain Attack on Plain Dataset ##################

dataset_name = "Brinkhoff"


grr_list_plain_on_stationary = [0.07001286899261154, 0.11161843632431834, 0.18067383095800812, 0.2792744669737171, 0.40144443616467446, 0.5345251924852811, 0.6590879047713245, 0.7643773955364974, 0.8981175320644923]
rappor_list_plain_on_stationary = [0.08423650225794538, 0.12678243631057695, 0.18437278228487214, 0.25753844572768775, 0.3436308604015894, 0.44177864942219747, 0.5388436565833767, 0.6235046634066603, 0.7493207864363951]
oue_list_plain_on_stationary = [0.08451795840577188, 0.13580071693740475, 0.21313546523466004, 0.30381707550123954, 0.3867955251556705, 0.4522713878221869, 0.4970320698284762, 0.5268810726244372, 0.5555088549246269]
olh_list_plain_on_stationary = [0.025888209014528277, 0.016767715402698075, 0.0015538841239425786, 0.14618872768480004, 0.24361252521985727, 0.3716959770754203, 0.5158785749360235, 0.6526740821289306, 0.8379827260604579]

"""
################## Geolife Plain Attack on Stationary Dataset ##################

dataset_name = "Geolife"


grr_list_plain_on_stationary =  [0.03569889608905023, 0.1008394193792996, 0.1674870701895634, 0.25332655833658513, 0.3748612173363498, 0.5131680627409552, 0.6219137679088661, 0.7398056483827987, 0.8776749287038615]
rappor_list_plain_on_stationary =  [0.05384429209697473, 0.11474206469158231, 0.17509659193663077, 0.26165397900224724, 0.36584474061982947, 0.4574635700830642, 0.54660231955944, 0.6359428235510652, 0.7812652097020637]
oue_list_plain_on_stationary =  [0.047746095713477744, 0.12570363686068856, 0.20740929037213968, 0.3049327073510442, 0.36805976646221394, 0.39061905192026347, 0.4312415320308886, 0.4892964811385496, 0.5200206825848509]
olh_list_plain_on_stationary =  [0.03756401694908515, 0.023494585815433573, 0.00011904761904761905, 0.12571593875845674, 0.22956208017211083, 0.3561828885007368, 0.5110452470517696, 0.6582050402727024, 0.840746145980398]





################## Taxi Plain Attack on Stationary Dataset ##################

dataset_name = "Taxi"

grr_list_plain_on_stationary =  [0.046282482815389124, 0.09617366454765816, 0.16849474857730062, 0.26360990917234245, 0.3840890492974602, 0.5167156185864729, 0.6442143854951207, 0.7508385040143558, 0.8915320098557492]
rappor_list_plain_on_stationary =  [0.05941860470498097, 0.10037859223970051, 0.15552319655079055, 0.2290015557699418, 0.31732233975583307, 0.41797191188665117, 0.5170865673812115, 0.6038841064551889, 0.7353154390103571]
oue_list_plain_on_stationary =  [0.0613080781671192, 0.11582159668857656, 0.1939146171636205, 0.2850763176175529, 0.36568540235504154, 0.42997650441441726, 0.4737069372584158, 0.5003020518563928, 0.5255065497594239]
olh_list_plain_on_stationary =  [0.025998640270355318, 0.017553869801645167, 0.0035399405353754724, 0.12524246430627722, 0.22525706919007218, 0.356682540440025, 0.5012694839414108, 0.6402071244421612, 0.8374865520135258]

"""


epsilon_list = epsilon_list[1:9:2] + [epsilon_list[-1]]


grr_list_plain_on_stationary = grr_list_plain_on_stationary[1:9:2] + [grr_list_plain_on_stationary[-1]]
rappor_list_plain_on_stationary = rappor_list_plain_on_stationary[1:9:2] + [rappor_list_plain_on_stationary[-1]]
oue_list_plain_on_stationary = oue_list_plain_on_stationary[1:9:2] + [oue_list_plain_on_stationary[-1]]
olh_list_plain_on_stationary = olh_list_plain_on_stationary[1:9:2] + [olh_list_plain_on_stationary[-1]]

plt.rcParams.update({'font.size': 20})
plt.figure(figsize=(4 * 1.33, 4 * 1.33))

# Adjust the left margin by specifying the left parameter in subplots_adjust
plt.subplots_adjust(left=0.20)  # Adjust the value as needed
plt.subplots_adjust(bottom=0.15)  # Adjust the value as needed

# Create bar charts for each dataset
bar_width = 0.2
epsilon_margin = 0.1  # Adjust the margin as needed

epsilon_list_with_margin = np.arange(len(epsilon_list))
"""
plt.bar(epsilon_list_with_margin - 0.3 - epsilon_margin, grr_list_stationary_on_plain, width=bar_width, color='purple', label="GRR")
plt.bar(epsilon_list_with_margin - epsilon_margin, rappor_list_stationary_on_plain, width=bar_width, color='grey', label="RAPPOR")
plt.bar(epsilon_list_with_margin + 0.15 - epsilon_margin, oue_stationary_on_plain, width=bar_width, color='blue', label="OUE")
plt.bar(epsilon_list_with_margin + 0.3 - epsilon_margin, olh_stationary_on_plain, width=bar_width, color='green', label="OLH")
"""

plt.bar(epsilon_list_with_margin - 1.5*bar_width, grr_list_plain_on_stationary, width=bar_width, color='purple', label="GRR")
plt.bar(epsilon_list_with_margin - 0.5*bar_width, rappor_list_plain_on_stationary, width=bar_width,color='grey', label="RAPPOR")
plt.bar(epsilon_list_with_margin + 0.5*bar_width, oue_list_plain_on_stationary, width=bar_width, color='blue', label="OUE")
plt.bar(epsilon_list_with_margin + 1.5*bar_width, olh_list_plain_on_stationary, width=bar_width, color='green', label="OLH")

# Adjust the x-axis tick positions to include margin
plt.xticks(epsilon_list_with_margin - epsilon_margin, epsilon_list, fontsize=20)
plt.yticks(fontsize=20)
plt.ylim(0, 1)
plt.ylabel("Prediction Accuracy", fontsize=20)
plt.xlabel('Epsilon', fontsize=20)
plt.grid(linestyle=':')
plt.legend(prop={'size': 15}, ncol=1, columnspacing=0.75, loc='upper left')
plt.title(dataset_name, fontsize=20)
plt.savefig(dataset_name + '_plain_on_stationary' + ".png", dpi=300)
plt.show()