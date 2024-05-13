import numpy as np
from matplotlib import pyplot as plt

epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases




################## Brinkhoff SIM Attack on Transit Dataset ##################

dataset_name = "Brinkhoff"


grr_list =  [0.12420125651076626, 0.29098426676690115, 0.47113784030499917, 0.5677925146324437, 0.6075283251892821, 0.6152606991354777, 0.6231541642055523, 0.6228319819577941, 0.626912957096064]
rappor_list =  [0.2119422219835687, 0.4420340439241798, 0.5594694732320249, 0.5980239488804167, 0.6137034849379799, 0.6186973097782312, 0.6228319819577941, 0.6229393760403802, 0.6243354991139988]
oue_list =  [0.2121570101487408, 0.43725500724910055, 0.5534554046072061, 0.5938892767008538, 0.6069376577350588, 0.6113408151210868, 0.6142941523922032, 0.6169790044568544, 0.6208451914299522]
olh_list =  [0.06996724480481126, 0.05992589808301563, 0.053106373838801485, 0.1956720184717822, 0.3256188584009021, 0.40444611501906247, 0.4787628201686087, 0.5351984105675778, 0.5867475702088815]




################## Geolife SIM Attack on Transit Dataset ##################

dataset_name = "Geolife"


grr_list =  [0.12220094284030643, 0.24889510901591044, 0.40748379493223336, 0.53601944608132, 0.6311137301119623, 0.6828226281673542, 0.7114024749558043, 0.7285651149086624, 0.7447701826753094]
rappor_list =  [0.18923099587507367, 0.36829699469652327, 0.5167206835592222, 0.5978933411903359, 0.6498232174425457, 0.6829699469652327, 0.7018267530936948, 0.7123600471420153, 0.729449027695934]
oue_list =  [0.18959929286977018, 0.3702857984678845, 0.5141426045963465, 0.5841190335886859, 0.6351649970536241, 0.6686063641720683, 0.6873158515026517, 0.6965969357690042, 0.7140542133176193]
olh_list =  [0.07307012374779022, 0.06054802592810843, 0.05023571007660577, 0.17626694166175605, 0.319387153800825, 0.452857984678845, 0.5494254566882735, 0.6181496758986447, 0.6949027695934001]






################## Taxi SIM Attack on Transit Dataset ##################

dataset_name = "Taxi"

grr_list =  [0.0856655322101276, 0.15287973823118536, 0.24778030920972444, 0.33340833872434583, 0.3858464827159452, 0.4102513618166306, 0.4189613628479547, 0.426368145210437, 0.4331655087709429]
rappor_list =  [0.12346824928041703, 0.22241911137363, 0.30428749566375085, 0.35826325017110605, 0.39023429809017524, 0.40514161955390543, 0.413926625976242, 0.4203114598861793, 0.4265556586879682]
oue_list =  [0.12421830319054182, 0.22434112451832475, 0.3105316944655397, 0.36131971985486455, 0.39027180078568147, 0.40450407373029934, 0.41478918797288555, 0.4185675845451392, 0.42498054547670616]
olh_list =  [0.06295765008109958, 0.058691718467264835, 0.05097553886685605, 0.12269944402253911, 0.21130893782990653, 0.2776324548326911, 0.3295736881088328, 0.3643480625169934, 0.40784181363035465]



for value in olh_list:
    print(value)

epsilon_list = epsilon_list[1:9:2] + [epsilon_list[-1]]

grr_list_stationary_on_plain = grr_list[1:9:2] + [grr_list[-1]]
rappor_list_stationary_on_plain = rappor_list[1:9:2] + [rappor_list[-1]]
oue_stationary_on_plain = oue_list[1:9:2] + [oue_list[-1]]
olh_stationary_on_plain = olh_list[1:9:2] + [olh_list[-1]]

grr_list_plain_on_stationary = grr_list[1:9:2] + [grr_list[-1]]
rappor_list_plain_on_stationary = rappor_list[1:9:2] + [rappor_list[-1]]
oue_list_plain_on_stationary = oue_list[1:9:2] + [oue_list[-1]]
olh_list_plain_on_stationary = olh_list[1:9:2] + [olh_list[-1]]

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

plt.bar(epsilon_list_with_margin - 1.5*bar_width, grr_list_stationary_on_plain, width=bar_width, color='purple', label="GRR")
plt.bar(epsilon_list_with_margin - 0.5*bar_width, rappor_list_stationary_on_plain, width=bar_width,color='grey', label="RAPPOR")
plt.bar(epsilon_list_with_margin + 0.5*bar_width, oue_stationary_on_plain, width=bar_width, color='blue', label="OUE")
plt.bar(epsilon_list_with_margin + 1.5*bar_width, olh_stationary_on_plain, width=bar_width, color='green', label="OLH")

# Adjust the x-axis tick positions to include margin
plt.xticks(epsilon_list_with_margin - epsilon_margin, epsilon_list, fontsize=20)
plt.yticks(fontsize=20)
plt.ylim(0, 1)
plt.ylabel("Prediction Accuracy", fontsize=20)
plt.xlabel('Epsilon', fontsize=20)
plt.grid(linestyle=':')
plt.legend(prop={'size': 15}, ncol=1, columnspacing=0.75, loc='upper left')
plt.title(dataset_name, fontsize=20)
plt.savefig(dataset_name + '_SIM_on_transit' + ".png", dpi=300)
plt.show()