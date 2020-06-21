import matplotlib.pyplot as plt

x = ['1k', '10k', '100k']

fig, axs = plt.subplots(3, 3)
(ax11, ax12, ax13), (ax21, ax22, ax23), (ax31, ax32, ax33) = axs
fig.suptitle('Lock Coupling Execution Time on 2 Threads')

# ===================================================

DRAM_input_sorted = [1829, 4395, 41249]
DRAM_input_dense = [1952, 4309, 46726]
DRAM_input_sparse = [1682, 3575, 38327]

PM_input_sorted = [7025, 66060, 654831]
PM_input_dense = [7038, 65996, 651649]
PM_input_sparse = [7031, 66535, 654447]

DRAM_input_sorted = [number / 1000 for number in DRAM_input_sorted]
DRAM_input_dense = [number / 1000 for number in DRAM_input_dense]
DRAM_input_sparse = [number / 1000 for number in DRAM_input_sparse]

PM_input_sorted = [number / 1000 for number in PM_input_sorted]
PM_input_dense = [number / 1000 for number in PM_input_dense]
PM_input_sparse = [number / 1000 for number in PM_input_sparse]

ax11.plot(x, DRAM_input_sorted, '-or', label='DRAM Sorted Keys')
ax12.plot(x, DRAM_input_dense, '-sr', label='DRAM Dense Keys')
ax13.plot(x, DRAM_input_sparse, '-^r', label='DRAM Sparse Keys')

ax11.plot(x, PM_input_sorted, '-og', label='PMEM Sorted Keys')
ax12.plot(x, PM_input_dense, '-sg', label='PMEM Dense Keys')
ax13.plot(x, PM_input_sparse, '-^g', label='PMEM Sparse Keys')

ax11.set_title('Sorted')
ax12.set_title('Dense')
ax13.set_title('Sparse')

lines_labels = [ax.get_legend_handles_labels() for ax in fig.axes]
lines, labels = [sum(lol, []) for lol in zip(*lines_labels)]
fig.legend(lines, labels, loc='lower right')

plt.setp(axs[0, 0], ylabel='Input Time in Seconds')

# ===================================================

DRAM_look_sorted = [955, 3770, 41630]
DRAM_look_dense = [1398, 3619, 42630]
DRAM_look_sparse = [1091, 2964, 36624]

PM_look_sorted = [3041, 28798, 359052]
PM_look_dense = [2998, 28903, 361808]
PM_look_sparse = [2953, 28897, 358014]

DRAM_look_sorted = [number / 1000 for number in DRAM_look_sorted]
DRAM_look_dense = [number / 1000 for number in DRAM_look_dense]
DRAM_look_sparse = [number / 1000 for number in DRAM_look_sparse]

PM_look_sorted = [number / 1000 for number in PM_look_sorted]
PM_look_dense = [number / 1000 for number in PM_look_dense]
PM_look_sparse = [number / 1000 for number in PM_look_sparse]

ax21.plot(x, DRAM_look_sorted, '-or', label='DRAM Sorted Keys')
ax22.plot(x, DRAM_look_dense, '-sr', label='DRAM Dense Keys')
ax23.plot(x, DRAM_look_sparse, '-^r', label='DRAM Sparse Keys')

ax21.plot(x, PM_look_sorted, '-og', label='PMEM Sorted Keys')
ax22.plot(x, PM_look_dense, '-sg', label='PMEM Dense Keys')
ax23.plot(x, PM_look_sparse, '-^g', label='PMEM Sparse Keys')

plt.setp(axs[1, 0], ylabel='Lookup Time in Seconds')

# ===================================================
DRAM_input_sorted = [513, 4639, 48493]
DRAM_input_dense = [1685, 4499, 52674]
DRAM_input_sparse = [1494, 4075, 45501]

PM_input_sorted = [7320, 68718, 751044]
PM_input_dense = [7345, 68162, 758006]
PM_input_sparse = [7327, 68439, 753223]

DRAM_input_sorted = [number / 1000 for number in DRAM_input_sorted]
DRAM_input_dense = [number / 1000 for number in DRAM_input_dense]
DRAM_input_sparse = [number / 1000 for number in DRAM_input_sparse]

PM_input_sorted = [number / 1000 for number in PM_input_sorted]
PM_input_dense = [number / 1000 for number in PM_input_dense]
PM_input_sparse = [number / 1000 for number in PM_input_sparse]

ax31.plot(x, DRAM_input_sorted, '-or', label='DRAM Sorted Keys')
ax32.plot(x, DRAM_input_dense, '-sr', label='DRAM Dense Keys')
ax33.plot(x, DRAM_input_sparse, '-^r', label='DRAM Sparse Keys')

ax31.plot(x, PM_input_sorted, '-og', label='PMEM Sorted Keys')
ax32.plot(x, PM_input_dense, '-sg', label='PMEM Dense Keys')
ax33.plot(x, PM_input_sparse, '-^g', label='PMEM Sparse Keys')

plt.setp(axs[2, 0], ylabel='Remove Time in Seconds')

# ===================================================
plt.show()




