import numpy as np
from dspBox import str2ndar
from viterbi import predict

def compute_alpha_beta(o, a, b, pi):
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

	return (alpha, beta)

def compute_xi_ri_rj(o, a, b, pi, alpha, beta):
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

	return (xi, r_i, r_j)

def compute_sigma(o, pi, xi, r_i, r_j, a_up, a_down, b_up, b_down, pi_temp):
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

	return (a_up, a_down, b_up, b_down, pi_temp)

def update_weight(a, b, pi, a_up, a_down, b_up, b_down, pi_temp, quantity):
	for i in range(pi.size):
		for j in range(pi.size):
			a[i, j] = a_up[i, j] / a_down[i]

	for j in range(pi.size):
		for k in range(pi.size):
			b[j, k] = b_up[j, k] / b_down[j, k]
	
	for i in range(pi.size):
		pi[i] = pi_temp[i] / quantity

	return (a, b, pi)

def train(lines):
	a = np.array([[0.3, 0.3, 0.4],
				  [0.3, 0.3, 0.4],
				  [0.4, 0.4, 0.2]])
	b = np.array([[0.4, 0.4, 0.2],
				  [0.3, 0.3, 0.4],
				  [0.3, 0.3, 0.4]])
	pi = np.array([0.3, 0.3, 0.4])

	for _ in range(10):
		a_up = np.zeros([pi.size, pi.size])
		a_down = np.zeros([pi.size])
		b_up = np.zeros_like(a_up)
		b_down = np.zeros_like(a_up)
		pi_temp = np.zeros_like(a_down)

		for content in lines:
			o = str2ndar(content)
			
			alpha, beta = compute_alpha_beta(o, a, b, pi)
			xi, r_i, r_j = compute_xi_ri_rj(o, a, b, pi, alpha, beta)
			a_up, a_down, b_up, b_down, pi_temp = compute_sigma(o, pi, xi, r_i, r_j, a_up, a_down, b_up, b_down, pi_temp)

		a, b, pi = update_weight(a, b, pi, a_up, a_down, b_up, b_down, pi_temp, len(lines))
		
	print ("model", data_set, "\nA:\n", a)
	print ("B:\n", b)
	print ("PI:\n", pi)
	print ("---------------------------------------------")

	return (a, b, pi)

if __name__ == "__main__":
	for data_set in range(1, 4):
		with open("training\\model_%d_training.txt" % (data_set), 'r') as f:
			lines = f.readlines()

		print ("Training model %d now..." % (data_set))
		a, b, pi = train(lines)

		with open("model_%d.txt" % (data_set), 'w') as wf:
			wf.write("A:\n{}\nB:\n{}\nPI:\n{}".format(a, b, pi))

		if data_set == 1:
			final_a = np.array([a])
			final_b = np.array([b])
			final_pi = np.array([pi])
		else:
			a = np.array([a])
			b = np.array([b])
			pi = np.array([pi])
			final_a = np.append(final_a, a, axis = 0)
			final_b = np.append(final_b, b, axis = 0)
			final_pi = np.append(final_pi, pi, axis = 0)

	print ("Predicting now...")
	predict(final_a, final_b, final_pi)
	print ("All function done!")