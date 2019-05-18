import numpy as np
import sys
from dspBox import str2ndar
from viterbi import run

for ff in range(1, 4):
	a = np.array([[0.3, 0.3, 0.4],
				  [0.3, 0.3, 0.4],
				  [0.4, 0.4, 0.2]])
	b = np.array([[0.4, 0.4, 0.2],
				  [0.3, 0.3, 0.4],
				  [0.3, 0.3, 0.4]])
	pi = np.array([0.3, 0.3, 0.4])

	#file_path = sys.argv[1]

	for _ in range(10):
		a_up = np.zeros([pi.size, pi.size])
		a_down = np.zeros([pi.size])
		b_up = np.zeros_like(a_up)
		b_down = np.zeros_like(a_up)
		pi_temp = np.zeros_like(a_down)

		with open("training\\model_%d_training.txt" % (ff), 'r') as f:
			lines = f.readlines()
			for content in lines:
				o = str2ndar(content)
				
				alpha = np.zeros([len(o), pi.size])
				beta = np.zeros_like(alpha)
				for t in range(len(o)):
					word = o[t]
					beta_time = len(o) - 1 - t

					if t == 0:
						for i in range(pi.size):
							alpha[t, i] = pi[i] * b[i, word]
							beta[beta_time, i] = 1
						continue

					for j in range(pi.size):
						for i in range(pi.size):
							alpha[t, j] += alpha[t - 1, i] * a[i, j]
						alpha[t, j] *= b[j, o[t]]

					for i in range(pi.size):
						for j in range(pi.size):
							beta[beta_time, i] += a[i, j] * b[j, o[beta_time + 1]] * beta[beta_time + 1, j]

				xi = np.zeros([len(o), pi.size, pi.size])
				for t in range(len(o) - 1):
					temp = 0
					for i in range(pi.size):
						for j in range(pi.size):
							temp += alpha[t, i] * a[i, j] * b[j, o[t + 1]] * beta[t + 1, j]
					for i in range(pi.size):
						for j in range(pi.size):
							xi[t, i, j] = alpha[t, i] * a[i, j] * b[j, o[t + 1]] * beta[t + 1, j] / temp

				r_i = np.zeros_like(alpha)
				for t in range(len(o)):
					for i in range(pi.size):
						for j in range(pi.size):
							r_i[t, i] += xi[t, i, j]

				r_j = np.zeros_like(r_i)
				for t in range(len(o)):
					for j in range(pi.size):
						for i in range(pi.size):
							r_j[t, j] += xi[t, i, j]

				
				for i in range(pi.size):
					for j in range(pi.size):
						a_up[i, j] += np.sum(xi, axis = 0)[i, j]
					a_down[i] += np.sum(r_i, axis = 0)[i]

				for j in range(pi.size):
					for k in range(pi.size):
						up, down = 0, 0
						for t in range(len(o)):
							if o[t] == k:
								up += r_j[t, j]
							down += r_j[t, j]
						b_up[j, k] += up
						b_down[j, k] += down

				for i in range(pi.size):
					pi_temp[i] += r_i[0, i]
				
		
		for i in range(pi.size):
			for j in range(pi.size):
				a[i, j] = a_up[i, j] / a_down[i]

		for j in range(pi.size):
			for k in range(pi.size):
				b[j, k] = b_up[j, k] / b_down[j, k]
		
		for i in range(pi.size):
			pi[i] = pi_temp[i] / len(lines)

	
	print("model", ff, "\nA:\n", a)
	print("B:\n", b)
	print("PI:\n", pi)
	print ("---------------------------------------------")

	if ff == 1:
		aa = np.array([a])
		bb = np.array([b])
		pp = np.array([pi])
	else:
		a = np.array([a])
		b = np.array([b])
		pi = np.array([pi])
		aa = np.append(aa, a, axis = 0)
		bb = np.append(bb, b, axis = 0)
		pp = np.append(pp, pi, axis = 0)

run(aa, bb, pp)