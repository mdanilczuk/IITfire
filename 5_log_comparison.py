import sys
import itertools as it
import numpy as np
import matplotlib.pylab as plt

### REFERENCE DICTIONARY (baseline, inputless)
if len(sys.argv)==1:
	prefix = '8x8'
	fpath = 'files_logs/log_1_01_22_21_05_49_17.txt'
else:
	pass
f = open(fpath)

### KEY SETS
# assume 3-nodes network
netsize = 3
# read state keys (as strings)
state_keys = list(it.product([0, 1], repeat = netsize))
state_keys_string = []
for s_key_tuple in state_keys:
	s_key_string = ''+str(s_key_tuple)+''
	state_keys_string.append(s_key_string)
state_keys = state_keys_string
# read parameter keys (as floats)
weight_keys = []
tau_keys = []
for line in f:
	if 'Standard weight' in line:
		w_key = float(line[17:])
		if w_key not in weight_keys: weight_keys.append(w_key)
	if 'Tau constant' in line:
		t_key = float(line[14:])
		if t_key not in tau_keys: tau_keys.append(t_key)
f.close()
# construct key sets
key_sets = []
for wk in weight_keys:
	for tk in tau_keys:
		for sk in state_keys:
			if (wk, tk, sk) not in key_sets:
				key_sets.append((wk, tk, sk))
# check 5x5 params x2^3states = 200
if len(weight_keys)*len(tau_keys)*len(state_keys) != len(key_sets): print 'keys error'

### DICTIONARY
pyphi_dict_ref = dict([(k_set,'0') for k_set in key_sets])
f = open(fpath)
for line in f:
	if 'Standard weight' in line: current_w_key = float(line[17:])
	if 'Tau constant' in line: current_t_key = float(line[14:])
	if 'state (' in line:
		current_s_key = line[6:15]
		if 'unreachable' in line:
			pyphi_dict_ref[(current_w_key, current_t_key, current_s_key)] = 'unreachable'
		else:
			pyphi_dict_ref[(current_w_key, current_t_key, current_s_key)] = float(line[32:])

### GET LOG FILE PATH
if len(sys.argv)==1:
	#prefix = '5x5'
	#fpath = 'alt_logs/alt_log_8_06_12_19_12_47_25.txt'
	prefix = '8x8'
	#fpath = 'zPoisson/7x7/uncut_cut_log.txt'
	#fpath = 'zPoisson/7x7/2020alt_log_7_11_12_20_04_26_08.txt'
	#fpath = 'zPoisson/7x7/2020alt_log_7_11_12_20_04_38_30.txt'
	fpath = 'files_logs/log_1_01_22_21_08_26_59.txt'
	#prefix = '10x10'
	#fpath = 'alt_logs/alt_log_8_06_17_19_08_39_37.txt'
else:
	pass
f = open(fpath)

### KEY SETS
# assume 3-nodes network
netsize = 3
# read state keys (as strings)
state_keys = list(it.product([0, 1], repeat = netsize))
state_keys_string = []
for s_key_tuple in state_keys:
	s_key_string = ''+str(s_key_tuple)+''
	state_keys_string.append(s_key_string)
state_keys = state_keys_string
# read parameter keys (as floats)
weight_keys = []
tau_keys = []
poiss_keys = []
for line in f:
	if 'Standard weight' in line:
		w_key = float(line[17:])
		if w_key not in weight_keys: weight_keys.append(w_key)
	if 'Tau constant' in line:
		t_key = float(line[14:])
		if t_key not in tau_keys: tau_keys.append(t_key)
	if 'Mean Poisson difference' in line:
		p_key = float(line[25:])
		if p_key not in poiss_keys: poiss_keys.append(p_key)
f.close()
# raw_input()
# construct key sets
key_sets = []
for pk in poiss_keys:
	for wk in weight_keys:
		for tk in tau_keys:
			for sk in state_keys:
				if (pk, wk, tk, sk) not in key_sets:
					key_sets.append((pk, wk, tk, sk))
# check 5x5 params x2^3states = 200
if len(poiss_keys)*len(weight_keys)*len(tau_keys)*len(state_keys) != len(key_sets): print 'keys error'

### DICTIONARY
pyphi_dict = dict([(k_set,0) for k_set in key_sets])
counter_dict = dict([(k_set,0) for k_set in key_sets])
f = open(fpath)
for line in f:
	if 'Mean Poisson difference' in line: current_p_key = float(line[25:])
	if 'Standard weight' in line: current_w_key = float(line[17:])
	if 'Tau constant' in line: current_t_key = float(line[14:])
	if 'state (' in line:
		current_s_key = line[6:15]
		if 'unreachable' in line:
			pyphi_dict[(current_p_key, current_w_key, current_t_key, current_s_key)] = 'unreachable'
		else:
			print pyphi_dict[(current_p_key, current_w_key, current_t_key, current_s_key)]
			pyphi_dict[(current_p_key, current_w_key, current_t_key, current_s_key)] += float(line[37:])
			counter_dict[(current_p_key, current_w_key, current_t_key, current_s_key)] += 1
if False:
	for key, value in counter_dict.items():
		print key, ': ', value
# raw_input()
if False:
# for mean PHI from different Poisson means: delete p_keys
	for key, value in pyphi_dict.items():
		pyphi_dict[key] /= np.maximum(1,counter_dict[key])
