from matplotlib import pyplot as plt

iter_list = [1, 3, 5, 7, 9]
epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]  # number of epsilon for test cases



data = {
    'Taxi': {
        'GRR': [8.3935, 10.6891, 8.7574, 4.7993, 2.0370, 0.9904, 0.5733, 0.3746, 0.1574],
        'RAPPOR': [11.0172, 9.9631, 5.5411, 2.5704, 1.3215, 0.7908, 0.5681, 0.4282, 0.2534],
        'OUE': [10.9300, 9.9718, 5.7642, 3.0109, 1.7565, 1.1867, 0.9175, 0.7195, 0.5587],
        'OLH': [32.4506, 33.9907, 37.4862, 22.2921, 16.5548, 11.7089, 7.4596, 4.5303, 1.6199]
    },
    'Geolife': {
        'GRR': [0.0318, 0.0323, 0.0302, 0.0164, 0.0114, 0.0032, 0.0019, 0.0033, 0.0002],
        'RAPPOR': [0.0284, 0.0295, 0.0142, 0.0111, 0.0038, 0.0016, 0.0010, 0.0012, 0.0006],
        'OUE': [0.0339, 0.0209, 0.0205, 0.0135, 0.0123, 0.0039, 0.0062, 0.0045, 0.0012],
        'OLH': [0.2821, 0.2588, 0.2928, 0.2111, 0.1581, 0.1136, 0.0813, 0.0589, 0.0170]
    },
    'Brinkhoff': {
        'GRR': [2.8053, 2.4790, 1.2864, 0.4957, 0.2259, 0.1197, 0.0718, 0.0529, 0.0308],
        'RAPPOR': [5.4639, 2.8706, 1.0567, 0.5100, 0.3185, 0.2343, 0.1876, 0.1389, 0.0936],
        'OUE': [5.4603, 2.8941, 1.1430, 0.5804, 0.3798, 0.2784, 0.2337, 0.2064, 0.1465],
        'OLH': [21.0953, 21.7840, 23.2309, 13.7735, 10.1257, 7.4166, 4.7534, 2.9631, 1.1152]
    }
}

plt.rcParams.update({'font.size': 12})
plt.figure(figsize=(4 * 1.33, 4 * 1.33))
plt.plot(epsilon_list, data["Brinkhoff"]["GRR"], linewidth=2, color='purple', marker='o', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="GRR")
plt.plot(epsilon_list, data["Brinkhoff"]["RAPPOR"], linewidth=2, color='grey', marker='s', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="RAPPOR")
plt.plot(epsilon_list, data["Brinkhoff"]["OUE"], linewidth=2, color='blue', marker='x', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="OUE")
plt.plot(epsilon_list, data["Brinkhoff"]["OLH"], linewidth=2, color='green', marker='d', markersize=10, mew=1.5,
         fillstyle='none', clip_on=False, label="OLH")
plt.xticks(fontsize=15)
plt.yticks(fontsize=10)
plt.ylabel("Path Metric")
plt.xlabel('Epsilon')
plt.grid(linestyle=':')
plt.legend(prop={'size': 12}, ncol=2, columnspacing=0.75)
plt.title("Brinkhoff")
# Add "x10^-3" at the top of the y-axis
plt.annotate("x$10^{-2}$", (0, 1.02), xycoords='axes fraction', fontsize=10)

plt.show()