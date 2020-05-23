import matplotlib.pyplot as plt


x = ['20', '100', '1000', '10000']

DRAM_input_sorted = [0.013908, 0.060827, 0.217061, 2.124947]
DRAM_input_dense = [0.027701, 0.104493, 0.380807, 2.338634]
DRAM_input_sparse = [0.028409, 0.119760, 0.343643, 1.280082]

fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)
ax1.title.set_text('DRAM')
ax2.title.set_text('PMEM')

ax1.plot(x, DRAM_input_sorted, '-ok', color='red')
ax1.plot(x, DRAM_input_dense, '-bs')
ax1.plot(x, DRAM_input_sparse, '-g^')
ax1.set_xlabel("# Keys")
ax1.set_ylabel("Excecution Time")


PM_input_sorted = [0.000566, 0.001360, 0.002345, 0.002824]
PM_input_dense = [0.000564, 0.001446, 0.002732, 0.002869]
PM_input_sparse = [0.000532, 0.001693, 0.002717, 0.002803]

ax2.plot(x, PM_input_sorted, '-ok', color='red', label='Sorted Keys')
ax2.plot(x, PM_input_dense, '-bs', label='Dense Keys')
ax2.plot(x, PM_input_sparse, '-g^', label='Sparse Keys')
ax2.set_xlabel("# Keys")
ax2.set_ylabel("Excecution Time")

handles, labels = ax2.get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center')

plt.suptitle('Input Process Execution Time')
plt.savefig('input_execution_time.png')
plt.show()
