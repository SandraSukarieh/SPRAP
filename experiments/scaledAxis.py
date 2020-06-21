import matplotlib.pyplot as plt

x = ['1k', '10k', '100k']


def forward(x):
    return x ** (1 / 5)


def inverse(x):
    return x ** 5


fig, ax = plt.subplots()

DRAM_input_sorted = [1829, 4395, 41249]
PM_input_sorted = [7025, 66060, 654831]

DRAM_look_sorted = [955, 3770, 41630]
PM_look_sorted = [3041, 28798, 359052]

DRAM_remove_sorted = [513, 4639, 48493]
PM_remove_sorted = [7320, 68718, 751044]

DRAM_input_sorted = [number / 1000 for number in DRAM_input_sorted]
PM_input_sorted = [number / 1000 for number in PM_input_sorted]
DRAM_look_sorted = [number / 1000 for number in DRAM_look_sorted]
PM_look_sorted = [number / 1000 for number in PM_look_sorted]
DRAM_remove_sorted = [number / 1000 for number in DRAM_remove_sorted]
PM_remove_sorted = [number / 1000 for number in PM_remove_sorted]

ax.plot(x, DRAM_input_sorted, '-or', label='DRAM - input')
ax.plot(x, PM_input_sorted, '--og', label='PMEM - input')
ax.plot(x, DRAM_look_sorted, '-^r', label='DRAM - lookup')
ax.plot(x, PM_look_sorted, '--^g', label='PMEM - lookup')
ax.plot(x, DRAM_remove_sorted, '-sr', label='DRAM - remove')
ax.plot(x, PM_remove_sorted, '--sg', label='PMEM - remove')

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels, loc='lower right')


ax.set_yscale('function', functions=(forward, inverse))

plt.show()


