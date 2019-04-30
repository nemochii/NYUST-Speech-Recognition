import numpy as np
from dspBox import str2ndar

allopt = np.array([[[0.2, 0.7, 0.1],	
				    [0.1, 0.2, 0.7], 
				    [0.7, 0.1, 0.2]],
				   [[0.7, 0.2, 0.1],
				    [0.3, 0.6, 0.1],
				    [0.1, 0.2, 0.7]],
				   [[0.2, 0.7, 0.1],
				    [0.6, 0.3, 0.1],
				    [0.2, 0.7, 0.1]]])
eachopt = np.array([[[0.5, 0.4, 0.1],	
				     [0.7, 0.2, 0.1],
				     [0.7, 0.1, 0.2]],
				    [[0.1, 0.8, 0.1],
				     [0.2, 0.7, 0.1],
				     [0.4, 0.5, 0.1]],
				    [[0.1, 0.2, 0.7],
				     [0.2, 0.2, 0.6],
				     [0.3, 0.1, 0.6]]])
pi = np.array([[0.7, 0.2, 0.1],
			   [0.1, 0.7, 0.2],
			   [0.2, 0.2, 0.6]])

for a in range(1, 4):
	with open("Observation_%d.txt" % (a)) as f:
		content = f.read()
		data = str2ndar(content)

	forward_S = np.zeros([3, 3])
	temp = np.zeros([3, 3])
	max_state = np.zeros([3])
	back_path = np.zeros([3, len(data), 3])
	path = np.zeros([3, len(data)], dtype = np.int8)
	for i in range(len(data)):
		word = data[i]

		if i == 0:
			for model in range(3):
				for state in range(3):
					forward_S[model, state] = pi[model, state] * eachopt[model, state, word]
			continue

		for model in range(3):
			for state in range(3):
				for weight in range(3):
					max_state[weight] = allopt[model, weight, state] * forward_S[model, weight]
				temp[model, state] = np.max(max_state) * eachopt[model, state, word]
				back_path[model, i, state] = np.argmax(max_state)
		
		for model in range(3):
			for state in range(3):
				forward_S[model, state] = temp[model, state]
		
		if i == len(data) - 1:
			for model in range(3):
				path[model, i] = np.argmax(forward_S, axis = 1)[model]

				for k in range(i - 1, -1, -1):
					path[model, k] = back_path[model, k + 1, path[model, k + 1]]
	forward_S = np.max(forward_S, axis = 1)
	
	print ("obser%d" % (a))
	for m in range(3):
		print ("model_%d probability:%.16e " % (m + 1, forward_S[m]))
		print ("viterbi max state sequence ", path[m])
	print ("")