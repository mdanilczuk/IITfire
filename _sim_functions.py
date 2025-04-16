import numpy as np
import itertools as it
import matplotlib.pyplot as plt
# source: alt_f1.py

def get_node_types(netsize, entry_node_types):
	legal_node_types = ['POISSON', 'OR', 'AND', 'XOR', 'CUSTOM']
	if entry_node_types is not None:
		if all(item in legal_node_types for item in entry_node_types):
			if len(entry_node_types) == netsize:
				return entry_node_types
	node_types = []
	for node in range(netsize):
		node_type = ''
		while node_type not in legal_node_types:
			node_type = raw_input("type of node? (POISSON, OR, AND, XOR, CUSTOM) ")
		node_types.append(node_type)
		print 'successfully added a node; current types:'
		print node_types
	return node_types

def get_weights_array(cm, standard_weight, decay_weight):
	weights_array = np.copy(cm)*standard_weight*1.
	## decay weight = dt/tau_m ; at 1=> full reset each step
	for node in range(np.shape(cm)[0]):
		weights_array[node,node] = decay_weight*1.
	return weights_array

def get_thresholds_array(netsize, standard_threshold):
	return np.ones(netsize)*standard_threshold
	
def create_network(netsize, connectivity_matrix, entry_node_types=None, entry_weights=None, standard_weight=2, decay_weight=1, entry_thresholds=None, entry_upper_thresholds=None, standard_threshold=5):
	if np.shape(connectivity_matrix) != (netsize, netsize):
		print 'ERROR'
	node_types = get_node_types(netsize, entry_node_types)
	weights_array = get_weights_array(connectivity_matrix, standard_weight, decay_weight)
	if entry_weights is not None:
		if np.shape(entry_weights) == np.shape(connectivity_matrix):
			weights_array = entry_weights
	thresholds_array = get_thresholds_array(netsize, standard_threshold)
	if entry_thresholds is not None:
		if len(entry_thresholds) == len(connectivity_matrix[0]):
			thresholds_array = entry_thresholds
	upper_thresholds_array = np.copy(thresholds_array)
	if entry_upper_thresholds is not None:
		if len(entry_upper_thresholds) == len(connectivity_matrix[0]):
			upper_thresholds_array = entry_upper_thresholds		
	print node_types
	print weights_array
	print thresholds_array
	print upper_thresholds_array

def membrane(nsteps, netsize, v_rest, node_types):
	## Membrane Potentials array
	v_membrane = np.ones([nsteps, netsize])*v_rest*1.
	for node in range(len(node_types)):
		if node_types[node] == 'POISSON':
			v_membrane[:,node] = 0
	return v_membrane

def binary_states(nsteps, netsize, node_types, mean_diff=10):
	## Binary State array
	spikes = np.zeros([nsteps, netsize])
	# random input; spikes freq = 1/mean_diff
	for node in range(len(node_types)):
		if node_types[node] == 'POISSON':
			spikes[:,node] = np.random.randint(mean_diff, size=nsteps)/(mean_diff-1) # binary array input of random spikes
	return spikes

