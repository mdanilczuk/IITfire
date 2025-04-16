'''
...-> [poisson -> OR] <-> [AND] <-> [XOR] <-...
!! _sim_functions_copy.py !!
'''
import numpy as np
import matplotlib.pyplot as plt
import _sim_functions as f
import itertools as it
import sys

netsize = 4
mean_diff = 10
## PARAMETERS
if len(sys.argv)==1:
	v_in = 50 		# [IF1 weight] input voltage (mV)
	v_rest = -100	# resting membrane potential (mV)
	v_thr = -50		# spike threshold (mV)
	tau_m = 0.1		# membrane time constant (ms)
else:
	## EXEC PARAMETERS OVERRIDE
	v_in = float(sys.argv[1])
	v_rest = float(sys.argv[2])
	v_thr = float(sys.argv[3])
	tau_m = float(sys.argv[4])
	if netsize == 4:
		mean_diff = float(sys.argv[5])

## SIM PARAMETERS
dt = 0.1 # Time-step duration (ms)
endtime = 100 # End of simulation (ms)
decay_weight = dt/tau_m
nsteps = int(endtime/dt) # Number of timesteps

if netsize == 4:
	entry_cm = np.array([
		[0, 1, 0, 0],
		[0, 0, 1, 1],
		[0, 1, 0, 1],
		[0, 1, 1, 0]
	])
	entry_thresholds = np.array([0, v_thr, 0, v_thr])
	entry_upper_thresholds = np.array([0, v_thr, 0, 0])
	entry_node_types = ['POISSON','OR','AND','XOR']
	entry_weights = f.get_weights_array(entry_cm, v_in, decay_weight)
elif netsize == 3:
	entry_cm = np.array([
		[0, 1, 1],
		[1, 0, 1],
		[1, 1, 0]
	])
	entry_thresholds = np.array([v_thr, 0, v_thr])
	entry_upper_thresholds = np.array([v_thr, 0, 0])
	entry_node_types = ['OR','AND','XOR']
	entry_weights = f.get_weights_array(entry_cm, v_in, decay_weight)
## CM EXPORT
np.save("files_matrices/cm1.npy", entry_cm)
cm_cut = np.delete(entry_cm, 0, 0)
cm_cut = np.delete(cm_cut, 0, 1)
np.save("files_matrices/cm1_cut.npy", cm_cut)

print 'Nsteps: ', nsteps
print 'decay_weight: ', decay_weight
print 'Node types: ', entry_node_types
print 'Weights: '
print entry_weights 
print 'Lower thresholds: ', entry_thresholds
print 'Upper thresholds: ', entry_upper_thresholds

# empty tpm array
spikes = np.zeros([netsize, nsteps])
tpm, denominator = f.empty_multi_tpm(netsize, spikes)
# empty tpm_cut array
spikes_cut = np.zeros([netsize-1, nsteps])
tpm_cut, denominator_cut = f.empty_multi_tpm(netsize-1, spikes_cut)

# all starting states
start_states = list(it.product([0, 1], repeat = netsize))
# calc tpm for every starting sate ; accumulate data
for state in start_states:
	spikes = f.simulation(nsteps, netsize, v_rest, mean_diff=mean_diff, weights=entry_weights, thresholds=entry_thresholds, upper_thresholds=entry_upper_thresholds, node_types=entry_node_types, starting_state=state, no_print=True)
	tpm, denominator = f.feed_tpm(tpm, denominator, spikes)
	spikes_cut = np.delete(spikes, 0, 1)
	tpm_cut, denominator_cut = f.feed_tpm(tpm_cut, denominator_cut, spikes_cut)

# calc real tpm
tpm = f.calculate_multi_tpm(tpm, denominator)
tpm_cut = f.calculate_multi_tpm(tpm_cut, denominator_cut)
## TPM EXPORT
np.save("files_matrices/tpm1.npy", tpm)
np.save("files_matrices/tpm1_cut.npy", tpm_cut)