# print
if False:
	for wk in weight_keys:
		for tk in tau_keys:
			for key, value in pyphi_dict.items():
				if (wk in key) and (tk in key):
					print key, ': ', value
# raw_input()
### NUMBER OF CALCULATED PHI'S
wk_len = len(weight_keys)
tk_len = len(tau_keys)
pk_len = len(poiss_keys)
full_data = np.zeros([pk_len, wk_len, tk_len])
# calculate
tau_keys.sort()
weight_keys.reverse()
print weight_keys
print tau_keys
print poiss_keys
#raw_input()
for pk_i in range(pk_len):
	pk = poiss_keys[pk_i]
	for wk_i in range(wk_len):
		wk = weight_keys[wk_i]
		for tk_i in range(tk_len):
			tk = tau_keys[tk_i]
			for key, value in pyphi_dict.items():
				if (pk in key) and (wk in key) and (tk in key) and isinstance(value,float):
					full_data[pk_i, wk_i, tk_i] += 1		
for pk_i in range(pk_len):
	pk = poiss_keys[pk_i]
	data = full_data[pk_i,:,:]
	# plot
	fig1 = plt.figure()
	plt.imshow(data, cmap='hot', interpolation='nearest')
	plt.colorbar()
	plt.yticks(range(wk_len), weight_keys)
	plt.ylabel('Standard weight parameter')
	plt.xticks(range(tk_len), tau_keys)
	plt.xlabel('Tau constant parameter')
	plt.title('Number of non-trivial phi values calculated in a simulation \n as a function of weight and tau parameters')
	#plt.show()
	### ALL PHI
	# 1) zwiekszyc zakres colorbar ?
	# 2) poprawic obszar
	wk_len = len(weight_keys)
	tk_len = len(tau_keys)
	sk_len = len(state_keys)
	#plt.savefig('2020comparison/'+prefix+'_mean_poiss_'+str(pk)+'_fig1.png', bbox_inches='tight')
	plt.close()
#raw_input()
miracle_params = []
for pk_i in range(pk_len):
	pk = poiss_keys[pk_i]
	fig2 = plt.figure()
	ax = fig2.add_subplot(111)
	ax.set_xlabel('Tau constant parameter')
	ax.set_ylabel('Standard weight parameter')
	ax.spines['top'].set_color('none')
	ax.spines['bottom'].set_color('none')
	ax.spines['left'].set_color('none')
	ax.spines['right'].set_color('none')
	ax.tick_params(labelcolor='w', top='off', bottom='off', left='off', right='off')
	fig2.suptitle('Absolute variations in Phi values calculated for each starting state of network \n (Poisson point process of lambda='+str(pk/10.)+'ms)\n as a function of weight and tau parameters')
	#fig2.suptitle('Relative variations in Phi values calculated for each starting state of network \n (Poisson point process of lambda='+str(pk/10.)+'ms)\n as a function of weight and tau parameters')
	for sk_i in range(sk_len):
		sk = state_keys[sk_i]
		ax = fig2.add_subplot(sk_len/4, 4, sk_i+1)
		data_abs = np.zeros([wk_len, tk_len])
		data_rel = np.zeros([wk_len, tk_len])
		for wk_i in range(wk_len):
			wk = weight_keys[wk_i]
			for tk_i in range(tk_len):
				tk = tau_keys[tk_i]
				for key, value in pyphi_dict.items():
					ref_value = pyphi_dict_ref[wk, tk, sk]
					if key == (pk, wk, tk, sk) and isinstance(value,float):
						if isinstance(ref_value,float):
							data_abs[wk_i, tk_i] = value - ref_value
							data_rel[wk_i, tk_i] = (value - ref_value)/ref_value*100
						elif isinstance(ref_value,str):
							miracle_params.append(key)
							data_abs[wk_i, tk_i] = value
							data_rel[wk_i, tk_i] = 0
						else:
							print 'wtf'	
					elif key == (pk, wk, tk, sk) and isinstance(value,str):
						if isinstance(ref_value,float):
							data_abs[wk_i, tk_i] = -ref_value
							data_rel[wk_i, tk_i] = 0
							miracle_params.append('REVERSE! '+str(key))
		im = ax.imshow(data_abs, cmap='bwr', interpolation='nearest', vmin=-1.5, vmax=1.5)
		#im = ax.imshow(data_rel, cmap='bwr', interpolation='nearest')
		if sk_i not in (0,4): ax.yaxis.set_visible(False)
		ax.title.set_text(sk)
		if not prefix=='10x10':
			plt.xticks(range(tk_len), tau_keys, fontsize=7)
		else:
			plt.xticks(range(tk_len), tau_keys, fontsize=5)
		plt.yticks(range(wk_len), weight_keys, fontsize=7)
	fig2.subplots_adjust(right=0.8)
	cbar_ax = fig2.add_axes([0.85, 0.15, 0.05, 0.7])
	fig2.colorbar(im, cax=cbar_ax)
	#plt.savefig('files_figures/comparison/'+prefix+'_abs_variation_mean_poiss_'+str(pk/10.)+'.png', bbox_inches='tight')
	#plt.savefig('files_figures/comparison/'+prefix+'_rel_variation_mean_poiss_'+str(pk/10.)+'.png', bbox_inches='tight')
	plt.show()
print miracle_params