def simulation(nsteps, netsize, v_rest, weights, thresholds, upper_thresholds, node_types=['empty'], mean_diff=10, starting_state=[0,0,1], no_print=True):
	## SIMULATION
	# for each timestep:
	#	CELL 1: membrane potential update (previous V + time constant influence + inputs)
	#	if membrane potential exceeds threshold:
	#		denote the spike in spikes array
	#		reset the membrane potential voltage
	v_mem = membrane(nsteps, netsize, v_rest, node_types=node_types)
	v_mem_step_plot = np.copy(v_mem)
	spikes = binary_states(nsteps, netsize, node_types, mean_diff=mean_diff)
	input_indices = []
	non_input_indices = []
	for n_index in range(len(node_types)):
		if node_types[n_index] == 'POISSON':
			input_indices.append(n_index)
		else:
			non_input_indices.append(n_index)
	spikes[0,] = starting_state
	if not no_print:
		print 'Input indices: ', input_indices
		print 'Non-input indices: ', non_input_indices
		print 'Starting network from state: ', spikes[0,]
	for step in range(1,nsteps):
		v_mem_step = np.zeros(netsize)
		for node in non_input_indices:
			# previous step + time constant influence
			v_mem[step,node] = v_mem[step-1,node] + weights[node,node]*(-v_mem[step-1,node]+v_rest)
			# the rest of the inputs
			for ref_node in range(netsize):
				if ref_node != node:
					v_mem[step,node] += weights[ref_node,node]*spikes[step-1,ref_node]
			# is threshold reached ?
			v_mem_step[node] = v_mem[step,node]
			if v_mem[step,node] >= thresholds[node]:
				spikes[step,node] = 1
				if upper_thresholds[node] > thresholds[node]:
					if v_mem[step,node] >= upper_thresholds[node]:
						spikes[step,node] = 0
						## ???
						v_mem[step,node] = v_rest
				elif upper_thresholds[node] == thresholds[node]:
					v_mem[step,node] = v_rest
		v_mem_step_plot[step,:] = v_mem_step
		# PRINT STEPS
		if not no_print:
			print 'step: ', step 
			print 'v_mem: ', v_mem_step
			print 'spiks: ', spikes[step,]
			raw_input()
	#extrapolation start
	#Delta = 0.1
	#t_span=2.2
	#V[i=step][k=node] - membrane potential
	#T_U=np.linspace(0,t_span,len(V)/Delta) - extrapolation time vector
	#t_f[k=node][j=step] - spike timestamps =0 / =200
	#v_rest=0 (resting potential)
	#v_spike=150 (spike potential)
	#v_hyper=-25 (hyperpolarization potential)
	if False:
		U=[]
		for k in range(3):
			u=[]
			for i in range(len(V[:,0])):            #storing potential in a bigger vector with 9 additional time steps between
				u.append(V[i][k])
				for j in range(9):
					u.append(0)
				
			for i in range(len(u)):                 #adding exponential term in between big time steps
				if u[i]==0:
					if i<10:
						u[i]=u[0]*np.exp(-Delta*0.1*(i)/tau)
					if i>=10 and i<100:
						u[i]=u[int(str(i)[0])*10]*np.exp(-Delta*0.1*(i-(int(str(i)[0])*10))/tau)
					if i>=100 and i<1000:
						u[i]=u[int(str(i)[0])*100]*np.exp(-Delta*0.1*(i-(int(str(i)[0])*100))/tau)
					if i>=1000:
						print("Simulation time too big, adjust the code")
						break			
			for i in range(len(u)):                 #adding spikes and hyperpolarization
				for j in range(len(t_f[k])):
					if t_f[k][j]==200:
						if i*0.1==j:
							u[i]=v_spike
							for l in range(i+1,i+10):
								u[l]=v_hyper					
			for i in range(len(u)):
				if u[i]>150:
					u[i]=v_spike
					for l in range(i+1,i+10):
						u[l]=v_hyper
			U.append(u)
		
		fig=plt.figure(figsize=(7.8,4.8))
		#alternative: violet, green, orange
		plt.plot(T_U,U[0],'red',label='AND')
		plt.plot(T_U,U[1],'green', label='OR')
		plt.plot(T_U,U[2],'blue',label='XOR')
		#plt.plot([],[],' ',label=r'$state = (0,0,0)$')
		#plt.plot([],[],' ',label=r'$\Phi \approx 1.0$')
		#plt.plot([],[],' ',label=r'$w = 65.0mV$')
		#plt.plot([],[],' ',label=r'$\tau = 0.4ms$')
		ax = fig.add_subplot(1, 1, 1)
		ax.set_xticks(np.arange(0,t_span+Delta,0.1))
		ax.set_ylim(-30,200)
		plt.grid()
		plt.xlabel('Time [s]')
		plt.ylabel('Membrane potential [mV]')
		#plt.title('Membrane potential as a function of time for three neuron logic gates')
		plt.legend(loc='lower right')
		t=ax.text(0.85,165,r'$\Phi \approx 0$',fontsize=30)
		t.set_bbox(dict(facecolor='white',alpha=0.3))
		#plt.savefig('010_03_memory_78_weights_new.pdf')
		plt.show()
	#extrapolation end
	## PLOT
	if not no_print:
		fig1 = plt.figure()
		for node in range(netsize):
			plt.plot(range(nsteps), v_mem_step_plot[:,node])
			plt.plot(range(nsteps), (spikes[:,node]))
		plt.show()
	return spikes

# TPM calculations
def empty_multi_tpm(netsize, net_states):
	''' gets 2dimensional network states-by-timepoints matrix
	creates EMPTY multidimensional state-by-node transition-probability-matrix
	dimensions: [2]*n + [n]
	and an additional [2]*n denominator matrix for counting probabilities
	'''
	size = np.shape(net_states)[-1]
	s1=[]
	for dim in xrange(netsize):
		s1.append(2)
	s2 = list(s1)
	s2.append(netsize)
	return np.zeros(s2), np.zeros(s1)
	
def feed_tpm(tpm, denom, feed):
	''' filling out an empty multidimensional state-by-node tpm template with tpm values
	and increase adequate denominators
	'''
	for i in xrange(len(feed)-1):
		address = tuple(feed[i])
		print address
		raw_input()
		values = feed[i+1]
		tpm[address] += values
		denom[address] += 1
	return tpm, denom

def calculate_multi_tpm(tpm, denom):
	''' calculates multi-dim state-by-node tpm
	'''
	size = np.shape(tpm)[-1]
	start_states = list(it.product([0, 1], repeat = size))
	for state in start_states:
		if sum(tpm[state]) != 0:
			tpm[state] /= denom[state]
	return tpm
