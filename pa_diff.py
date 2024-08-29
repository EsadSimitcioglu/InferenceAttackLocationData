import np
from matplotlib import pyplot as plt

epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]
defences = ["GRR_M", "RAPPOR", "OUE", "OLH"]
dataset_name = 'brinkhoff'
five = [0.06502317334766453, 0.12156706031501058, 0.15056566853615183, 0.1781669859030715, 0.18142090056819493,
        0.1655867748855112, 0.14806414125407086, 0.1253253225665688, 0.08475336116891052]
ten = [0.01474095387182002, 0.04935638088728675, 0.10976709917577068, 0.15992547761572468, 0.20059309234822678,
       0.22810353760844876, 0.23637798429444423, 0.22735298548871324, 0.18552141783613152]
fiveteen = [0.03270786346536337, 0.04658548573055951, 0.0958186152694267, 0.15205761978475263, 0.2062553111348948,
            0.24826300050986894, 0.28015231760701503, 0.2871710541425703, 0.2473020583087968]
twenty = [0.03406053381574613, 0.071905915425292, 0.11028925562442846, 0.16945199582833398, 0.20431564078261677,
          0.2606955422919206, 0.28435569395240273, 0.3109424591207272, 0.25838364370037775]
twenty_five = [0.0025851876282143756, 0.014762395166231977, 0.04301572150528843, 0.09095836598503089,
               0.14954952140956118, 0.22346439028064996, 0.30164013343022433, 0.3688596052030805, 0.4073746748993347]


# Your existing code for creating the plot
plt.rcParams.update({'font.size': 20})
fig, ax = plt.subplots(figsize=(4 * 1.33, 4 * 1.33))

# Adjust the left margin by specifying the left parameter in subplots_adjust
plt.subplots_adjust(left=0.20)  # Adjust the value as needed
plt.subplots_adjust(bottom=0.15)  # Adjust the value as needed
plt.plot(epsilon_list, five, linewidth=2, color='purple', marker='o', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="1x5")
plt.plot(epsilon_list, ten, linewidth=2, color='grey', marker='s', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="2x5")
plt.plot(epsilon_list, fiveteen, linewidth=2, color='blue', marker='x', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="3x5")
plt.plot(epsilon_list, twenty, linewidth=2, color='yellow', marker='x', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="4x5")
plt.plot(epsilon_list, twenty_five, linewidth=2, color='green', marker='x', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="5x5")
plt.xticks(fontsize=15)
# Select specific values from epsilon_list to display on the x-axis
selected_epsilon_values = [epsilon_list[0], epsilon_list[2], epsilon_list[4], epsilon_list[6], epsilon_list[8]]
# Set the x-axis tick positions and labels
plt.xticks(selected_epsilon_values, fontsize=20)
plt.title("Brinkhoff")
plt.ylabel("PA Difference")
plt.xlabel('Epsilon')
plt.grid(linestyle=':')
plt.legend(prop={'size': 15}, ncol=2, columnspacing=0.75)
plt.show()
