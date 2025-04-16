# ipython3
import pyphi
import numpy as np
import itertools as it
# http://integratedinformationtheory.org/calculate.html

print()
print('UNCUT VERSION')
# transition probability matrix
# multi-dim state-by-node form
tpm = np.load("files_matrices/tpm1.npy", fix_imports=True)
tpm_sbs = pyphi.convert.state_by_node2state_by_state(tpm)
print()
print('Transition Probability Matrix (state-by-state form):')
print(tpm_sbs)
print()
cm = np.load("files_matrices/cm1.npy", fix_imports=True)
print('Connectivity Matrix:')
print(cm)
print()
netsize = np.shape(cm)[0]

# network nodes labels, numeration, network states list
node_indices = tuple(range(netsize))
start_states = list(it.product([0, 1], repeat = netsize))
unreachable_states = list()
# create network
network = pyphi.Network(tpm, cm=cm)
                        
# subsystem consists of network[selected nodes] + state
# calculate phi
for state in start_states:
	try:
		subsystem = pyphi.Subsystem(network, state, node_indices)
		pyphi_value = pyphi.compute.phi(subsystem)
		if(pyphi_value): print('state', state, ': pyphi value (uncut)= ', pyphi_value)
	except ValueError:
		unreachable_states.append(state)
		pass
# print unreachable states info parameter
for u_state in unreachable_states:
	print('state', u_state, ': unreachable (uncut)')
print()

print()
print('CUT VERSION')
tpm_cut = np.load("files_matrices/tpm1_cut.npy", fix_imports=True)
tpm_sbs_cut = pyphi.convert.state_by_node2state_by_state(tpm_cut)
print('Cut Transition Probability Matrix (state-by-state form):')
print(tpm_sbs_cut)
cm_cut = np.load("files_matrices/cm1_cut.npy", fix_imports=True)
print('Cut Connectivity Matrix:')
print(cm_cut)
print()
netsize = np.shape(cm_cut)[0]

# network nodes labels, numeration, network states list
node_indices = tuple(range(netsize))
start_states = list(it.product([0, 1], repeat = netsize))
unreachable_states = list()
# create network
network = pyphi.Network(tpm_cut, cm=cm_cut)
                        
# subsystem consists of network[selected nodes] + state
# calculate phi
for state in start_states:
	try:
		subsystem = pyphi.Subsystem(network, state, node_indices)
		pyphi_value = pyphi.compute.phi(subsystem)
		if(pyphi_value): print('state', state, ': pyphi value (cut)= ', pyphi_value)
	except ValueError:
		unreachable_states.append(state)
		pass
# print unreachable states info parameter
for u_state in unreachable_states:
	print('state', u_state, ': unreachable (cut)')
print()
