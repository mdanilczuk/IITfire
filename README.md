_sim_functions.py : basic tools for setting up neuron simulation and calculation of TPM

1_matrix_generator.py : creates TPMs, parameters (neuron types, weights etc) and other arrays necessary for calculating PHI of a particular system

2_matrix_reader.py : PHI calculation via the PyPhi package

3_log_creator.sh compiles the results of PHI calculations of many simulations with various parameters into one 'dataset' txt file

4a_log_reader_trinode.py , 4b_log_reader_poisson.py , 5_log_comparison.py : used to process and compare 'dataset' files and plot figures based on the results

bla bla test
