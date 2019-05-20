import numpy as np
from dspBox import str2ndar

def predict(allopt, eachopt, pi):
	with open("Observations.txt", 'r') as f:
		lines = f.readlines()
		wf = open("Observations_Ans.txt", 'w')
		for content in lines:
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

			wf.write("model %d\n" % (np.argmax(forward_S) + 1))

		wf.close()