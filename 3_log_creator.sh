#!/bin/bash 
# chmod u+x 3_log_creator.sh
# ./3_log_creator.sh
filename=/home/praceeg1/Desktop/gigaspaghetti/iit2021/files_logs/log_1_$(date +"%m_%d_%y_%H_%M_%S").txt

LOOP1=8
LOOP2=1
LOOP3=1
LOOP4=8
LOOP5=2
COUNTER0=0
COUNTER1=0
while [ $COUNTER1 -lt $LOOP1 ]; do
	param1=$(bc <<<"scale=2;12.5+$COUNTER1*12.5")
	COUNTER2=0
	while [ $COUNTER2 -lt $LOOP2 ]; do
		param2=$(bc <<<"scale=2;-100+$COUNTER2*2")
		COUNTER3=0
		while [ $COUNTER3 -lt $LOOP3 ]; do
			param3=$(bc <<<"scale=2;-50+$COUNTER3*25")
			COUNTER4=0
			while [ $COUNTER4 -lt $LOOP4 ]; do
				param4=$(bc <<<"scale=2;0.1+$COUNTER4*0.1")
				COUNTER5=0
				while [ $COUNTER5 -lt $LOOP5 ]; do
					param5=$(bc <<<"scale=2;28+$COUNTER5*5")
					echo SIMULATION $COUNTER0
					echo Parameters: $param1 $param2 $param3 $param4 $param5
					echo SIMULATION $COUNTER0 >> $filename
					echo Parameters: >> $filename
					echo Standard weight: $param1 >> $filename
					echo Rest potential: $param2 >> $filename
					echo Standard threshold: $param3 >> $filename
					echo Tau constant: $param4 >> $filename
					echo Mean Poisson difference: $param5 >> $filename
					python2 1_matrix_generator.py $param1 $param2 $param3 $param4 $param5 >> $filename
					python3 2_matrix_reader.py >> $filename
					
					let COUNTER5+=1
					let COUNTER0+=1
				done
				let COUNTER4+=1
			done
			let COUNTER3+=1
		done
		let COUNTER2+=1
	done
	let COUNTER1+=1
done
geany $filename
