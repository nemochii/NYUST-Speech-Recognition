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
	with open("obser%d.txt" % (a)) as f:
		content = f.read()
		data = str2ndar(content)

	forward_S = np.zeros([3, 3])
	temp = np.zeros([3, 3])
	for i in range(len(data)):
		word = data[i]

		if i == 0:
			for model in range(3):
				for state in range(3):
					forward_S[model, state] = pi[model, state] * eachopt[model, state, word]
			continue

		temp *= 0
		for model in range(3):
			for state in range(3):
				for weight in range(3):
					temp[model, state] += forward_S[model, weight] * allopt[model, weight, state] 					
				temp[model, state] *= eachopt[model, state, word]

		for model in range(3):
			for state in range(3):
				forward_S[model, state] = temp[model, state]
	forward_S = np.sum(forward_S, axis = 1)

	backward_S = np.zeros([3, 3])
	for i in range(len(data) - 1, -1, -1):
		word = data[i]

		if i == len(data) - 1:
			for model in range(3):
				for state in range(3):
					backward_S[model, state] = 1
			continue

		temp *= 0
		for model in range(3):
			for state in range(3):
				for weight in range(3):
					temp[model, state] += backward_S[model, weight] * allopt[model, state, weight] * eachopt[model, weight, data[i + 1]]

		for model in range(3):
			for state in range(3):
				backward_S[model, state] = temp[model, state]
	
	backward_S_result = np.zeros(3)
	for model in range(3):
		for state in range(3):
			backward_S_result[model] += backward_S[model, state] * pi[model, state] * eachopt[model, state, word]
	
	print ("obser%d" % (a))
	for m in range(3):
		print ("model_%d forward:%.16e backward:%.16e" % (m + 1, forward_S[m], backward_S_result[m]))