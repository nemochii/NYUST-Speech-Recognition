import numpy as np
import sys
from dspBox import str2ndar

a = np.array([[0.3, 0.3, 0.4],
			  [0.3, 0.3, 0.4],
			  [0.4, 0.4, 0.2]])
b = np.array([[0.4, 0.4, 0.2],
			  [0.3, 0.3, 0.4],
			  [0.3, 0.3, 0.4]])
pi = np.array([0.3, 0.3, 0.4])

file_path = sys.argv[1]
with open(file_path, 'r') as f:
	content = f.readline()
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
		a[i, j] = np.sum(xi, axis = 0)[i, j] / np.sum(r_i, axis = 0)[i]

for j in range(pi.size):
	for k in range(pi.size):
		up, down = 0, 0
		for t in range(len(o)):
			if o[t] == k:
				up += r_j[t, j]
			down += r_j[t, j]
		b[j, k] = up / down

for i in range(pi.size):
	pi[i] = r_i[0, i]

print("A:\n", a)
print("B:\n", b)
print("PI:\n", pi)