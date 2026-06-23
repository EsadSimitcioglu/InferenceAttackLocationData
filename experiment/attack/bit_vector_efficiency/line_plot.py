import matplotlib.pyplot as plt

epsilon_list = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 5]

# Data for taxi dataset
rappor_old_taxi = [
    0.051989736873873385,
    0.0906273057437031,
    0.14245611323512503,
    0.21355167806338204,
    0.3007371895584127,
    0.4013867769459646,
    0.5007204387206239,
    0.5896005758226767,
    0.7279114858193418,
]
rappor_taxi = [
    0.024354025978157983,
    0.030328316271744576,
    0.05099461307180185,
    0.11366587523166376,
    0.21735380326278028,
    0.3506352856722425,
    0.47147677197922383,
    0.5800858150189706,
    0.7248836212725002,
]
oue_old_taxi = [
    0.05320375812142479,
    0.10597715469259238,
    0.1825729224192001,
    0.27331364004099434,
    0.358676566394449,
    0.42499245647403266,
    0.4719633702376692,
    0.5019168762780201,
    0.5310953624181206,
]
oue_taxi = [
    0.024576989922129158,
    0.07070194120314029,
    0.1679942591134337,
    0.26823059592271775,
    0.3549856925255128,
    0.4222770559413304,
    0.47023195210028557,
    0.4985421588278808,
    0.526463110777038,
]

# Data for geolife dataset
rappor_old_geolife = [
    0.02813539535574602,
    0.056543094310166776,
    0.0981712419222701,
    0.16087633874558863,
    0.24134390083707394,
    0.3361649517573284,
    0.4346210727092785,
    0.5247585730723249,
    0.6720575104993135,
]
rappor_geolife = [
    0.01014613520978967,
    0.01885200788029361,
    0.042600908394158706,
    0.09628669454603439,
    0.20299728922014929,
    0.3094069718994491,
    0.43563312398088566,
    0.5286509369422198,
    0.6861050671522408,
]
oue_old_geolife = [
    0.030244834015282385,
    0.07372113826814565,
    0.14978891022935073,
    0.2407298063092807,
    0.32430823508119927,
    0.38659738269318283,
    0.43221394737576907,
    0.4620932034697193,
    0.4916296216005553,
]
oue_geolife = [
    0.010781393865510342,
    0.058508093761091305,
    0.15205828948248282,
    0.24633376026830034,
    0.3322171298653869,
    0.3915945249448328,
    0.43794268783852597,
    0.4686434270018363,
    0.49506710080294636,
]

# Data for brinkhoff dataset
rappor_old_brinkhoff = [
    0.07058072956759658,
    0.11537315216211196,
    0.1687483942170693,
    0.24320436257183273,
    0.3294138244648792,
    0.42841026713416064,
    0.5257198936325191,
    0.6113813114717613,
    0.7417202077170573,
]
rappor_brinkhoff = [
    0.03941494927520921,
    0.05780228401656927,
    0.09753968917457725,
    0.154516081912981,
    0.2402617864055907,
    0.34617062968927564,
    0.47214339456932847,
    0.5756893987346133,
    0.7309551216742718,
]
oue_old_brinkhoff = [
    0.07345253032719255,
    0.12458890828145316,
    0.20119596168989715,
    0.29418017442857536,
    0.37863340677258905,
    0.44382984258862723,
    0.49019892777016194,
    0.5188784544073446,
    0.5480257640037582,
]
oue_brinkhoff = [
    0.0480633814138634,
    0.0993641831439173,
    0.16613735518193953,
    0.267277342375572,
    0.3589191205314367,
    0.43264760165398736,
    0.4784280689118538,
    0.5116474555842285,
    0.5393189474525526,
]

# Your existing code for creating the plot
plt.rcParams.update({"font.size": 20})
fig, ax = plt.subplots(figsize=(4 * 1.33, 4 * 1.33))

# Adjust the left margin by specifying the left parameter in subplots_adjust
plt.subplots_adjust(left=0.20)  # Adjust the value as needed
plt.subplots_adjust(bottom=0.15)  # Adjust the value as needed

# Adjust the left margin by specifying the left parameter in subplots_adjust
plt.subplots_adjust(left=0.20)  # Adjust the value as needed
plt.subplots_adjust(bottom=0.15)  # Adjust the value as needed
plt.plot(
    epsilon_list,
    rappor_old_taxi,
    linewidth=2,
    color="gray",
    marker="o",
    markersize=15,
    mew=1.5,
    fillstyle="none",
    clip_on=False,
    label="RAPPOR Old",
)  # Blue
plt.plot(
    epsilon_list,
    rappor_taxi,
    linewidth=2,
    color="black",
    marker="s",
    markersize=15,
    mew=1.5,
    fillstyle="none",
    clip_on=False,
    label="RAPPOR",
)  # Orange
plt.plot(
    epsilon_list,
    oue_old_taxi,
    linewidth=2,
    color="blue",
    marker="x",
    markersize=15,
    mew=1.5,
    fillstyle="none",
    clip_on=False,
    label="OUE Old",
)  # Green
plt.plot(
    epsilon_list,
    oue_taxi,
    linewidth=2,
    color="red",
    marker="x",
    markersize=15,
    mew=1.5,
    fillstyle="none",
    clip_on=False,
    label="OUE",
)  # Red
# Select specific values from epsilon_list to display on the x-axis
selected_epsilon_values = [
    epsilon_list[0],
    epsilon_list[2],
    epsilon_list[4],
    epsilon_list[6],
    epsilon_list[8],
]
# Set the x-axis tick positions and labels
plt.xticks(selected_epsilon_values, fontsize=20)
plt.yticks(fontsize=20)
plt.ylim(0, 1)
plt.title("Taxi", fontsize=20)
plt.ylabel("PA", fontsize=20)
plt.xlabel("Epsilon")
plt.grid(linestyle=":")
plt.legend(prop={"size": 15}, ncol=1, columnspacing=0.75, loc="upper right")
plt.show()
